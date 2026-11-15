#!/usr/bin/env python3
"""Estudo para o regulamento da IV Competição da Ponte de Palito de Picolé (UCB 2026/2).

Regras usadas (docs/requisitos.md): vão livre 800 mm, comprimento total 1000-1100 mm, largura 200-250 mm,
altura até 300 mm, peso até 1 kg, no máximo 5 palitos por seção, carga no meio do vão.
Pontuação: NF = (carga de ruptura / peso) x 0,8 + estética x 0,2  -> o objetivo é a maior carga POR PESO.

Para cada geometria e cada carga-alvo P: dimensiona cada barra com o menor número de camadas (1 a 5) que
resiste a GAMA x esforço (GAMA = 1,5 cobre imperfeições e colagem), estima a massa da ponte inteira
(2 treliças + chapas + travamento + cola) e calcula a eficiência P / massa.
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import estudo_geometrias as eg

G = 9.80665
VAO, LARG, H_MAX_EIXO = 800.0, 220.0, 270.0
GAMA = 1.5                     # resistência calculada >= 1,5 x esforço (imperfeições, colagem, variação do palito)
N_MAX = 5
RHO_L = 560e-9 * 8.4 * 2.0 * 1000     # g por mm de palito (Pinus elliottii, 560 kg/m³)
eg.VAO = VAO

def dimensiona(m, P):
    m = dict(m); m["cargas"] = {k: [0.0, -P / 2] for k in m["cargas"]}   # metade da carga em cada treliça
    r = eg.resolver(m)
    massa_mm, linhas = 0.0, []
    for b in r["barras"]:
        n = 1 if abs(b["N"]) < 1e-6 else None
        if n is None:
            for k in range(1, N_MAX + 1):
                if eg.capacidade(b["N"], b["L_mm"], k)[0] >= GAMA * abs(b["N"]): n = k; break
        if n is None: return None                       # nem 5 palitos resolvem
        if abs(b["N"]) < 1e-6: n = 2                     # barra de travamento: 2 palitos
        linhas.append((b, n)); massa_mm += n * b["L_mm"]
    return r, linhas, massa_mm

def massa_total(m, massa_mm_trelica):
    nos = len(m["nos"]); paineis = sum(1 for k in m["nos"] if k.startswith("b")) - 1
    trelicas = 2 * massa_mm_trelica * RHO_L
    chapas = 2 * nos * 2 * 3 * 40 * RHO_L                 # 2 faces, 3 peças de 40 mm por nó
    travamento = (paineis + 1 + paineis - 1) * 2 * LARG * RHO_L + 2 * paineis * 1.15 * math.hypot(LARG, VAO / paineis) * RHO_L
    balanco = 2 * 2 * 3 * 125 * RHO_L                     # prolongamento de 125 mm além de cada apoio (banzo inferior)
    madeira = trelicas + chapas + travamento + balanco
    return madeira * 1.12                                  # + cola seca (~12%)

res = []
for tipo in ("pratt", "howe", "warren", "parker"):
    for paineis in (6, 8, 10, 12):
        for h in range(120, int(H_MAX_EIXO) + 1, 15):
            m = eg.gerar(tipo, paineis, float(h))
            if m is None: continue
            for kg in range(30, 161, 5):
                d = dimensiona(m, kg * G)
                if d is None: break
                r, linhas, mm = d
                M = massa_total(m, mm)
                if M > 1000: continue
                Lmax = max(b["L_mm"] for b, n in linhas)
                res.append(dict(tipo=tipo, paineis=paineis, h=h, kg=kg, massa=M, ef=kg * 1000 / M, Lmax=Lmax,
                                nmax=max(n for b, n in linhas)))
res.sort(key=lambda x: -x["ef"])
print(f"{len(res)} combinações viáveis (até 5 palitos por barra, até 1 kg)")
print(f"{'tipo':7}{'pain':>5}{'h':>5}{'meta kg':>8}{'massa g':>9}{'kg/kg':>8}{'Lmax':>7}{'nmax':>5}")
vistos = set()
for x in res:
    k = (x["tipo"], x["paineis"], x["h"])
    if k in vistos: continue
    vistos.add(k)
    print(f"{x['tipo']:7}{x['paineis']:>5}{x['h']:>5}{x['kg']:>8}{x['massa']:>9.1f}{x['ef']:>8.1f}{x['Lmax']:>7.1f}{x['nmax']:>5}")
    if len(vistos) >= 15: break
print("\nmelhor de cada tipo:")
for tipo in ("pratt", "howe", "warren", "parker"):
    x = max((y for y in res if y["tipo"] == tipo), key=lambda y: y["ef"])
    print(f"{tipo:7}{x['paineis']:>5}{x['h']:>5}{x['kg']:>8}{x['massa']:>9.1f}{x['ef']:>8.1f}{x['Lmax']:>7.1f}{x['nmax']:>5}")
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados_ucb.json"), "w"))
