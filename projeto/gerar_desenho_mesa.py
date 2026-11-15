#!/usr/bin/env python3
"""Desenho cotado da treliça para riscar direto na mesa (em vez de imprimir o gabarito).
Lê projeto/ponte_ucb.json e projeto/montagem.json; grava projeto/manual/desenho_na_mesa.png."""
import json, os
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
m = json.load(open(os.path.join(D, "ponte_ucb.json")))
C = json.load(open(os.path.join(D, "montagem.json")))["const"]
NOS, W, BAL, VAO, H = m["nos"], C["W"], C["BAL"], C["VAO"], C["H"]
S = 2.0                                   # pixels por mm
MX, MY = 70, 250
X = lambda x: MX + (x + BAL) * S
Y = lambda y: MY + (H - y) * S
LARG, ALT = int((VAO + 2 * BAL) * S + 2 * MX + 190), int(H * S + MY + 330)
img = Image.new("RGB", (LARG, ALT), "white"); g = ImageDraw.Draw(img)
fonte = lambda t, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf", t)
F, FB, FT = fonte(19), fonte(19, True), fonte(30, True)
f1 = lambda v: f"{v:.1f}".replace(".", ",").replace(",0", "")

g.text((MX, 22), "Desenho na mesa: medidas de uma treliça, em mm (as duas treliças usam o mesmo desenho)", font=FT, fill="black")
g.text((MX, 70), "Linhas finas = eixos das barras (risque estas). Faixa cinza = a barra de palito (8,4 mm, 4,2 mm para cada lado do eixo).", font=F, fill="#333")
g.text((MX, 98), "Cubra o desenho com plástico (saco de lixo ou de polietileno) antes de colar: a cola não gruda no plástico.", font=F, fill="#b03a2e")

# faixas das barras
for b in m["barras"]:
    (x1, y1), (x2, y2) = NOS[b["i"]], NOS[b["j"]]
    g.line([(X(x1), Y(y1)), (X(x2), Y(y2))], fill="#e6dccb", width=int(W * S))
g.rectangle([X(-BAL), Y(W / 2), X(VAO + BAL), Y(-W / 2)], fill="#e6dccb")   # banzo inferior inteiro (com os prolongamentos)
# eixos
g.line([(X(-BAL), Y(0)), (X(VAO + BAL), Y(0))], fill="black", width=2)
for b in m["barras"]:
    (x1, y1), (x2, y2) = NOS[b["i"]], NOS[b["j"]]
    g.line([(X(x1), Y(y1)), (X(x2), Y(y2))], fill="black", width=2)
for k, (x, y) in NOS.items():
    g.ellipse([X(x) - 5, Y(y) - 5, X(x) + 5, Y(y) + 5], fill="#c0392b")
    g.text((X(x) + 7, Y(y) + (8 if y == 0 else -30)), k, font=FB, fill="#c0392b")

def cota_h(x1, x2, y, txt, cor="#1f5fa8"):
    g.line([(X(x1), y), (X(x2), y)], fill=cor, width=2)
    for x in (x1, x2): g.line([(X(x), y - 9), (X(x), y + 9)], fill=cor, width=2)
    w = g.textlength(txt, font=F); g.text(((X(x1) + X(x2)) / 2 - w / 2, y - 26), txt, font=F, fill=cor)

def cota_v(x, y1, y2, txt, cor="#1f5fa8"):
    g.line([(x, Y(y1)), (x, Y(y2))], fill=cor, width=2)
    for y in (y1, y2): g.line([(x - 9, Y(y)), (x + 9, Y(y))], fill=cor, width=2)
    g.text((x + 10, (Y(y1) + Y(y2)) / 2 - 10), txt, font=F, fill=cor)

yb = Y(-W / 2) + 55
cota_h(-BAL, 0, yb, f"{f1(BAL)}"); cota_h(VAO, VAO + BAL, yb, f"{f1(BAL)}")
for i in range(8): cota_h(i * 100, (i + 1) * 100, yb, "100")
cota_h(-BAL, VAO + BAL, yb + 70, f"linha de baixo: {f1(VAO + 2 * BAL)} mm (b0 fica a {f1(BAL)} mm da ponta)")
cota_h(0, VAO, yb + 130, f"vão: {f1(VAO)} mm (b0 e b8 ficam na borda dos blocos de apoio)", cor="#555")
cota_h(100, 700, Y(H + W / 2) - 40, "linha de cima: 600 mm, de t1 a t7, exatamente acima de b1 e b7")
cota_v(X(VAO + BAL) + 25, 0, H, "100 mm\n(entre as linhas)")
g.text((MX, ALT - 70), "Confira o esquadro: cada quadrado de 100 × 100 mm tem diagonal de 141,4 mm (meça b1→t2 e t1→b2). "
       "Área ocupada: 1020 × 108,4 mm.", font=F, fill="#333")
OUT = os.path.join(D, "manual", "desenho_na_mesa.png"); img.save(OUT)
print(OUT, img.size)
