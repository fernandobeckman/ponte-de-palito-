#!/usr/bin/env python3
"""Manual de montagem estilo LEGO (docs/manual.html).

Uso em duas fases:
  python3 projeto/gerar_manual_site.py plano    -> projeto/manual/plano.json (passos, peças, enquadramento)
  node projeto/renderizar_manual.js <three> <tmp> -> imagens em docs/img/manual/ e projeto/manual/posicoes.json
  python3 projeto/gerar_manual_site.py pagina   -> docs/manual.html
"""
import json, os, sys

D = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(D, "..")
mont = json.load(open(os.path.join(D, "montagem.json")))
P, TIPOS = mont["passos"], {t["cod"]: t for t in mont["tipos"]}
PLANO = os.path.join(D, "manual", "plano.json")
POS = os.path.join(D, "manual", "posicoes.json")

PLANO_DIR = [0.12, 1.0, 0.5]       # treliça deitada: de cima, levemente inclinado
TRES_D = [-0.55, 0.6, 0.95]        # ponte de pé
POR_BAIXO = [-0.35, -0.22, 1.0]    # peças coladas por baixo dos banzos
INSTR = {
    "chapas da face de baixo": "Corte as chapas e coloque cada uma sobre o plástico, no nó marcado no gabarito. Ainda sem cola.",
    "camada 1": "Corte e coloque as peças da camada 1 por cima das chapas. Cola só onde a peça apoia nas chapas. Encoste as pontas de topo, sem fresta.",
    "camada 2": "Passe um cordão de cola sobre a camada de baixo e coloque cada peça por cima, alinhada. As emendas ficam desencontradas pelo menos 30 mm das da camada 1. Pressione 30 s.",
    "camada 3": "Mesma coisa da camada 2: cordão de cola, peça alinhada por cima e 30 s de pressão. As emendas ficam desencontradas das camadas de baixo.",
    "chapas da face de cima": "Passe cola em toda a face de cada chapa e cole sobre o nó, cobrindo o banzo e as pontas das barras. Limpe o excesso de cola.",
}

def faixa(nums):
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}–{nums[j]}"); i = j + 1
    return ", ".join(out)

def chave_w(nome):
    """Elemento a que a peça do mundo pertence (todas as camadas de uma transversina, de um consolo, de uma camada da mini-treliça)."""
    import re
    if nome.startswith("Consolo"): return "Consolos"
    if nome.startswith("Mini-treliça"):
        m = re.search(r"(face \d|camada \d)", nome); return "Mini-treliça " + (m.group(1) if m else "")
    return nome.split(", camada")[0].split(", peça")[0]

def texto_w(cap, ch):
    """Texto e subtítulo de um passo com peças do mundo (elementos inteiros)."""
    els = []
    for k in ch:
        e = chave_w(P[k]["nome"])
        if e not in els: els.append(e)
    ids = " e ".join(e.split()[-1] for e in els)
    um = len(els) == 1
    nos, pains = ("do nó" if um else "dos nós"), ("do painel" if um else "dos painéis")
    if cap == "Transversinas inferiores":
        return (f"Cole {'a transversina' if um else 'as transversinas'} {nos} {ids} por baixo dos dois banzos, de uma face externa à outra (220 mm). "
                "São 2 camadas, com as emendas desencontradas."), f"nós {ids}"
    if cap == "Contraventamento inferior":
        return (f"Cole {'a diagonal' if um else 'as diagonais'} de baixo {pains} {ids}, por baixo dos banzos e entre as transversinas, em 2 camadas. "
                "Elas formam um zigue-zague."), f"painéis {ids}"
    if cap == "Escoras superiores":
        return f"Cole {'a escora' if um else 'as escoras'} {nos} {ids} por cima dos dois banzos de cima, em 2 camadas com as emendas desencontradas.", f"{'nó' if um else 'nós'} {ids}"
    if cap == "Contraventamento superior":
        return f"Cole {'a diagonal' if um else 'as diagonais'} de cima {pains} {ids}, sobre os banzos e entre as escoras, em 2 camadas.", f"painéis {ids}"
    if els == ["Consolos"]:
        return ("Cole os consolos: 3 camadas de 30 mm na face de dentro do nó b4 de cada treliça, alinhadas com o banzo de baixo. "
                "O topo deles fica na altura do topo do banzo."), "consolos"
    e = els[0].replace("Mini-treliça ", "")
    if e == "face 1":
        return "Mini-treliça: coloque as chapas da primeira face sobre o plástico, nos nós, ainda sem cola.", "mini-treliça, chapas da face 1"
    if e == "face 2":
        return "Mini-treliça: passe cola em toda a face de cada chapa e cole sobre os nós, cobrindo o banzo e as pontas das barras.", "mini-treliça, chapas da face 2"
    k = e.split()[-1]
    if k == "1":
        return ("Mini-treliça, camada 1: banzos, montantes e diagonais por cima das chapas. Cola só onde a peça apoia nas chapas. "
                "Encoste as pontas de topo."), "mini-treliça, camada 1"
    return f"Mini-treliça, camada {k}: cordão de cola sobre a camada de baixo e cada peça alinhada por cima. Emendas desencontradas.", f"mini-treliça, camada {k}"

def plano():
    passos, i = [], 0
    pecas_de = lambda g: [k for k, p in enumerate(P) if p["k"] == "pc" and p["g"] == g]
    ponte = [k for k, p in enumerate(P) if p["k"] == "pc" and p["g"] != "E"]
    ev = {p["ev"]: k for k, p in enumerate(P) if p["k"] == "ev"}
    def novo(**kw): kw["n"] = len(passos) + 1; kw["img"] = f"img/manual/p{kw['n']:02d}.jpg" if kw.get("t") is not None else None; passos.append(kw)
    while i < len(P):
        p = P[i]
        if p["k"] == "ev":
            e = p["ev"]
            base = dict(titulo=p["cap"], texto=p["txt"], det=p["det"], pecas=[], abre=i + 1)
            if e == "materiais":
                novo(**base, t=i + 1, quadro=[], extra=[[-150, 0, 180], [1150, 0, 540]], dir=[0.0, 1.0, 0.8])
            elif e in ("prensaA", "prensaB"):
                novo(**base, t=i + 1, quadro=pecas_de(e[-1]), dir=PLANO_DIR)
            elif e == "lixa":
                novo(**base, t=i + 0.5, quadro=pecas_de("A") + pecas_de("B"), dir=PLANO_DIR)
            elif e in ("levantaA", "levantaB", "colocaE", "tiraesp"):
                q = pecas_de("A") + (pecas_de("B") if e != "levantaA" else [])
                novo(**base, t=i + 1, quadro=q, dir=TRES_D, destaque=pecas_de("E") if e == "colocaE" else [])
            elif e == "ensaio":
                novo(**base, t=i + 1, quadro=ponte, extra=[[400, 60, 0]], dir=TRES_D)
            else:
                novo(**base, t=None)
            i += 1; continue
        cap = p["cap"]; j = i
        while j < len(P) and P[j]["k"] == "pc" and P[j]["cap"] == cap: j += 1
        grupo = list(range(i, j))
        tam = 99 if cap.startswith("Treliça B") else 8
        if P[i]["g"] == "W":
            # peças do mundo: um passo por elemento inteiro (2 elementos por passo; ponto de carga por camada)
            blocos, chave_ant = [], None
            for k in grupo:
                c = chave_w(P[k]["nome"])
                if c != chave_ant: blocos.append([]); chave_ant = c
                blocos[-1].append(k)
            junta = 1 if cap == "Ponto de carga" else 2
            pedacos = [sum(blocos[b:b + junta], []) for b in range(0, len(blocos), junta)]
        else:
            pedacos = [grupo[a:a + tam] for a in range(0, len(grupo), tam)]
        for a_, ch in enumerate(pedacos):
            sub = ""
            parte = cap.split(" · ")[-1]
            if cap.startswith("Treliça B"):
                txt = f"Faça igual à treliça A: {INSTR.get(parte, '')}"
            elif cap.startswith("Treliça A"):
                txt = INSTR.get(parte, P[ch[0]]["txt"])
            elif P[ch[0]]["g"] == "W":
                txt, sub = texto_w(cap, ch)
            else:
                txt = P[ch[0]]["txt"].split(": ", 1)[-1][:1].upper() + P[ch[0]]["txt"].split(": ", 1)[-1][1:]
            det = P[ch[0]]["det"].split(" Comprimento")[0]
            g = P[ch[0]]["g"]
            if g in ("A", "B"):
                quadro, d = ch if len(ch) > 3 else pecas_de(g), PLANO_DIR
            elif g == "E":
                quadro, d = ch, [0.1, 0.9, 0.7]
            else:
                baixo = "inferior" in P[ch[0]]["nome"]
                quadro, d = ch + [ch[0]], (POR_BAIXO if baixo else TRES_D)
            nums = [P[k]["num"] for k in ch]
            if P[ch[0]]["g"] == "W": titulo = f"{cap} · {sub}"
            else: titulo = cap + (f" · parte {a_ + 1}" if len(pedacos) > 1 else "")
            novo(titulo=titulo, texto=txt, det=det, pecas=ch, destaque=ch, t=ch[-1] + 1, quadro=quadro, dir=d,
                 abre=ch[-1] + 1, faixa=faixa(nums))
        i = j
    os.makedirs(os.path.dirname(PLANO), exist_ok=True)
    json.dump(passos, open(PLANO, "w"), ensure_ascii=False, indent=0)
    print(len(passos), "passos,", sum(1 for s in passos if s["img"]), "imagens")

def pagina():
    passos = json.load(open(PLANO)); pos = json.load(open(POS)) if os.path.exists(POS) else {}
    sys.path.insert(0, D)
    import gerar_site as gs   # reaproveita cabeçalho, menu e estilos de navegação
    pecas = {k: dict(num=P[k]["num"], cod=P[k]["cod"], nome=P[k]["nome"], passo=k + 1) for s in passos for k in s["pecas"]}
    def espalha(rot, dx=.075, dy=.06):
        """Afasta etiquetas que ficariam uma sobre a outra (em coordenadas 0-1 da imagem).
        Cada item vira [peça, x da peça, y da peça, x da etiqueta, y da etiqueta]."""
        out = []
        for k, x, y in sorted(rot, key=lambda r: (r[2], r[1])):
            lx, ly = x, y
            for _ in range(40):
                choque = [o for o in out if abs(o[3] - lx) < dx and abs(o[4] - ly) < dy]
                if not choque: break
                ly = max(o[4] for o in choque) + dy
                if ly > .96: ly, lx = y, lx + dx
            out.append([k, x, y, round(min(.97, max(.03, lx)), 4), round(min(.97, max(.03, ly)), 4)])
        return out
    for s in passos:
        s["rotulos"] = espalha(pos.get(str(s["n"]), []))
        cont = {}
        for k in s["pecas"]: cont[P[k]["cod"]] = cont.get(P[k]["cod"], 0) + 1
        s["caixa"] = sorted(cont.items(), key=lambda x: (-x[1], x[0]))
    dados = dict(passos=passos, pecas=pecas, tipos=TIPOS)
    html = open(os.path.join(D, "manual_modelo.html")).read()
    html = (html.replace("__CABECA__", gs.cabeca_comum("Manual de montagem da ponte de palito",
                         "Manual passo a passo, como os de LEGO, para montar a ponte de palito de picolé."))
                .replace("__NAVCSS__", gs.NAV_CSS).replace("__NAV__", gs.nav("manual.html"))
                .replace("__DADOS__", json.dumps(dados, ensure_ascii=False, separators=(",", ":"))))
    open(os.path.join(R, "docs", "manual.html"), "w").write(html)
    print("docs/manual.html", len(html) // 1024, "KB")

if __name__ == "__main__":
    {"plano": plano, "pagina": pagina}[sys.argv[1]]()
