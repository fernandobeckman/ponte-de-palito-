#!/usr/bin/env python3
"""Gera site/projeto.html: página do projeto para ver no celular (3D + números + montagem)."""
import json, os
d = os.path.dirname(os.path.abspath(__file__))
m = json.load(open(os.path.join(d, "ponte_parker_8x90.json")))
r = json.load(open(os.path.join(d, "resultados_ponte.json")))
LARG = 80.0
N = {x["id"]: x for x in r["linhas"]}
bars = []
for z in (0.0, LARG):
    for b in m["barras"]:
        a, c = m["nos"][b["i"]], m["nos"][b["j"]]; x = N[b["id"]]
        bars.append({"id": b["id"], "a": [a[0], a[1], z], "b": [c[0], c[1], z], "N": round(x["N"], 5),
                     "Nd": round(x["N_desloc_max"], 5), "n": x["n"], "L": round(x["L_mm"], 5)})
for k, c in m["nos"].items():
    if k.startswith("b"):
        bars.append({"id": "transversina " + k, "a": [c[0], 0, 0], "b": [c[0], 0, LARG], "N": None})
    elif k.startswith("t"):
        bars.append({"id": "escora " + k, "a": [c[0], c[1], 0], "b": [c[0], c[1], LARG], "N": None})
# vista lateral (SVG) de uma treliça
def Y(y): return 100 - y
svg = []
for b in m["barras"]:
    a, c = m["nos"][b["i"]], m["nos"][b["j"]]; x = N[b["id"]]["N"]
    cls = "t" if x > 1e-6 else "c" if x < -1e-6 else "z"
    svg.append(f'<line class="{cls}" x1="{a[0]+10}" y1="{Y(a[1])}" x2="{c[0]+10}" y2="{Y(c[1])}"/>')
for k, c in m["nos"].items():
    svg.append(f'<circle cx="{c[0]+10}" cy="{Y(c[1])}" r="2.2"/>')
svg = "".join(svg)
f5 = lambda v: f"{v:.5f}".replace(".", ",")
rows = "".join(
    f'<tr><td>{n}</td><td class="num">{L}</td><td class="num {cl}">{Nc}</td><td class="num">{Nd}</td><td class="num">{cam}</td><td class="num">{fs}</td><td>{modo}</td></tr>'
    for n, L, cl, Nc, Nd, cam, fs, modo in [
        ("Banzo inferior", "62,50000", "tr", "+306,45781", "+383,07227", "3 (2 efet.)", "5,76158", "tração"),
        ("Banzo superior", "66,42665", "co", "−325,71146", "−407,13932", "3 (2 efet.)", "<b>2,26124</b>", "flambagem"),
        ("Montante central", "90,00000", "tr", "+220,64962", "+165,48722", "3", "12,00328", "tração"),
        ("Diagonais centrais", "91,99185", "", "0,00000", "−225,53296", "3", "5,74685*", "flambagem"),
        ("Montantes b3-t3, b5-t5", "67,50000", "", "0,00000", "+220,64962", "3", "12,00328*", "tração"),
        ("Demais barras da alma", "22,5 a 77,0", "", "0,00000", "0,00000", "3", "—", "travamento"),
    ])
html = open(os.path.join(d, "pagina_modelo.html")).read()
html = (html.replace("__BARS__", json.dumps(bars)).replace("__SVG__", svg).replace("__ROWS__", rows)
        .replace("__FS__", f5(r["fs_min"])).replace("__FLECHA__", f5(r["flecha_mm"]))
        .replace("__RUPT__", f5(r["fs_min"] * 45)).replace("__PALITOS__", str(r["total_palitos"])))
os.makedirs(os.path.join(d, "..", "site"), exist_ok=True)
open(os.path.join(d, "..", "site", "projeto.html"), "w").write(html)
print("site/projeto.html", len(html), "bytes")
