#!/usr/bin/env python3
"""Manual de corte em PDF (estilo LEGO): moldes em tamanho real de cada tipo de peça + índice numerado.
Lê projeto/montagem.json (gerado por gerar_montagem.py) e grava projeto/manual/manual_de_corte.pdf."""
import json, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white

D = os.path.dirname(os.path.abspath(__file__))
dados = json.load(open(os.path.join(D, "montagem.json")))
tipos, passos = dados["tipos"], dados["passos"]
pecas = [p for p in passos if p["k"] == "pc"]
OUT = os.path.join(D, "manual", "manual_de_corte.pdf"); os.makedirs(os.path.dirname(OUT), exist_ok=True)
PW, PH = A4
MARG = 12 * mm
COR = {"banzo": "#b5651d", "diagonal": "#2a66ad", "montante": "#2f7a4f", "chapa": "#8a5cb8", "transversina": "#c0392b",
       "escora": "#d48a00", "contravento": "#16838f", "consolo": "#6b6b6b", "espacador": "#4f86c6"}
f1 = lambda v: f"{v:.1f}".replace(".", ",")

def faixas(nums):
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}–{nums[j]}"); i = j + 1
    return ", ".join(out)

def regua(c, x, y):
    c.setLineWidth(.6); c.setStrokeColor(black)
    c.line(x, y, x + 100 * mm, y)
    for k in range(0, 101, 10):
        c.line(x + k * mm, y, x + k * mm, y + (3 if k % 50 else 5) * mm)
    c.setFont("Helvetica", 7); c.drawString(x, y - 9, "Régua de conferência: esta linha deve medir exatamente 100 mm. Se não medir, imprima em 100% (tamanho real).")

def cabecalho(c, titulo, pag):
    c.setFillColor(black); c.setFont("Helvetica-Bold", 13); c.drawString(MARG, PH - MARG - 4, titulo)
    c.setFont("Helvetica", 8); c.drawRightString(PW - MARG, PH - MARG - 4, f"Ponte Parker 8×90 · manual de corte · página {pag}")
    c.setLineWidth(.4); c.line(MARG, PH - MARG - 9, PW - MARG, PH - MARG - 9)

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Manual de corte — Ponte Parker 8x90"); c.setAuthor("ponte-de-palito-")
pag = 1
# ---------------- capa / como usar
cabecalho(c, "Manual de corte — como usar", pag)
y = PH - MARG - 26
linhas = [
    ("Cada formato de peça tem um CÓDIGO", "letra da família + número (ex.: B1 = banzo de 100 mm com cortes retos)."),
    ("Cada peça da ponte tem um NÚMERO", f"de 1 a {len(pecas)}, na ordem de montagem. Escreva o número a lápis na peça logo depois de cortar."),
    ("Moldes em tamanho real", "imprima em 100% (sem ajustar à página) e confira a régua de 100 mm. Apoie o palito sobre o molde e corte nas linhas."),
    ("Ângulo do corte", "medido entre a linha de corte e a borda comprida do palito. 90° = corte reto. 'Em bico' = ponta com dois cortes."),
    ("Borda A e borda B", "comprimento de cada lado comprido depois de cortado. Marque as duas medidas e ligue os pontos com a régua."),
    ("Palito", "8,4 mm × 2,0 mm × 110 mm; parte reta útil de 101,6 mm (sem as pontas arredondadas)."),
    ("Peças iguais", "têm o mesmo código: corte todas de uma vez, separe em montinhos por código (como os saquinhos do LEGO)."),
]
from reportlab.lib.utils import simpleSplit
COL1, COL2 = 52 * mm, PW - 2 * MARG - 56 * mm
for t1, t2 in linhas:
    l1 = simpleSplit(t1, "Helvetica-Bold", 9.5, COL1); l2 = simpleSplit(t2, "Helvetica", 9.5, COL2)
    c.setFont("Helvetica-Bold", 9.5)
    for k, ln in enumerate(l1): c.drawString(MARG, y - k * 11.5, ln)
    c.setFont("Helvetica", 9.5)
    for k, ln in enumerate(l2): c.drawString(MARG + 56 * mm, y - k * 11.5, ln)
    y -= 11.5 * max(len(l1), len(l2)) + 7
y -= 6
c.setFont("Helvetica-Bold", 10); c.drawString(MARG, y, "Famílias de peças"); y -= 14
fams = {}
for t in tipos: fams.setdefault(t["cat"], [t["nome_cat"], 0, 0]); fams[t["cat"]][1] += 1; fams[t["cat"]][2] += t["qtd"]
for cat, (nome, nt, nq) in fams.items():
    c.setFillColor(HexColor(COR[cat])); c.rect(MARG, y - 2, 9, 9, fill=1, stroke=0); c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9.5); c.drawString(MARG + 14, y, f"{tipos[[t['cat'] for t in tipos].index(cat)]['cod'][0]}  {nome}")
    c.setFont("Helvetica", 9.5); c.drawString(MARG + 70 * mm, y, f"{nt} tipo(s), {nq} peça(s)" + ("  — provisório, não fica na ponte" if cat == "espacador" else ""))
    y -= 14
y -= 8
c.setFont("Helvetica", 9.5)
c.drawString(MARG, y, f"Total: {len(pecas)} peças em {len(tipos)} tipos. Dica: corte primeiro os tipos com mais peças (C6, B1, T2...)."); y -= 26
regua(c, MARG, y)
c.showPage(); pag += 1

# ---------------- moldes 1:1
ALT = 27 * mm               # altura de cada linha
XT = MARG                   # coluna de texto
XD = MARG + 66 * mm         # início do desenho (110 mm cabem até a margem direita)
y = None
def nova_pagina():
    global y, pag
    cabecalho(c, "Moldes em tamanho real (1:1)", pag); y = PH - MARG - 16
for i, t in enumerate(tipos):
    if y is None or y - ALT < MARG + 16:
        if y is not None: regua(c, MARG, MARG + 6); c.showPage(); pag += 1
        nova_pagina()
    top = y
    cor = HexColor(COR[t["cat"]])
    c.setFillColor(cor); c.roundRect(XT, top - 15, 30, 15, 3, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 11); c.drawCentredString(XT + 15, top - 11, t["cod"])
    c.setFillColor(black); c.setFont("Helvetica-Bold", 11); c.drawString(XT + 35, top - 11, f"× {t['qtd']}")
    c.setFont("Helvetica", 7.6)
    c.drawString(XT, top - 25, f"{t['nome_cat']} · comprimento total {f1(t['L'])} mm")
    c.drawString(XT, top - 34, f"Borda A {f1(t['bordaA'])} mm · borda B {f1(t['bordaB'])} mm")
    c.drawString(XT, top - 43, f"Pontas: {t['txt_esq']} | {t['txt_dir']}"[:70])
    c.setFont("Helvetica", 6.6); c.setFillColor(HexColor("#444444"))
    nums = "Nº " + faixas(t["nums"])
    c.drawString(XT, top - 52, nums[:84] + ("…" if len(nums) > 84 else ""))
    c.setFillColor(black)
    # desenho 1:1 (y do contorno centrado; base do desenho no meio da linha)
    cy = top - 30
    p = c.beginPath()
    pts = t["poly"]
    p.moveTo(XD + pts[0][0] * mm, cy + pts[0][1] * mm)
    for x, yy in pts[1:]: p.lineTo(XD + x * mm, cy + yy * mm)
    p.close()
    c.setFillColor(HexColor("#f1e4cf")); c.setStrokeColor(black); c.setLineWidth(.7); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(cor); c.setFont("Helvetica-Bold", 8); c.drawCentredString(XD + t["L"] * mm * .45, cy - 2.6, t["cod"])
    # cota do comprimento total
    c.setStrokeColor(HexColor("#666666")); c.setLineWidth(.35)
    yc = cy + 7.5 * mm
    c.line(XD, yc, XD + t["L"] * mm, yc); c.line(XD, yc - 2, XD, yc + 2); c.line(XD + t["L"] * mm, yc - 2, XD + t["L"] * mm, yc + 2)
    c.setFillColor(HexColor("#444444")); c.setFont("Helvetica", 7); c.drawCentredString(XD + t["L"] * mm / 2, yc + 2, f"{f1(t['L'])} mm")
    c.setFillColor(black)
    c.setStrokeColor(HexColor("#dddddd")); c.line(MARG, top - ALT + 2, PW - MARG, top - ALT + 2); c.setStrokeColor(black)
    y = top - ALT
regua(c, MARG, MARG + 6); c.showPage(); pag += 1

# ---------------- índice numerado (nº -> código e peça)
cabecalho(c, "Índice numerado: número da peça → código", pag)
COLS, LH = 4, 9.6
colw = (PW - 2 * MARG) / COLS
y0 = PH - MARG - 22; col = 0; y = y0
etapa_ant = None
for p in pecas:
    etapa = p["cap"]
    if y < MARG + 10:
        col += 1; y = y0
        if col >= COLS:
            c.showPage(); pag += 1; cabecalho(c, "Índice numerado (continuação)", pag); col = 0; y = y0
    x = MARG + col * colw
    if etapa != etapa_ant:
        c.setFont("Helvetica-Bold", 6.6); c.setFillColor(HexColor("#7a5520")); c.drawString(x, y, etapa[:42]); c.setFillColor(black)
        y -= LH; etapa_ant = etapa
        if y < MARG + 10: continue
    cat = next(t["cat"] for t in tipos if t["cod"] == p["cod"])
    c.setFillColor(HexColor(COR[cat])); c.rect(x, y - 1.5, 5, 6, fill=1, stroke=0); c.setFillColor(black)
    c.setFont("Helvetica-Bold", 7.4); c.drawString(x + 8, y, f"{p['num']:>3}")
    c.setFont("Helvetica", 7.4); c.drawString(x + 26, y, p["cod"])
    y -= LH
c.showPage()
c.save()
print(OUT, pag, "páginas")
