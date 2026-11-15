#!/usr/bin/env python3
"""Lista de montagem em PDF: só o necessário para montar com as peças já cortadas e numeradas.
Para cada passo da aba Manual: número da peça, código, tamanho e onde ela entra.
Lê projeto/montagem.json e projeto/manual/plano.json; grava projeto/manual/lista_de_montagem.pdf."""
import json, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import simpleSplit

D = os.path.dirname(os.path.abspath(__file__))
dados = json.load(open(os.path.join(D, "montagem.json")))
P, tipos = dados["passos"], {t["cod"]: t for t in dados["tipos"]}
plano = json.load(open(os.path.join(D, "manual", "plano.json")))
OUT = os.path.join(D, "manual", "lista_de_montagem.pdf")
PW, PH = A4
M = 12 * mm
COR = {"banzo": "#b5651d", "diagonal": "#2a66ad", "montante": "#2f7a4f", "chapa": "#8a5cb8", "transversina": "#c0392b",
       "escora": "#d48a00", "contravento": "#16838f", "consolo": "#6b6b6b", "espacador": "#4f86c6"}
f1 = lambda v: f"{v:.1f}".replace(".", ",")
pecas = [p for p in P if p["k"] == "pc"]
CURTO = {"Diagonal de contraventamento": "Contravento", "Espaçador provisório": "Espaçador (provisório)"}

def faixas(nums):
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}–{nums[j]}"); i = j + 1
    return ", ".join(out)

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Lista de montagem — Ponte UCB 2026/2 (Pratt 80 cm)"); c.setAuthor("ponte-de-palito-")
pag = [0]
def nova(titulo):
    if pag[0]: c.showPage()
    pag[0] += 1
    c.setFillColor(black); c.setFont("Helvetica-Bold", 12.5); c.drawString(M, PH - M - 4, titulo)
    c.setFont("Helvetica", 7.5); c.drawRightString(PW - M, PH - M - 4, f"Ponte UCB 2026/2 · lista de montagem · página {pag[0]}")
    c.setLineWidth(.4); c.line(M, PH - M - 8, PW - M, PH - M - 8)
    return PH - M - 22

def chip(x, y, cod, w=22):
    cat = tipos[cod]["cat"]
    c.setFillColor(HexColor(COR[cat])); c.roundRect(x, y - 2.2, w, 10, 2.5, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 7.4); c.drawCentredString(x + w / 2, y + .4, cod); c.setFillColor(black)

# ---------------- página 1: como usar + separar por código
y = nova("Lista de montagem: o que entra em cada passo")
txt = ("As peças já estão cortadas e numeradas. Esta lista diz, passo a passo, quais peças entram: número (escrito a lápis na peça), "
       "código (o nome do formato, igual ao do manual de corte) e tamanho. Os passos são os mesmos da aba Manual do site, "
       "onde cada passo tem imagem. Os números e códigos não mudaram desde o manual de corte usado para cortar.")
c.setFont("Helvetica", 9)
for ln in simpleSplit(txt, "Helvetica", 9, PW - 2 * M): c.drawString(M, y, ln); y -= 11.5
y -= 8
c.setFont("Helvetica-Bold", 10); c.drawString(M, y, "Antes de começar: separe as peças por código (confira a quantidade de cada montinho)"); y -= 14
c.setFont("Helvetica-Bold", 7); c.setFillColor(HexColor("#555555"))
cols = [M, M + 30, M + 100, M + 140, M + 162]
for x, h in zip(cols, ("código", "peça", "tamanho", "qtd", "números")): c.drawString(x, y, h)
c.setFillColor(black); y -= 11
for t in sorted(tipos.values(), key=lambda t: (t["cod"][0], int(t["cod"][1:]))):
    if y < M + 12: y = nova("Separe por código (continuação)")
    chip(cols[0], y, t["cod"])
    c.setFont("Helvetica", 7.6); c.drawString(cols[1], y, CURTO.get(t["nome_cat"], t["nome_cat"])[:22])
    c.drawString(cols[2], y, f"{f1(t['L'])} mm"); c.drawString(cols[3], y, str(t["qtd"]))
    c.setFont("Helvetica", 6.6); fx = faixas(t["nums"])
    linhas = simpleSplit(fx, "Helvetica", 6.6, PW - M - cols[4])
    for k, ln in enumerate(linhas[:2]): c.drawString(cols[4], y - 7.5 * k, ln + ("…" if k == 1 and len(linhas) > 2 else ""))
    y -= 11.5 + 7.5 * (min(2, len(linhas)) - 1)
c.setFont("Helvetica", 7.6); c.setFillColor(HexColor("#555555"))
y -= 4; c.drawString(M, y, f"Total: {len(pecas)} peças ({sum(1 for p in pecas if p['g'] == 'E')} são dos espaçadores provisórios, que saem no fim)."); c.setFillColor(black)

# ---------------- passos
y = nova("Passo a passo")
LH = 9.6
for s in plano:
    texto = s["texto"]
    for a, b in (("Corte as chapas e coloque", "Coloque as chapas"), ("Corte e coloque", "Coloque"), ("Corte e cole", "Cole")):
        texto = texto.replace(a, b)
    linhas_txt = simpleSplit(texto, "Helvetica", 8, PW - 2 * M - 4)
    precisa = 16 + len(linhas_txt) * 10 + (LH * 2 if s["pecas"] else 0)
    if y - precisa < M: y = nova("Passo a passo (continuação)")
    c.setFillColor(HexColor("#f2e6d2")); c.rect(M, y - 4, PW - 2 * M, 14, fill=1, stroke=0); c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9.2); c.drawString(M + 3, y, f"Passo {s['n']}  ·  {s['titulo']}")
    if s["pecas"]:
        c.setFont("Helvetica", 7.4); c.drawRightString(PW - M - 3, y, f"peças {s.get('faixa', '')}  ({len(s['pecas'])})")
    y -= 15
    c.setFont("Helvetica", 8)
    for ln in linhas_txt: c.drawString(M + 3, y, ln); y -= 10
    for k in s["pecas"]:
        if y < M + 4:
            y = nova("Passo a passo (continuação)")
            c.setFont("Helvetica-Bold", 8); c.drawString(M + 3, y, f"Passo {s['n']} (continuação)"); y -= 12
        p = P[k]
        c.setFont("Helvetica-Bold", 8); c.drawRightString(M + 24, y, str(p["num"]))
        chip(M + 30, y, p["cod"])
        c.setFont("Helvetica", 8); c.drawString(M + 58, y, f"{f1(tipos[p['cod']]['L'])} mm")
        c.setFont("Helvetica", 7.8); c.drawString(M + 104, y, p["nome"][:92])
        y -= LH
    y -= 6
c.save()
print(OUT, pag[0], "páginas")
