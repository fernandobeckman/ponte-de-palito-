#!/usr/bin/env python3
"""Gabarito em tamanho real (1:1) de uma treliça da ponte UCB, dividido em folhas A4 deitadas para emendar com fita.
Desenha o contorno de cada peça da camada 1 (com o número), as chapas da face de baixo (tracejadas) e os eixos.
Lê projeto/montagem.json e grava projeto/manual/gabarito_trelica_1-1.pdf."""
import json, os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black

D = os.path.dirname(os.path.abspath(__file__))
dados = json.load(open(os.path.join(D, "montagem.json")))
P = dados["passos"]; nos = dados["nos"]; barras = dados["barras"]
pecasA = [p for p in P if p["k"] == "pc" and p["g"] == "A"]
L1 = [p for p in pecasA if "camada 1" in p["cap"]]
F1 = [p for p in pecasA if "face de baixo" in p["cap"]]
PW, PH = landscape(A4)
M = 10 * mm                                  # margem
UW = PW - 2 * M                              # largura útil por folha (mm de desenho = mm reais)
X0, X1, Y0, Y1 = -140.0, 940.0, -25.0, 130.0 # janela do desenho (mm)
SOBRE = 10.0                                 # sobreposição entre folhas (mm)
passo = UW / mm - SOBRE
folhas = []
x = X0
while x < X1: folhas.append(x); x += passo
OUT = os.path.join(D, "manual", "gabarito_trelica_1-1.pdf")
c = canvas.Canvas(OUT, pagesize=landscape(A4)); c.setTitle("Gabarito 1:1 — treliça da ponte UCB")
for n, xa in enumerate(folhas):
    ox = M - xa * mm; oy = M + 18 * mm - Y0 * mm      # origem do desenho na página
    T = lambda x, y: (ox + x * mm, oy + y * mm)
    c.saveState()
    p = c.beginPath(); p.rect(M, M, UW, PH - 2 * M); c.clipPath(p, stroke=0)
    # eixos das barras
    c.setStrokeColor(HexColor("#9aa5a1")); c.setLineWidth(.4); c.setDash(4, 3)
    for i, j in barras:
        a, b = nos[i], nos[j]; c.line(*T(*a), *T(*b))
    c.setDash()
    # chapas da face de baixo (tracejado) e peças da camada 1 (contorno cheio com número)
    for lst, cor, dash, larg in ((F1, "#8a5cb8", (2, 2), .5), (L1, "#1b211e", None, .8)):
        c.setStrokeColor(HexColor(cor)); c.setLineWidth(larg)
        if dash: c.setDash(*dash)
        for pc in lst:
            pts = pc["poly"]; path = c.beginPath(); path.moveTo(*T(*pts[0]))
            for q in pts[1:]: path.lineTo(*T(*q))
            path.close(); c.drawPath(path, stroke=1, fill=0)
        c.setDash()
    c.setFillColor(black); c.setFont("Helvetica-Bold", 6.5)
    for pc in L1:
        cx = sum(q[0] for q in pc["poly"]) / len(pc["poly"]); cy = sum(q[1] for q in pc["poly"]) / len(pc["poly"])
        c.drawCentredString(*T(cx, cy - 1), f"{pc['num']} {pc['cod']}")
    c.setFont("Helvetica", 7); c.setFillColor(HexColor("#555555"))
    for k, (x_, y_) in nos.items(): c.drawString(*T(x_ + 5, y_ + (6 if k.startswith("t") else -10)), k)
    # marcas dos apoios (bordas dos blocos)
    c.setStrokeColor(HexColor("#c0392b")); c.setLineWidth(1)
    for xs in (0, 800): c.line(*T(xs, -22), *T(xs, -12))
    c.setFont("Helvetica-Bold", 7); c.setFillColor(HexColor("#c0392b"))
    c.drawString(*T(3, -22), "borda do bloco de apoio"); c.drawString(*T(803, -22), "borda do bloco de apoio")
    c.restoreState()
    # moldura, régua e instruções
    c.setStrokeColor(black); c.setLineWidth(.3); c.rect(M, M, UW, PH - 2 * M)
    c.setFont("Helvetica-Bold", 11); c.drawString(M + 4, PH - M - 14, f"Gabarito 1:1 — treliça (lado) · folha {n+1} de {len(folhas)}")
    c.setFont("Helvetica", 8)
    c.drawString(M + 4, PH - M - 26, "Imprima em 100% (tamanho real). Emende as folhas sobrepondo a faixa cinza da borda direita sobre a próxima folha, alinhando as linhas.")
    c.drawString(M + 4, PH - M - 37, "Contorno cheio = peça da camada 1 (número e código). Tracejado roxo = chapa da face de baixo. Faça as duas treliças sobre o mesmo gabarito.")
    c.setFillColor(HexColor("#e6e6e6")); c.rect(PW - M - SOBRE * mm, M, SOBRE * mm, PH - 2 * M, fill=1, stroke=0); c.setFillColor(black)
    c.setLineWidth(.6); c.line(M + 6 * mm, M + 8 * mm, M + 106 * mm, M + 8 * mm)
    for k in range(0, 101, 10): c.line(M + (6 + k) * mm, M + 8 * mm, M + (6 + k) * mm, M + (10 if k % 50 else 12) * mm)
    c.setFont("Helvetica", 7); c.drawString(M + 6 * mm, M + 3.5 * mm, "Esta régua tem de medir exatamente 100 mm.")
    c.showPage()
c.save(); print(OUT, len(folhas), "folhas")
