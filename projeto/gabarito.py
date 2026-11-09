#!/usr/bin/env python3
"""Gabarito 1:1 (SVG em mm) da vista lateral de UMA treliça, para imprimir e montar por cima."""
import json, os
d = os.path.dirname(__file__)
m = json.load(open(os.path.join(d, "ponte_parker_8x90.json")))
res = {x["id"]: x for x in json.load(open(os.path.join(d, "resultados_ponte.json")))["linhas"]}
MX, MY, W = 20, 20, 8.4
xs = [c[0] for c in m["nos"].values()]; ys = [c[1] for c in m["nos"].values()]
larg, alt = max(xs) + 2 * MX, max(ys) + 2 * MY + 30
Y = lambda y: max(ys) + MY - y
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{larg}mm" height="{alt}mm" viewBox="0 0 {larg} {alt}" font-family="Arial">',
     f'<rect width="{larg}" height="{alt}" fill="white"/>']
for b in m["barras"]:
    a, c = m["nos"][b["i"]], m["nos"][b["j"]]; r = res[b["id"]]
    cor = "#2563eb" if r["N"] > 1e-6 else "#dc2626" if r["N"] < -1e-6 else "#6b7280"
    s.append(f'<line x1="{a[0]+MX}" y1="{Y(a[1])}" x2="{c[0]+MX}" y2="{Y(c[1])}" stroke="{cor}" stroke-opacity="0.35" stroke-width="{W}" stroke-linecap="round"/>')
    s.append(f'<line x1="{a[0]+MX}" y1="{Y(a[1])}" x2="{c[0]+MX}" y2="{Y(c[1])}" stroke="black" stroke-width="0.3"/>')
    mx, my = (a[0] + c[0]) / 2 + MX, (Y(a[1]) + Y(c[1])) / 2
    s.append(f'<text x="{mx}" y="{my-1}" font-size="3" text-anchor="middle">{b["id"]} · {r["n"]}c · {r["L_mm"]:.1f}</text>')
for k, c in m["nos"].items():
    s.append(f'<circle cx="{c[0]+MX}" cy="{Y(c[1])}" r="1.2" fill="black"/><text x="{c[0]+MX+2}" y="{Y(c[1])+5}" font-size="3.5">{k}</text>')
s.append(f'<line x1="{MX}" y1="{alt-15}" x2="{MX+100}" y2="{alt-15}" stroke="black" stroke-width="0.5"/>'
         f'<text x="{MX}" y="{alt-9}" font-size="4">Régua de conferência: esta linha deve medir 100 mm na impressão (escala 1:1). Vão 500 mm, h 90 mm. c = camadas.</text>')
s.append("</svg>")
open(os.path.join(d, "gabarito_lateral_1-1.svg"), "w").write("\n".join(s)); print("ok", larg, "x", alt, "mm")
