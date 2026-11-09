#!/usr/bin/env python3
"""Cálculo estrutural completo da ponte escolhida: Parker (banzo superior triangular), 8 painéis, h = 90 mm.
Gera: projeto/ponte_parker_8x90.json (modelo) e projeto/resultados_ponte.json, e imprime o memorial (5 casas)."""
import copy, json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from estudo_geometrias import *  # mesmas hipóteses e materiais do estudo

TIPO, PAINEIS, H = "parker", 8, 90.0
LARG = 80.0            # distância entre os eixos das duas treliças (mm)
RHO = 560e-9           # kg/mm³ — Pinus elliottii, NBR 7190 (ρ ap a 12%)
TAU_COLA_K = 2.0       # MPa — ESTIMATIVA conservadora para PVA em madeira [PENDENTE ensaio]
FS_LIG = 2.0

m = gerar(TIPO, PAINEIS, H)
json.dump(m, open(os.path.join(os.path.dirname(__file__), "ponte_parker_8x90.json"), "w"), indent=1)
tot, linhas, r = avaliar(m)
f = lambda x: f"{x + 0.0:.5f}" if abs(x) >= 5e-6 else "0.00000"
print("=" * 100)
print(f"PONTE PARKER {PAINEIS} PAINÉIS, VÃO {VAO:.0f} mm, ALTURA {H:.0f} mm, LARGURA {LARG:.0f} mm")
print(f"Carga: {MASSA_ALVO} kg x {G} = {f(P)} N  |  por treliça = {f(P/2)} N")
print(f"Reações por treliça = {f(r['reacoes_N']['b0'][1])} N e {f(r['reacoes_N'][f'b{PAINEIS}'][1])} N  |  equilíbrio = {r['verificacao_equilibrio']}")
print("=" * 100)
print(f"{'barra':10}{'L (mm)':>11}{'N centro (N)':>15}{'N desloc (N)':>15}{'camadas':>8}{'R (N)':>14}{'FS centro':>11}{'modo':>13}")
palitos_trelica = 0
for x in linhas:
    R = x["R"]; fs = (R / abs(x["N"])) if R and abs(x["N"]) > 1e-9 else float("inf")
    palitos_trelica += x["n"]
    print(f"{x['id']:10}{f(x['L_mm']):>11}{f(x['N']):>15}{f(x['N_desloc_max']):>15}{x['n']:>8}"
          f"{(f(R) if R else '-'):>14}{(f(fs) if fs != float('inf') else 'barra nula'):>11}{x['modo']:>13}")
fs_min = min(x["R"] / abs(x["N"]) for x in linhas if x["R"] and abs(x["N"]) > 1e-9)
flecha = abs(r["deslocamentos_mm"][f"b{PAINEIS//2}"][1])
print("-" * 100)
print(f"FS mínimo (carga central) = {f(fs_min)}  ->  carga de ruptura prevista ≈ {f(fs_min*MASSA_ALVO)} kg")
print(f"Flecha no meio do vão (elástica, 45 kg) = {f(flecha)} mm")

# --- transversina central (recebe a carga e reparte para as duas treliças) ---
M = P * LARG / 4; V = P / 2
b_tr, n_tr = 2 * B, 10                      # 2 palitos lado a lado x 10 camadas deitadas
h_tr = n_tr * T
W = b_tr * h_tr**2 / 6
sig = M / W; tau = 1.5 * V / (b_tr * h_tr)
print("\nTRANSVERSINA CENTRAL (onde a carga é pendurada)")
print(f" seção {f(b_tr)} x {f(h_tr)} mm | M = {f(M)} N·mm | σ = {f(sig)} MPa (FS = {f(FC/sig)} usando f_c como limite)")
print(f" V = {f(V)} N | τ (cola entre camadas) = {f(tau)} MPa (FS = {f(TAU_COLA_K/tau)} com τ_cola,k estimado {TAU_COLA_K} MPa)")

# --- banzos contínuos: 3 camadas laminadas, emendas de topo desencontradas (≥ 30 mm) ---
# Em qualquer seção 1 camada pode estar emendada -> considera-se só 2 camadas efetivas (já é o que a tabela usa).
banzo_sup = 2 * math.hypot(VAO / 2, H); banzo_inf = VAO
cam_banzo = 3
print("\nBANZOS CONTÍNUOS (3 camadas, emendas desencontradas; resistência conta só 2 camadas)")
print(f" banzo superior: 2 trechos retos de {f(banzo_sup/2)} mm | banzo inferior: {f(banzo_inf)} mm")

# --- ligações das barras de alma (diagonais e montantes) nas chapas (2 faces) ---
print("\nLIGAÇÕES DAS BARRAS DE ALMA — sobreposição mínima dentro da chapa (2 faces coladas, largura 8,4 mm)")
alma = [x for x in linhas if not ((x["i"][0] == x["j"][0] == "b") or (x["i"][0] == x["j"][0] == "t")
        or x["id"] in ("b0-t1", f"t{PAINEIS-1}-b{PAINEIS}"))]
for x in sorted(alma, key=lambda y: -max(abs(y["N"]), abs(y["N_desloc_max"])))[:5]:
    Nd = max(abs(x["N"]), abs(x["N_desloc_max"]))
    Lo = FS_LIG * Nd / (TAU_COLA_K * 2 * B)
    print(f" {x['id']:10} N = {f(Nd)} N -> sobreposição ≥ {f(Lo)} mm (adote 20 mm)")

# --- quantitativo e massa ---
nos = len(m["nos"])
pal_banzos = math.ceil(cam_banzo * (banzo_sup + banzo_inf) / L_PAL) + 2   # +2 por causa do desencontro
pal_alma = sum(x["n"] for x in alma)
palitos_trelica = pal_banzos + pal_alma
transv_comuns = (PAINEIS + 1 - 1) * 2              # 8 transversinas inferiores de 2 camadas
transv_sup = (PAINEIS - 1) * 2                     # escoras superiores nos nós t1..t7
contrav = PAINEIS * 2 * 2                          # X inferior e superior por painel (aprox.)
chapas = nos * 2                                   # 2 chapas (1 palito cada) por nó, por treliça
transv_central = n_tr * 2
total = 2 * palitos_trelica + 2 * chapas + transv_comuns + transv_sup + contrav + transv_central
massa_palito = RHO * B * T * L_PAL * 1000          # g
print("\nQUANTITATIVO (palitos inteiros)")
print(f" banzos = {2*pal_banzos} | alma = {2*pal_alma} | chapas = {2*chapas} | transversinas = {transv_comuns + transv_central}"
      f" | escoras superiores = {transv_sup} | contraventamento = {contrav}")
print(f" TOTAL ≈ {total} palitos (+20% de perda: compre {math.ceil(total*1.2)})")
print(f" massa estimada = {f(total*massa_palito*1.15)} g (madeira + 15% de cola) — peso próprio desprezível frente a 45 kg")
json.dump({"linhas": linhas, "reacoes": r["reacoes_N"], "flecha_mm": flecha, "fs_min": fs_min, "total_palitos": total},
          open(os.path.join(os.path.dirname(__file__), "resultados_ponte.json"), "w"), indent=1, ensure_ascii=False, default=str)
