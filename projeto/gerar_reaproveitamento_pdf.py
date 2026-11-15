#!/usr/bin/env python3
"""Plano de reaproveitamento em PDF: o que fazer com cada montinho de peças da ponte antiga e o que cortar de palito novo.
Lê projeto/manual/reaproveitamento.json (reaproveitamento.py), projeto/montagem.json e projeto/manual/parker_montagem.json.
Grava projeto/manual/plano_reaproveitamento.pdf."""
import json, math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import simpleSplit

D = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(D, "manual", "reaproveitamento.json")))
NOV = json.load(open(os.path.join(D, "montagem.json")))
ANT = {t["cod"]: t for t in json.load(open(os.path.join(D, "manual", "parker_montagem.json")))["tipos"]}
TN = {t["cod"]: t for t in NOV["tipos"]}
OUT = os.path.join(D, "manual", "plano_reaproveitamento.pdf")
PW, PH = A4
M = 13 * mm
COR = {"banzo": "#b5651d", "diagonal": "#2a66ad", "montante": "#2f7a4f", "chapa": "#8a5cb8", "transversina": "#c0392b",
       "escora": "#d48a00", "contravento": "#16838f", "consolo": "#6b6b6b", "espacador": "#4f86c6"}
f1 = lambda v: f"{v:.1f}".replace(".", ",")
ordem = lambda c: ("BDMCTEXKP".index(c[0]), int(c[1:]))

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Plano de reaproveitamento — peças da ponte antiga na ponte UCB"); c.setAuthor("ponte-de-palito-")
pag = [0]
def nova(t):
    if pag[0]: c.showPage()
    pag[0] += 1
    c.setFillColor(black); c.setFont("Helvetica-Bold", 13); c.drawString(M, PH - M - 4, t)
    c.setFont("Helvetica", 7.5); c.drawRightString(PW - M, PH - M - 4, f"Ponte UCB 2026/2 · reaproveitamento · página {pag[0]}")
    c.setLineWidth(.4); c.line(M, PH - M - 8, PW - M, PH - M - 8)
    return PH - M - 24

def chip(x, y, cod, cat, antigo=False):
    w = 26
    if antigo:
        c.setStrokeColor(HexColor(COR[cat])); c.setFillColor(white); c.setLineWidth(1.2); c.roundRect(x, y - 2.5, w, 11, 3, fill=1, stroke=1)
        c.setFillColor(HexColor(COR[cat]))
    else:
        c.setFillColor(HexColor(COR[cat])); c.roundRect(x, y - 2.5, w, 11, 3, fill=1, stroke=0); c.setFillColor(white)
    c.setFont("Helvetica-Bold", 8); c.drawCentredString(x + w / 2, y + .3, cod); c.setFillColor(black)

def par(y, txt, fonte="Helvetica", tam=9, larg=None):
    c.setFont(fonte, tam)
    for ln in simpleSplit(txt, fonte, tam, larg or PW - 2 * M): c.drawString(M, y, ln); y -= tam + 2.6
    return y

tot = len(R["destino"]); de_ant = sum(1 for d in R["destino"].values() if d["de"] == "antiga")
sem = sum(1 for d in R["destino"].values() if d["de"] == "antiga" and not d["recorte"])
pal = R["palitos_novos"]; comprar = math.ceil(pal * 1.15)
y = nova("Plano de reaproveitamento das peças da ponte antiga")
y = par(y, f"Vocês já cortaram as peças da ponte antiga (Parker, 50 cm). {de_ant} das {tot} peças da ponte nova saem delas: "
           f"{sem} sem nenhum corte e {de_ant - sem} recortadas. As outras {tot - de_ant} saem de {pal} palitos novos "
           f"(sem reaproveitar seriam {NOV['resumo']['palitos_ponte'] + NOV['resumo']['palitos_esp']}). Com 15% de perda, tenham {comprar} palitos novos.")
y -= 4
y = par(y, "Os códigos que já estão nas peças continuam valendo: peça da ponte nova com o mesmo formato de uma antiga ficou com o "
           "mesmo código (B1, B4, B11, C6, K1). Os códigos que não existiam na ponte antiga são novos (B17 em diante, C9 em diante, "
           "D4, M5, T3, E2, X2, P2...). Chip com contorno = código antigo; chip cheio = código da ponte nova.", tam=8.6)
y -= 6
y = par(y, "Ordem: (1) separe os montinhos antigos; (2) faça os recortes da tabela 2 usando o molde do código novo no manual de corte; "
           "(3) corte o que falta de palito novo (tabela 3); (4) junte tudo em montinhos pelo código NOVO e monte pela lista de montagem.",
        "Helvetica-Bold", 8.8)
y -= 8

# 1) sem recorte
c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "1. Peças antigas que entram sem recortar"); y -= 15
c.setFont("Helvetica-Bold", 7.2); c.setFillColor(HexColor("#555555"))
for x, h in ((M, "antiga"), (M + 34, "tamanho"), (M + 74, "usar"), (M + 100, "como"), (M + 134, "observação")): c.drawString(x, y, h)
c.setFillColor(black); y -= 12
for m in sorted(R["montinhos"], key=lambda m: ordem(m["cod_ant"])):
    for v in m["vira"]:
        if not v["sem_corte"]: continue
        cn = v["novos"][0]; ta, tn = ANT[m["cod_ant"]], TN[cn]
        chip(M, y, m["cod_ant"], ta["cat"], True); c.setFont("Helvetica", 8.4)
        c.drawString(M + 34, y, f"{f1(ta['L'])} mm"); c.drawString(M + 74, y, f"{v['qtd']}")
        chip(M + 100, y, cn, tn["cat"])
        obs = "mesmo código, é só usar" if cn == m["cod_ant"] else f"é igual à {cn} nova: escreva {cn} na peça"
        if abs(ta["L"] - tn["L"]) > .05: obs += f" (lixe para {f1(tn['L'])} mm)"
        c.drawString(M + 134, y, obs); y -= 13
y -= 8

# 2) recortar
c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "2. Peças antigas para recortar (use o molde do código novo)"); y -= 15
c.setFont("Helvetica-Bold", 7.2); c.setFillColor(HexColor("#555555"))
for x, h in ((M, "antiga"), (M + 34, "tamanho"), (M + 74, "qtd"), (M + 100, "vira"), (M + 134, "novo tamanho e pontas")): c.drawString(x, y, h)
c.setFillColor(black); y -= 12
for m in sorted(R["montinhos"], key=lambda m: ordem(m["cod_ant"])):
    for v in m["vira"]:
        if v["sem_corte"]: continue
        if y < M + 20: y = nova("2. Peças antigas para recortar (continuação)")
        ta = ANT[m["cod_ant"]]
        chip(M, y, m["cod_ant"], ta["cat"], True); c.setFont("Helvetica", 8.4)
        c.drawString(M + 34, y, f"{f1(ta['L'])} mm"); c.drawString(M + 74, y, f"{v['qtd']}")
        x = M + 100
        for k, cn in enumerate(v["novos"]):
            chip(x, y, cn, TN[cn]["cat"]); x += 30
        tn = TN[v["novos"][0]]
        c.setFont("Helvetica", 8); c.drawString(M + 134, y, f"{f1(tn['L'])} mm · {tn['txt_esq']} | {tn['txt_dir']}"[:80]); y -= 13
y -= 8

# 3) palito novo
if y < M + 120: y = nova("3. Cortar de palito novo")
else: c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "3. Cortar de palito novo"); y -= 15
c.setFont("Helvetica-Bold", 7.2); c.setFillColor(HexColor("#555555"))
cols = [M, M + 34, M + 74, M + 100]
for x, h in zip(cols, ("código", "tamanho", "qtd", "pontas")): c.drawString(x, y, h)
c.drawString(M + 92 * mm, y, "código"); c.drawString(M + 92 * mm + 34, y, "tamanho"); c.drawString(M + 92 * mm + 74, y, "qtd"); c.drawString(M + 92 * mm + 100, y, "pontas")
c.setFillColor(black); y -= 12
itens = sorted(R["novas_de_palito"].items(), key=lambda t: ordem(t[0]))
meio = (len(itens) + 1) // 2
y0 = y
for k, (cn, q) in enumerate(itens):
    x0 = M if k < meio else M + 92 * mm
    yy = y0 - 13 * (k if k < meio else k - meio)
    tn = TN[cn]
    chip(x0, yy, cn, tn["cat"]); c.setFont("Helvetica", 8.4)
    c.drawString(x0 + 34, yy, f"{f1(tn['L'])} mm"); c.drawString(x0 + 74, yy, str(q))
    c.setFont("Helvetica", 6.8); c.drawString(x0 + 100, yy, ("retas" if tn["txt_esq"] == tn["txt_dir"] == "reta (90°)" else "cortes inclinados: ver molde")[:30])
y = y0 - 13 * meio - 6
c.setFont("Helvetica-Bold", 9); c.drawString(M, y, f"Total: {sum(q for _, q in itens)} peças de {pal} palitos novos (tenham {comprar} com a perda)."); y -= 18

# 4) sobras
sob = [m for m in R["montinhos"] if m["sobra"]]
if sob:
    if y < M + 40: y = nova("4. Peças antigas que sobram")
    c.setFont("Helvetica-Bold", 11); c.drawString(M, y, "4. Peças antigas que sobram (não entram na ponte nova)"); y -= 14
    c.setFont("Helvetica", 8.4)
    txt = ", ".join(f"{m['cod_ant']} ({f1(m['L_ant'])} mm) × {m['sobra']}" for m in sorted(sob, key=lambda m: ordem(m["cod_ant"])))
    y = par(y, txt + ". Guardem para testes de cola ou para repor alguma peça que quebrar.", tam=8.4)
c.save()
print(OUT, pag[0], "páginas")
