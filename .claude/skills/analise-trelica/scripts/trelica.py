#!/usr/bin/env python3
"""Solver de treliça 2D/3D pelo método da rigidez direta (sem dependências).

Uso: python3 trelica.py entrada.json [--E 10000] [--A 7.0]
Entrada (unidades: mm, N, MPa):
{
  "dim": 2,
  "E": 10000, "A": 7.0,              # padrão para barras (MPa, mm²)
  "nos": {"1": [0,0], "2": [100,0], ...},
  "barras": [{"id":"b1","i":"1","j":"2","A":7.0,"E":10000}, ...],
  "apoios": {"1": [1,1], "5": [0,1]},  # 1 = restrito (x, y[, z])
  "cargas": {"3": [0,-100]}             # N
}
Saída: esforço axial de cada barra (+ tração, - compressão), reações e deslocamentos.
"""
import json, math, sys

def resolver(m):
    dim = m.get("dim", 2)
    nos = list(m["nos"].keys()); idx = {n: k for k, n in enumerate(nos)}
    ndof = dim * len(nos)
    K = [[0.0] * ndof for _ in range(ndof)]
    info = []
    for b in m["barras"]:
        pi, pj = m["nos"][b["i"]], m["nos"][b["j"]]
        d = [pj[k] - pi[k] for k in range(dim)]
        L = math.sqrt(sum(x * x for x in d))
        if L == 0: raise ValueError(f"barra {b['id']} com comprimento zero")
        c = [x / L for x in d]
        EA = b.get("E", m.get("E", 10000)) * b.get("A", m.get("A", 7.0))
        k = EA / L
        dofs = [dim * idx[b["i"]] + a for a in range(dim)] + [dim * idx[b["j"]] + a for a in range(dim)]
        cc = c + [-x for x in c]
        for r in range(2 * dim):
            for s in range(2 * dim):
                K[dofs[r]][dofs[s]] += k * cc[r] * cc[s]
        info.append((b, L, c, EA, dofs))
    F = [0.0] * ndof
    for n, f in m.get("cargas", {}).items():
        for a in range(dim): F[dim * idx[n] + a] += f[a]
    fixos = set()
    for n, r in m.get("apoios", {}).items():
        for a in range(dim):
            if r[a]: fixos.add(dim * idx[n] + a)
    livres = [g for g in range(ndof) if g not in fixos]
    # eliminação de Gauss com pivoteamento parcial
    n = len(livres)
    M = [[K[livres[r]][livres[s]] for s in range(n)] + [F[livres[r]]] for r in range(n)]
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[p][col]) < 1e-9 * max(1.0, max(abs(K[g][g]) for g in range(ndof))):
            raise ValueError("matriz singular: a treliça é um mecanismo ou falta apoio")
        M[col], M[p] = M[p], M[col]
        for r in range(col + 1, n):
            f = M[r][col] / M[col][col]
            for s in range(col, n + 1): M[r][s] -= f * M[col][s]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][s] * x[s] for s in range(r + 1, n))) / M[r][r]
    U = [0.0] * ndof
    for k_, g in enumerate(livres): U[g] = x[k_]
    R = {}
    for g in sorted(fixos):
        R[g] = sum(K[g][s] * U[s] for s in range(ndof)) - F[g]
    barras = []
    for b, L, c, EA, dofs in info:
        du = [U[dofs[dim + a]] - U[dofs[a]] for a in range(dim)]
        N = EA / L * sum(c[a] * du[a] for a in range(dim))
        barras.append({"id": b["id"], "i": b["i"], "j": b["j"], "L_mm": round(L, 2),
                       "N": round(N, 3), "tipo": "tração" if N > 1e-9 else ("compressão" if N < -1e-9 else "nula")})
    reacoes = {}
    for g, v in R.items():
        reacoes.setdefault(nos[g // dim], [0.0] * dim)[g % dim] = round(v, 3)
    desloc = {nos[i]: [round(U[dim * i + a], 5) for a in range(dim)] for i in range(len(nos))}
    soma_c = [sum(f[a] for f in m.get("cargas", {}).values()) for a in range(dim)]
    soma_r = [sum(r[a] for r in reacoes.values()) for a in range(dim)]
    return {"barras": barras, "reacoes_N": reacoes, "deslocamentos_mm": desloc,
            "verificacao_equilibrio": [round(soma_c[a] + soma_r[a], 6) for a in range(dim)]}

if __name__ == "__main__":
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    m = json.load(open(sys.argv[1]))
    r = resolver(m)
    print(f"{'barra':>6} {'i':>4} {'j':>4} {'L(mm)':>9} {'N(N)':>11}  tipo")
    for b in r["barras"]:
        print(f"{b['id']:>6} {b['i']:>4} {b['j']:>4} {b['L_mm']:>9} {b['N']:>11}  {b['tipo']}")
    print("reações (N):", r["reacoes_N"])
    print("equilíbrio (deve ser ~0):", r["verificacao_equilibrio"])
    if "--json" in sys.argv: print(json.dumps(r, ensure_ascii=False, indent=2))
