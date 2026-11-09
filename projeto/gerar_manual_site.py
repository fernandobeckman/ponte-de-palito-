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
                novo(**base, t=i + 1, quadro=[], extra=[[-60, 0, 150], [760, 0, 470]], dir=[0.0, 1.0, 0.8])
            elif e in ("prensaA", "prensaB"):
                novo(**base, t=i + 1, quadro=pecas_de(e[-1]), dir=PLANO_DIR)
            elif e == "lixa":
                novo(**base, t=i + 0.5, quadro=pecas_de("A") + pecas_de("B"), dir=PLANO_DIR)
            elif e in ("levantaA", "levantaB", "colocaE", "tiraesp"):
                q = pecas_de("A") + (pecas_de("B") if e != "levantaA" else [])
                novo(**base, t=i + 1, quadro=q, dir=TRES_D, destaque=pecas_de("E") if e == "colocaE" else [])
            elif e == "ensaio":
                novo(**base, t=i + 1, quadro=ponte, extra=[[250, 60, 40]], dir=TRES_D)
            else:
                novo(**base, t=None)
            i += 1; continue
        cap = p["cap"]; j = i
        while j < len(P) and P[j]["k"] == "pc" and P[j]["cap"] == cap: j += 1
        grupo = list(range(i, j))
        tam = 99 if cap.startswith("Treliça B") else 8
        for a in range(0, len(grupo), tam):
            ch = grupo[a:a + tam]
            parte = cap.split(" · ")[-1]
            if cap.startswith("Treliça B"):
                txt = f"Faça igual à treliça A: {INSTR.get(parte, '')}"
            elif cap.startswith("Treliça A"):
                txt = INSTR.get(parte, P[ch[0]]["txt"])
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
            titulo = cap + (f" · parte {a // tam + 1}" if len(grupo) > tam else "")
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
    for s in passos:
        s["rotulos"] = pos.get(str(s["n"]), [])
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
