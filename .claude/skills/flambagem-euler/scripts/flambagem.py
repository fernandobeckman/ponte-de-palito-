#!/usr/bin/env python3
"""Carga crítica de Euler e esmagamento de barras de palito.

Uso: python3 flambagem.py --b 9.5 --h 2.0 --L 100 --E 10000 --fc 40 [--n 2] [--K 1.0] [--N 1500]
 b, h  : seção de UM palito (mm); h = espessura (direção em que os palitos são empilhados)
 n     : nº de palitos colados empilhados na direção de h (seção composta b × n·h, assume colagem perfeita)
 L     : comprimento entre nós (mm); K: coef. de flambagem (1.0 nós rotulados)
 E     : módulo de elasticidade paralelo às fibras (MPa)
 fc    : resistência à compressão paralela às fibras (MPa)
 N     : esforço de compressão atuante (N), opcional, para calcular o fator de segurança
"""
import argparse, math
p = argparse.ArgumentParser()
for a, d in [("b", 9.5), ("h", 2.0), ("L", 100.0), ("E", 10000.0), ("fc", 40.0), ("K", 1.0), ("N", 0.0)]:
    p.add_argument("--" + a, type=float, default=d)
p.add_argument("--n", type=int, default=1)
a = p.parse_args()
B, H = a.b, a.n * a.h
A = B * H
I_fraco = B * H**3 / 12      # flexão em torno do eixo paralelo a b
I_forte = H * B**3 / 12
Le = a.K * a.L
P_fraco = math.pi**2 * a.E * I_fraco / Le**2
P_forte = math.pi**2 * a.E * I_forte / Le**2
P_esm = a.fc * A
P_res = min(P_fraco, P_forte, P_esm)
lam = Le / math.sqrt(min(I_fraco, I_forte) / A)
modo = {P_fraco: "flambagem eixo fraco", P_forte: "flambagem eixo forte", P_esm: "esmagamento"}[P_res]
print(f"seção {B:.2f} x {H:.2f} mm, A = {A:.2f} mm², esbeltez λ = {lam:.0f}")
print(f"P_cr eixo fraco = {P_fraco:.1f} N | eixo forte = {P_forte:.1f} N | esmagamento = {P_esm:.1f} N")
print(f"resistência governante = {P_res:.1f} N ({modo})")
if a.N > 0:
    print(f"fator de segurança = {P_res / a.N:.2f}  ({'OK' if P_res / a.N >= 1.5 else 'INSUFICIENTE (< 1,5)'})")
if lam < 30:
    print("aviso: λ < 30 — Euler não governa, prevalece esmagamento; considere teste experimental.")
