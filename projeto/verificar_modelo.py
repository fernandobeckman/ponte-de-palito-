#!/usr/bin/env python3
"""Confere o modelo físico (projeto/montagem.json) contra o regulamento e procura peças que se atravessam.

1. Caixa envolvente da ponte pronta (sem os espaçadores provisórios) contra docs/requisitos.md:
   comprimento 1000-1100 mm, largura 200-250 mm, altura até 300 mm.
2. Simetria: o prolongamento além de cada apoio tem de ser igual dos dois lados.
3. Colisões: amostra pontos no interior de cada peça (0,3 mm para dentro das bordas) e verifica se algum
   cai dentro de outra peça. Peças que só se encostam (face com face, borda com borda) não contam.
Sai com código 1 se alguma verificação falhar.
"""
import json, os, sys, math
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
dados = json.load(open(os.path.join(D, "montagem.json")))
C = dados["const"]
T = C["T"]
MARGEM = 0.3

def quadro(p):
    """(origem, u, v, n) no mundo. Treliças: x ao longo do vão, y para cima, z na largura."""
    if p["g"] in ("A", "B"):
        z = C["ZA"] if p["g"] == "A" else C["ZB"]
        return np.array([0.0, C["Y0"], z]), np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])
    fr = p["fr"]
    return tuple(np.array(fr[k], float) for k in ("o", "u", "v", "n"))

def dentro_poly(px, py, poly, margem):
    """Ponto no polígono convexo (sentido qualquer) a pelo menos `margem` das bordas."""
    n = len(poly); s = 0.0
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]; s += x1 * y2 - x2 * y1
    sg = 1.0 if s > 0 else -1.0
    ok = np.ones_like(px, dtype=bool)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 1e-9: continue
        dist = sg * ((x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)) / L
        ok &= dist > margem
    return ok

pecas = [p for p in dados["passos"] if p["k"] == "pc"]
info = []
for p in pecas:
    o, u, v, n = quadro(p)
    poly = p["poly"]; z0 = p["z0"]
    xs = [q[0] for q in poly]; ys = [q[1] for q in poly]
    gx, gy = np.meshgrid(np.arange(min(xs), max(xs), 0.7) + 0.35, np.arange(min(ys), max(ys), 0.7) + 0.35)
    gx, gy = gx.ravel(), gy.ravel()
    m = dentro_poly(gx, gy, poly, MARGEM); gx, gy = gx[m], gy[m]
    pts = []
    for zz in (z0 + 0.5, z0 + 1.5):
        pts.append(o + np.outer(gx, u) + np.outer(gy, v) + zz * n)
    pts = np.vstack(pts) if len(gx) else np.zeros((0, 3))
    cantos = np.array([o + a * u + b * v + zz * n for a, b in poly for zz in (z0, z0 + T)])
    info.append(dict(p=p, o=o, u=u, v=v, n=n, pts=pts, lo=cantos.min(0), hi=cantos.max(0)))

falhas = []
# 1-2. medidas (ponte pronta: sem espaçadores provisórios)
fixas = [i for i in info if i["p"]["g"] != "E"]
lo = np.min([i["lo"] for i in fixas], 0); hi = np.max([i["hi"] for i in fixas], 0)
comp, alt, larg = hi - lo
print(f"Caixa da ponte: x {lo[0]:.5f} a {hi[0]:.5f} | y {lo[1]:.5f} a {hi[1]:.5f} | z {lo[2]:.5f} a {hi[2]:.5f}")
print(f"comprimento {comp:.5f} mm (regra 1000 a 1100) | largura {larg:.5f} mm (200 a 250) | altura {alt:.5f} mm (até 300)")
if not 1000 <= comp <= 1100: falhas.append(f"comprimento {comp:.5f} fora de 1000-1100")
if not 200 <= larg <= 250: falhas.append(f"largura {larg:.5f} fora de 200-250")
if alt > 300: falhas.append(f"altura {alt:.5f} acima de 300")
esq, dir_ = -lo[0], hi[0] - C["VAO"]
print(f"prolongamento além dos apoios: esquerda {esq:.5f} mm, direita {dir_:.5f} mm")
if abs(esq - dir_) > 0.01: falhas.append(f"ponte assimétrica: prolongamento {esq:.5f} x {dir_:.5f}")

# 3. colisões
colisoes = []
N = len(info)
LO = np.array([i["lo"] for i in info]); HI = np.array([i["hi"] for i in info])
for a in range(N):
    A = info[a]
    if not len(A["pts"]): continue
    cand = np.where(np.all(LO <= A["hi"] - 0.2, 1) & np.all(HI >= A["lo"] + 0.2, 1))[0]
    for b in cand:
        if b <= a: continue
        B = info[b]
        # espaçadores provisórios só colidem entre si e com a ponte; ambos são testados normalmente
        rel = A["pts"] - B["o"]
        la, lb, lz = rel @ B["u"], rel @ B["v"], rel @ B["n"]
        z0 = B["p"]["z0"]
        m = (lz > z0 + 0.05) & (lz < z0 + T - 0.05)
        if not m.any(): continue
        m2 = dentro_poly(la[m], lb[m], B["p"]["poly"], 0.05)
        k = int(m2.sum())
        if k:
            colisoes.append((k, A["p"]["num"], A["p"]["nome"], B["p"]["num"], B["p"]["nome"]))
colisoes.sort(reverse=True)
print(f"\n{len(info)} peças conferidas, {len(colisoes)} pares que se atravessam")
for k, na, a, nb, b in colisoes[:40]:
    print(f"  {k:6d} pts  #{na} {a}  x  #{nb} {b}")
if colisoes: falhas.append(f"{len(colisoes)} pares de peças se atravessam")

print("\nRESULTADO:", "OK" if not falhas else "FALHOU -> " + "; ".join(falhas))
sys.exit(1 if falhas else 0)
