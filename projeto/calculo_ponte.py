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
# Decisão construtiva (v2): todas as barras com 3 camadas (6 mm), para as chapas das duas faces ficarem planas.
# Banzos: 3 camadas físicas com emendas desencontradas -> resistência com 2 efetivas (n da tabela = 2).
# Alma (diagonais e montantes): cada barra é menor que um palito, sem emenda -> 3 camadas efetivas.
def eh_banzo(x): return x["i"][0] == x["j"][0] or x["id"] in ("b0-t1", f"t{PAINEIS-1}-b{PAINEIS}")
for x in linhas:
    if not eh_banzo(x):
        x["n"] = 3
        Nref = x["N"] if abs(x["N"]) > 1e-9 else x["N_desloc_max"]
        if abs(x["N"]) > 1e-9: x["R"], x["modo"] = capacidade(x["N"], x["L_mm"], 3)
        x["R_desloc"], _ = capacidade(Nref, x["L_mm"], 3) if abs(Nref) > 1e-9 else (None, "")
f = lambda x: f"{x + 0.0:.5f}" if abs(x) >= 5e-6 else "0.00000"
print("=" * 100)
print(f"PONTE PARKER {PAINEIS} PAINÉIS, VÃO {VAO:.0f} mm, ALTURA {H:.0f} mm, LARGURA {LARG:.0f} mm")
print(f"Carga: {MASSA_ALVO} kg x {G} = {f(P)} N  |  por treliça = {f(P/2)} N")
print(f"Reações por treliça = {f(r['reacoes_N']['b0'][1])} N e {f(r['reacoes_N'][f'b{PAINEIS}'][1])} N  |  equilíbrio = {r['verificacao_equilibrio']}")
print("=" * 100)
print(f"{'barra':10}{'L (mm)':>11}{'N centro (N)':>15}{'N desloc (N)':>15}{'camadas':>8}{'R (N)':>14}{'FS centro':>11}{'modo':>13}{'FS desloc':>11}")
palitos_trelica = 0
for x in linhas:
    R = x["R"]; fs = (R / abs(x["N"])) if R and abs(x["N"]) > 1e-9 else float("inf")
    Rd, _ = capacidade(x["N_desloc_max"], x["L_mm"], x["n"]) if abs(x["N_desloc_max"]) > 1e-9 else (None, "")
    x["FS_desloc"] = (Rd / abs(x["N_desloc_max"])) if Rd else None
    palitos_trelica += x["n"]
    print(f"{x['id']:10}{f(x['L_mm']):>11}{f(x['N']):>15}{f(x['N_desloc_max']):>15}{x['n']:>8}"
          f"{(f(R) if R else '-'):>14}{(f(fs) if fs != float('inf') else 'barra nula'):>11}{x['modo']:>13}"
          f"{(f(x['FS_desloc']) if x['FS_desloc'] else '-'):>11}")
fs_min = min(x["R"] / abs(x["N"]) for x in linhas if x["R"] and abs(x["N"]) > 1e-9)
flecha = abs(r["deslocamentos_mm"][f"b{PAINEIS//2}"][1])
print("-" * 100)
print(f"FS mínimo (carga central) = {f(fs_min)}  ->  carga de ruptura prevista ≈ {f(fs_min*MASSA_ALVO)} kg")
print(f"Flecha no meio do vão (elástica, 45 kg) = {f(flecha)} mm")

# --- transversina central (v2): apoiada em consolos colados na face interna das chapas do nó b4 ---
# Ela não pode ficar em cima do banzo: ali passam o montante b4-t4 e as diagonais t3-b4 e t5-b4.
Z_APOIO = 64.0                              # distância entre os centros de apoio nos consolos (mm)
M = P * Z_APOIO / 4; V = P / 2
b_tr, n_tr = 2 * B, 10                      # 2 palitos lado a lado x 10 camadas deitadas
h_tr = n_tr * T
W = b_tr * h_tr**2 / 6
sig = M / W; tau = 1.5 * V / (b_tr * h_tr)
FC90 = 0.25 * FC                            # compressão normal às fibras (NBR 7190: f_c90 = 0,25 f_c0)
A_apoio = b_tr * 3 * T                      # contato transversina x consolo (16,8 x 6 mm)
sig_apoio = V / A_apoio
A_consolo = 30.0 * B                        # cola do consolo na chapa (30 x 8,4 mm)
tau_consolo = V / A_consolo
print("\nTRANSVERSINA CENTRAL (onde a carga é pendurada), apoiada em consolos")
print(f" vão entre apoios = {f(Z_APOIO)} mm | seção {f(b_tr)} x {f(h_tr)} mm | M = {f(M)} N·mm | σ = {f(sig)} MPa (FS = {f(FC/sig)})")
print(f" V = {f(V)} N | τ (cola entre camadas) = {f(tau)} MPa (FS = {f(TAU_COLA_K/tau)} com τ_cola,k estimado {TAU_COLA_K} MPa)")
print(f" apoio no consolo: σ90 = {f(sig_apoio)} MPa (FS = {f(FC90/sig_apoio)} com f_c90 = {f(FC90)} MPa)")
print(f" cola do consolo na chapa: τ = {f(tau_consolo)} MPa (FS = {f(TAU_COLA_K/tau_consolo)})")

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
    print(f" {x['id']:10} N = {f(Nd)} N -> sobreposição ≥ {f(Lo)} mm | adotado: 2 faixas de chapa = {f(2*B)} mm (FS = {f(FS_LIG*2*B/Lo)})")

# --- quantitativo e massa: vêm do modelo físico peça por peça (projeto/gerar_montagem.py) ---
mont = os.path.join(os.path.dirname(__file__), "montagem.json")
total = None
if os.path.exists(mont):
    rs = json.load(open(mont))["resumo"]
    total = rs["palitos_ponte"]
    print("\nQUANTITATIVO (do modelo físico, plano de corte)")
    print(f" peças = {rs['pecas']} | palitos para a ponte = {rs['palitos_ponte']} | para os ensaios = {rs['palitos_ensaio']}"
          f" | comprar (+15%) = {rs['palitos_comprar']}")
    print(f" área colada = {f(rs['area_cola_cm2'])} cm² | cola nas juntas = {f(rs['cola_g'])} g | massa estimada = {f(rs['massa_g'])} g")
else:
    print("\n(rode projeto/gerar_montagem.py para o quantitativo peça por peça)")
json.dump({"linhas": linhas, "reacoes": r["reacoes_N"], "flecha_mm": flecha, "fs_min": fs_min, "total_palitos": total},
          open(os.path.join(os.path.dirname(__file__), "resultados_ponte.json"), "w"), indent=1, ensure_ascii=False, default=str)
