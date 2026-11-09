#!/usr/bin/env python3
"""Gera um modelo OpenSCAD (.scad) de barras retangulares a partir do JSON da skill analise-trelica.

Uso: python3 json2scad.py entrada.json saida.scad [--b 9.5] [--h 2.0] [--largura 80]
Para treliça 2D (dim=2), gera duas treliças laterais afastadas por --largura (mm)
e barras transversais entre nós correspondentes.
"""
import json, math, sys, argparse
p = argparse.ArgumentParser(); p.add_argument("ent"); p.add_argument("sai")
p.add_argument("--b", type=float, default=9.5); p.add_argument("--h", type=float, default=2.0)
p.add_argument("--largura", type=float, default=80.0)
a = p.parse_args(); m = json.load(open(a.ent))
def p3(c, z=0.0): return [c[0], c[1], c[2] if len(c) > 2 else z]
barras = []
planos = [0.0, a.largura] if m.get("dim", 2) == 2 else [0.0]
for z in planos:
    for b in m["barras"]: barras.append((p3(m["nos"][b["i"]], z), p3(m["nos"][b["j"]], z)))
if m.get("dim", 2) == 2:
    for c in m["nos"].values(): barras.append((p3(c, 0.0), p3(c, a.largura)))
out = [f"// gerado por json2scad.py — seção {a.b} x {a.h} mm", f"b={a.b}; h={a.h};",
       "module barra(p1,p2){ d=p2-p1; L=norm(d);",
       "  translate(p1) rotate([0,acos(d[2]/L),atan2(d[1],d[0])])",
       "  translate([-b/2,-h/2,0]) cube([b,h,L]); }"]
for p1, p2 in barras: out.append(f"barra({p1},{p2});")
open(a.sai, "w").write("\n".join(out) + "\n"); print(f"{len(barras)} barras -> {a.sai}")
