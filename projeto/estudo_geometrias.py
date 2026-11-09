#!/usr/bin/env python3
"""Estudo paramétrico: qual geometria de treliça aguenta 45 kg no meio de um vão de 500 mm
com o menor número de palitos de picolé + cola branca (PVA).

Hipóteses (ver projeto/MEMORIAL.md):
- Duas treliças planas iguais; cada uma recebe P/2 no nó central do banzo inferior.
- Barras = palitos laminados (n camadas coladas com a face larga no plano da treliça empilhadas
  para fora do plano). Seção: b = 8,4 mm (no plano) x n·2,0 mm (fora do plano).
- Tração: área útil (n-1) camadas se a barra for maior que um palito (emenda defasada), senão n.
- Compressão: menor entre Euler (eixo fraco e forte, K = 1, L = comprimento da barra) e esmagamento.
- Critério (envoltória): carga no centro com FS = 2,0 e carga deslocada um painel para cada lado
  com FS = 1,5 (a carga real nunca fica exatamente no centro). Mínimo de 2 camadas por barra.
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".claude", "skills", "analise-trelica", "scripts"))
from trelica import resolver

G = 9.80665
MASSA_ALVO = 45.0                 # kg
P = MASSA_ALVO * G               # N (total)
FS = 2.0
FS_DESLOC = 1.5
VAO = 500.0                      # mm
B, T, L_PAL = 8.4, 2.0, 110.0   # mm (palito)
E = 7350.0                       # MPa
FT = 52.55                       # MPa (tração paralela)
FC = 40.4                        # MPa (compressão paralela, Pinus elliottii, NBR 7190)
A1 = B * T

def capacidade(N, L, n):
    if N >= 0:
        nef = n if L <= L_PAL else n - 1
        return FT * A1 * nef, "tração"
    H = n * T
    I_fora = B * H**3 / 12; I_plano = H * B**3 / 12
    pe = math.pi**2 * E * min(I_fora, I_plano) / L**2
    pc = FC * B * H
    return (pe, "flambagem") if pe < pc else (pc, "esmagamento")

def dimensionar(casos, L):
    """casos: lista de (N, FS). Retorna n mínimo que atende todos."""
    n = 2
    while True:
        if all(abs(N) < 1e-9 or capacidade(N, L, n)[0] >= fs * abs(N) for N, fs in casos):
            N0 = casos[0][0]
            R, modo = capacidade(N0, L, n) if abs(N0) > 1e-9 else (None, "nula")
            return n, R, modo
        n += 1

def gerar(tipo, paineis, h):
    """Retorna modelo JSON da treliça (uma das duas) com carga P/2 no meio."""
    a = VAO / paineis
    nos, barras = {}, []
    for i in range(paineis + 1): nos[f"b{i}"] = [i * a, 0.0]
    def alt(x):  # altura do banzo superior
        if tipo == "parker": return h * (1 - abs(x - VAO / 2) / (VAO / 2)) if 0 < x < VAO else 0
        return h
    def add(i, j): barras.append({"id": f"{i}-{j}", "i": i, "j": j})
    for i in range(paineis): add(f"b{i}", f"b{i+1}")
    meio = paineis // 2
    if tipo in ("warren",):
        for i in range(paineis): nos[f"t{i}"] = [(i + 0.5) * a, h]
        for i in range(paineis - 1): add(f"t{i}", f"t{i+1}")
        for i in range(paineis): add(f"b{i}", f"t{i}"); add(f"t{i}", f"b{i+1}")
    elif tipo == "warren_v":
        for i in range(paineis): nos[f"t{i}"] = [(i + 0.5) * a, h]
        for i in range(paineis - 1): add(f"t{i}", f"t{i+1}")
        for i in range(paineis): add(f"b{i}", f"t{i}"); add(f"t{i}", f"b{i+1}")
        # montantes sob os nós superiores exigem nós no banzo inferior: subdivide
        return None
    else:
        for i in range(1, paineis): nos[f"t{i}"] = [i * a, alt(i * a)]
        for i in range(1, paineis - 1): add(f"t{i}", f"t{i+1}")
        add("b0", "t1"); add(f"t{paineis-1}", f"b{paineis}")
        for i in range(1, paineis): add(f"b{i}", f"t{i}")
        for i in range(1, paineis - 1):
            if tipo in ("pratt", "parker"):   # diagonais descem em direção ao centro
                add(f"t{i}", f"b{i+1}") if i < meio else add(f"t{i+1}", f"b{i}")
            elif tipo == "howe":            # diagonais sobem em direção ao centro
                add(f"b{i}", f"t{i+1}") if i < meio else add(f"b{i+1}", f"t{i}")
    return {"dim": 2, "E": E, "A": A1 * 2, "nos": nos, "barras": barras,
            "apoios": {"b0": [1, 1], f"b{paineis}": [0, 1]}, "cargas": {f"b{meio}": [0.0, -P / 2]}}

def avaliar(m):
    import copy
    r = resolver(m)
    meio = int(next(iter(m["cargas"]))[1:])
    desloc = []
    for k in (meio - 1, meio + 1):
        m2 = copy.deepcopy(m); m2["cargas"] = {f"b{k}": [0.0, -P / 2]}
        desloc.append({b["id"]: b["N"] for b in resolver(m2)["barras"]})
    tot, linhas = 0.0, []
    for b in r["barras"]:
        casos = [(b["N"], FS)] + [(d[b["id"]], FS_DESLOC) for d in desloc]
        n, R, modo = dimensionar(casos, b["L_mm"])
        b["N_desloc_max"] = max((d[b["id"]] for d in desloc), key=abs)
        palitos = n * b["L_mm"] / L_PAL
        tot += palitos
        linhas.append({**b, "n": n, "R": R, "modo": modo, "palitos": palitos})
    return tot, linhas, r

if __name__ == "__main__":
    res = []
    for tipo in ("pratt", "howe", "warren", "parker"):
        for paineis in (4, 6, 8, 10):
            for h in range(60, 181, 10):
                m = gerar(tipo, paineis, float(h))
                if m is None: continue
                try: tot, linhas, r = avaliar(m)
                except ValueError: continue
                res.append((tot, tipo, paineis, h, max(abs(d[1]) for d in r["deslocamentos_mm"].values())))
    res.sort()
    print(f"P total = {P:.5f} N ({MASSA_ALVO} kg), por treliça = {P/2:.5f} N, FS = {FS}")
    print(f"{'tipo':8} {'painéis':>7} {'h(mm)':>6} {'palitos/treliça':>16} {'flecha(mm)':>11}")
    for t in res[:15]: print(f"{t[1]:8} {t[2]:>7} {t[3]:>6} {t[0]:>16.5f} {t[4]:>11.5f}")
    print("\nmelhor de cada tipo:")
    for tipo in ("pratt", "howe", "warren", "parker"):
        t = min(x for x in res if x[1] == tipo)
        print(f"{t[1]:8} {t[2]:>7} {t[3]:>6} {t[0]:>16.5f} {t[4]:>11.5f}")
    json.dump([list(x) for x in res], open(os.path.join(os.path.dirname(__file__), "resultados_estudo.json"), "w"), indent=1)
