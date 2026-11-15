#!/usr/bin/env python3
"""Reaproveitamento das peças já cortadas para a ponte antiga (Parker 8×90, manual de corte de 09/11, commit 7b592f4).

Para cada peça da ponte nova, procura uma peça antiga onde ela caiba, recortando se preciso. O encaixe é geométrico:
cada peça é uma faixa de 8,4 mm com pontas cortadas; para cada altura y da faixa comparamos o começo e o fim da
peça nova com os da peça antiga (4 jeitos de virar o palito). Uma peça antiga pode render mais de uma peça nova,
com 0,5 mm de perda em cada corte. O que não couber em nenhuma peça antiga sai de palito novo (101,6 mm úteis).

Entradas: projeto/manual/parker_montagem.json (cópia congelada da ponte antiga) e projeto/montagem.json (ponte nova).
Saída: projeto/manual/reaproveitamento.json
"""
import json, os

D = os.path.dirname(os.path.abspath(__file__))
ANT = json.load(open(os.path.join(D, "manual", "parker_montagem.json")))
NOV = json.load(open(os.path.join(D, "montagem.json")))
W, KERF, L_UTIL = 8.4, 0.5, 101.6
YS = [-4.1 + 8.2 * i / 20 for i in range(21)]

def perfil(poly):
    """Para cada y de YS: (x inicial, x final) da peça (polígono convexo)."""
    out = []
    for y in YS:
        xs = []
        n = len(poly)
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            if (y1 - y) * (y2 - y) <= 0 and abs(y2 - y1) > 1e-9:
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        out.append((min(xs), max(xs)) if xs else (None, None))
    return out

def variantes(poly):
    L = max(x for x, _ in poly)
    vs = []
    for fx in (False, True):
        for fy in (False, True):
            p = [((L - x) if fx else x, (-y) if fy else y) for x, y in poly]
            pf = perfil(p)
            if all(a is not None for a, _ in pf) and pf not in vs: vs.append(pf)
    return vs

class Estoque:
    """Uma peça antiga (ou um palito novo) sendo recortada da esquerda para a direita."""
    def __init__(self, origem, pf):
        self.origem, self.pf, self.ocup, self.pecas = origem, pf, None, []
    def tenta(self, var_nova):
        melhor = None
        for pn in var_nova:
            s = max(max(self.pf[i][0], (self.ocup[i] + KERF) if self.ocup else -1e9) - pn[i][0] for i in range(len(YS)))
            if all(s + pn[i][1] <= self.pf[i][1] + 1e-6 for i in range(len(YS))):
                fim = max(s + pn[i][1] for i in range(len(YS)))
                if melhor is None or fim < melhor[0]: melhor = (fim, s, pn)
        return melhor
    def coloca(self, res, peca):
        fim, s, pn = res
        self.ocup = [s + pn[i][1] for i in range(len(YS))]; self.pecas.append(peca)
    def sobra(self):
        return min(self.pf[i][1] - (self.ocup[i] if self.ocup else self.pf[i][0]) for i in range(len(YS)))

# estoque antigo: todas as peças cortadas da ponte antiga (inclusive espaçadores)
tipos_ant = {t["cod"]: t for t in ANT["tipos"]}
estoque_ant = {c: t["qtd"] for c, t in tipos_ant.items()}
perfil_ant = {c: perfil(t["poly"]) for c, t in tipos_ant.items()}
tipos_nov = {t["cod"]: t for t in NOV["tipos"]}
var_nov = {c: variantes(t["poly"]) for c, t in tipos_nov.items()}
pecas_nov = [p for p in NOV["passos"] if p["k"] == "pc"]

def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))) / 2

def igual(cn, ca):
    """Mesma forma (sem recorte): mesmo comprimento e mesmas bordas, com 0,3 mm de folga."""
    a, b = tipos_nov[cn], tipos_ant[ca]
    return abs(a["L"] - b["L"]) <= .3 and abs(a["bordaA"] - b["bordaA"]) <= .3 and abs(a["bordaB"] - b["bordaB"]) <= .3 \
        and a["txt_esq"] == b["txt_esq"] and a["txt_dir"] == b["txt_dir"]

abertos, novos = [], []           # peças antigas já em uso / palitos novos
destino = {}                      # número da peça nova -> origem
ordem = sorted(pecas_nov, key=lambda p: (-tipos_nov[p["cod"]]["L"], -area(tipos_nov[p["cod"]]["poly"]), p["num"]))
for p in ordem:
    vn = var_nov[p["cod"]]
    # 1) mesma forma, sem recorte
    exato = next((c for c in estoque_ant if estoque_ant[c] and igual(p["cod"], c)), None)
    if exato:
        estoque_ant[exato] -= 1
        e = Estoque(("antiga", exato), perfil_ant[exato]); e.coloca((tipos_ant[exato]["L"], 0, perfil_ant[exato]), p["num"])
        e.exato = True; abertos.append(e); destino[p["num"]] = dict(de="antiga", cod_ant=exato, recorte=False); continue
    # 2) sobra de uma peça antiga já recortada (a que ficar com menos sobra)
    cands = [(r[0], e, r) for e in abertos if not getattr(e, "exato", False) for r in [e.tenta(vn)] if r]
    if cands:
        _, e, r = min(cands, key=lambda t: t[1].pf[0][1] - t[0])
        e.coloca(r, p["num"]); destino[p["num"]] = dict(de="antiga", cod_ant=e.origem[1], recorte=True); continue
    # 3) abrir uma peça antiga nova: a menor em que caiba
    op = []
    for c in estoque_ant:
        if not estoque_ant[c]: continue
        e = Estoque(("antiga", c), perfil_ant[c]); r = e.tenta(vn)
        if r: op.append((tipos_ant[c]["L"], c, e, r))
    if op:
        _, c, e, r = min(op, key=lambda t: (t[0], t[1]))
        estoque_ant[c] -= 1; e.coloca(r, p["num"]); abertos.append(e)
        destino[p["num"]] = dict(de="antiga", cod_ant=c, recorte=True); continue
    # 4) palito novo (sobra de um já aberto, ou um palito novo)
    ret = [[0, -4.2], [L_UTIL, -4.2], [L_UTIL, 4.2], [0, 4.2]]
    cands = [(r[0], e, r) for e in novos for r in [e.tenta(vn)] if r]
    if cands:
        _, e, r = max(cands, key=lambda t: t[0]); e.coloca(r, p["num"])
    else:
        e = Estoque(("novo", len(novos) + 1), perfil(ret)); r = e.tenta(vn); e.coloca(r, p["num"]); novos.append(e)
    destino[p["num"]] = dict(de="novo", palito=e.origem[1])

# resumo por montinho antigo: o que cada peça antiga vira
por_ant = {}
for e in abertos:
    c = e.origem[1]
    chave = tuple(sorted(next(q["cod"] for q in pecas_nov if q["num"] == n) for n in e.pecas))
    por_ant.setdefault(c, {}).setdefault(chave, 0)
    por_ant[c][chave] += 1
num2 = {p["num"]: p for p in pecas_nov}
res = dict(
    origem_antiga="manual de corte da ponte Parker 8x90 (09/11, commit 7b592f4)",
    destino={str(k): v for k, v in sorted(destino.items())},
    montinhos=[dict(cod_ant=c, L_ant=tipos_ant[c]["L"], nome_ant=tipos_ant[c]["nome_cat"], tem=tipos_ant[c]["qtd"],
                    usa=sum(por_ant.get(c, {}).values()), sobra=tipos_ant[c]["qtd"] - sum(por_ant.get(c, {}).values()),
                    vira=[dict(novos=list(k), qtd=q, sem_corte=all(igual(x, c) for x in k) and len(k) == 1)
                          for k, q in sorted(por_ant.get(c, {}).items(), key=lambda t: -t[1])])
               for c in tipos_ant],
    novas_de_palito={},
    palitos_novos=len(novos),
)
for n, d in destino.items():
    if d["de"] == "novo":
        c = num2[n]["cod"]; res["novas_de_palito"][c] = res["novas_de_palito"].get(c, 0) + 1
json.dump(res, open(os.path.join(D, "manual", "reaproveitamento.json"), "w"), ensure_ascii=False, indent=1)

tot = len(pecas_nov); de_ant = sum(1 for d in destino.values() if d["de"] == "antiga")
sem = sum(1 for d in destino.values() if d["de"] == "antiga" and not d["recorte"])
print(f"Peças da ponte nova: {tot}  |  de peças antigas: {de_ant} ({sem} sem recorte)  |  de palito novo: {tot - de_ant}")
print(f"Peças antigas usadas: {sum(m['usa'] for m in res['montinhos'])} de {sum(m['tem'] for m in res['montinhos'])}")
print(f"Palitos novos necessários: {len(novos)} (sem reaproveitar seriam {NOV['resumo']['palitos_ponte'] + NOV['resumo']['palitos_esp']})")
for m in res["montinhos"]:
    vira = "; ".join(f"{v['qtd']}× → {'+'.join(v['novos'])}{' (igual)' if v['sem_corte'] else ''}" for v in m["vira"])
    print(f"  antiga {m['cod_ant']:4} {m['L_ant']:6.1f} mm  tem {m['tem']:3}  usa {m['usa']:3}  sobra {m['sobra']:3}  | {vira}")
print("Novas de palito novo:", res["novas_de_palito"])
