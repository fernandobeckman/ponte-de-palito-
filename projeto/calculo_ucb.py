#!/usr/bin/env python3
"""Cálculo da ponte para o regulamento UCB 2026/2: treliça Pratt, 8 painéis, vão 800 mm, altura 100 mm.

Todas as barras com 3 palitos laminados (chapas planas). Barras maiores que um palito (banzos e diagonais)
têm emendas desencontradas: a resistência à tração conta só 2 palitos efetivos.
Gera projeto/ponte_ucb.json (modelo) e projeto/resultados_ucb_ponte.json; imprime o memorial com 5 casas.
"""
import json, math, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import estudo_geometrias as eg

G = 9.80665
VAO, PAINEIS, H, LARG = 800.0, 8, 100.0, 220.0
N_CAM = 3
E, FT, FC, B, T, L_PAL = eg.E, eg.FT, eg.FC, eg.B, eg.T, eg.L_PAL
TAU_COLA_K = 2.0             # MPa, estimativa conservadora para PVA [PENDENTE ensaio]
FC90 = 0.25 * FC
eg.VAO = VAO
f = lambda x: f"{x + 0.0:.5f}" if abs(x) >= 5e-6 else "0.00000"

m = eg.gerar("pratt", PAINEIS, H)
P1 = 1000.0                                          # carga total de referência (N); metade em cada treliça
m["cargas"] = {k: [0.0, -P1 / 2] for k in m["cargas"]}
m["E"], m["A"] = E, N_CAM * B * T
json.dump(m, open(os.path.join(D, "ponte_ucb.json"), "w"), indent=1)
r = eg.resolver(m)

BANZOS = {b["id"] for b in m["barras"] if b["i"][0] == b["j"][0]}   # b-b e t-t: banzos contínuos laminados

def cap(N, L, emendada=False):
    """Resistência da barra de 3 palitos. Barra emendada (maior que um palito ou banzo contínuo com
    emendas desencontradas): na tração só contam 2 palitos; na compressão o topo das emendas encosta e transmite."""
    emendada = emendada or L > L_PAL
    if N >= 0:
        nef = N_CAM - 1 if emendada else N_CAM
        return FT * B * T * nef, "tração" + (" (emenda: 2 efetivos)" if emendada else "")
    Hh = N_CAM * T
    pe = math.pi ** 2 * E * min(B * Hh ** 3 / 12, Hh * B ** 3 / 12) / L ** 2
    pc = FC * B * Hh
    return (pe, "flambagem") if pe < pc else (pc, "esmagamento")

# carga deslocada um painel (a barra de aço pode não ficar exatamente no centro)
meio = PAINEIS // 2
desl = []
for k in (meio - 1, meio + 1):
    m2 = dict(m); m2["cargas"] = {f"b{k}": [0.0, -P1 / 2]}
    desl.append({b["id"]: b["N"] for b in eg.resolver(m2)["barras"]})

print("=" * 104)
print(f"PONTE UCB — PRATT {PAINEIS} PAINÉIS · VÃO {VAO:.0f} mm · ALTURA {H:.0f} mm · LARGURA {LARG:.0f} mm · {N_CAM} PALITOS POR BARRA")
print(f"Esforços para carga total de {f(P1)} N ({f(P1 / G)} kgf), metade em cada treliça")
print(f"Reações por treliça: {r['reacoes_N']} | equilíbrio = {r['verificacao_equilibrio']}")
print("=" * 104)
print(f"{'barra':9}{'L (mm)':>11}{'N/1000 N':>13}{'N desloc':>13}{'R (N)':>13}{'P colapso (kgf)':>17}  modo")
linhas, pcol = [], []
for b in r["barras"]:
    Nd = max(desl[0][b["id"]], desl[1][b["id"]], key=abs)
    # cada situação de carga usa a resistência do seu próprio sinal (tração ou compressão)
    Rc, modo_c = cap(b["N"], b["L_mm"], b["id"] in BANZOS) if abs(b["N"]) > 1e-9 else (None, "")
    pc_c = Rc / abs(b["N"]) * P1 / G if Rc else float("inf")
    pc_d, Rd, modo_d = float("inf"), None, ""
    for dd in desl:                      # carga deslocada para cada lado, cada uma com o seu sinal
        Nk = dd[b["id"]]
        if abs(Nk) < 1e-9: continue
        Rk, mk = cap(Nk, b["L_mm"], b["id"] in BANZOS); pk = Rk / abs(Nk) * P1 / G
        if pk < pc_d: pc_d, Rd, modo_d, Nd = pk, Rk, mk, Nk
    pmin = min(pc_c, pc_d)
    R, modo = (Rc, modo_c) if pc_c <= pc_d else (Rd, modo_d + " (carga deslocada)")
    if R is None: R, modo = cap(0.0, b["L_mm"], b["id"] in BANZOS)
    pcol.append((pmin, b["id"], modo))
    linhas.append(dict(id=b["id"], i=b["i"], j=b["j"], L_mm=b["L_mm"], N=b["N"], N_desloc=Nd, R=R, modo=modo, P_kgf=pmin, n=N_CAM))
    print(f"{b['id']:9}{f(b['L_mm']):>11}{f(b['N']):>13}{f(Nd):>13}{f(R):>13}{(f(pmin) if pmin < 1e9 else '—'):>17}  {modo}")
pcol.sort()
P_barra = pcol[0][0]
print("-" * 104)
print(f"Barra crítica: {pcol[0][1]} ({pcol[0][2]}) -> colapso calculado das barras = {f(P_barra)} kgf")

# ligações coladas: chapa nas duas faces; sobreposição de cada barra dentro da chapa
Nmax = max(abs(x["N"]) for x in linhas) * (P_barra * G / P1)
SOBRE = 40.0                                          # mm de sobreposição de cada ponta de barra dentro da chapa
R_lig = TAU_COLA_K * 2 * B * SOBRE * 1.0              # 2 faces x largura x sobreposição
P_lig = R_lig / (max(abs(x["N"]) for x in linhas) / P1) / G
print(f"\nLIGAÇÕES: chapas nas 2 faces, {SOBRE:.0f} mm de sobreposição -> resistência {f(R_lig)} N por ponta de barra")
print(f" colapso pela cola (barra mais carregada) = {f(P_lig)} kgf  (τ_cola estimado {TAU_COLA_K} MPa [PENDENTE ensaio])")

# mini-treliça transversal que recebe a haste de aço no meio (vão entre os consolos, altura 70 mm, 3 palitos por barra)
VAO_M, D_M = 194.0, 70.0
k_banzo = VAO_M / (4 * D_M)                                   # força no banzo = k_banzo x P
P_m_banzo_t = (FT * B * T * (N_CAM - 1)) / k_banzo / G        # banzo de baixo (tração, com emenda)
P_m_banzo_c = (math.pi ** 2 * E * (B * (N_CAM * T) ** 3 / 12) / 46.0 ** 2) / k_banzo / G
sen_d = 70.0 / math.hypot(50.0, 70.0)
k_diag = 0.5 / sen_d                                          # força na diagonal = k_diag x P
P_m_diag = (FT * B * T * N_CAM) / k_diag / G
R_lig_m = TAU_COLA_K * 2 * B * (3 * B)                        # 3 faixas de chapa nas 2 faces
P_m_lig = R_lig_m / k_diag / G
R_consolo = TAU_COLA_K * 30.0 * B                             # cola do consolo na chapa interna (por lado)
P_consolo = 2 * R_consolo / G
print(f"\nMINI-TRELIÇA DO PONTO DE CARGA (vão {f(VAO_M)} mm, altura {f(D_M)} mm):")
print(f" banzo de baixo (tração) -> {f(P_m_banzo_t)} kgf | banzo de cima (flambagem) -> {f(P_m_banzo_c)} kgf")
print(f" diagonais (tração) -> {f(P_m_diag)} kgf | ligações (3 faixas, 2 faces) -> {f(P_m_lig)} kgf")
print(f" cola dos consolos nas treliças (30 x 8,4 mm por lado) -> {f(P_consolo)} kgf")
P_tr = min(P_m_banzo_t, P_m_banzo_c, P_m_diag, P_m_lig); P_tr_tau = P_consolo

P_final = min(P_barra, P_lig, P_tr, P_tr_tau)
print("\n" + "=" * 104)
print(f"CARGA DE COLAPSO CALCULADA (menor de todas) = {f(P_final)} kgf")
print(f"Bônus exige 30 kgf -> fator de segurança calculado = {f(P_final / 30)}")
json.dump(dict(linhas=linhas, P_barra=P_barra, P_lig=P_lig, P_tr=P_tr, P_tr_tau=P_tr_tau, P_final=P_final,
               reacoes=r["reacoes_N"]), open(os.path.join(D, "resultados_ucb_ponte.json"), "w"), indent=1, ensure_ascii=False)
