#!/usr/bin/env python3
"""Modelo físico da ponte palito por palito + sequência de montagem + lista de corte + orçamento.
Versão UCB 2026/2: treliça Pratt, 8 painéis de 100 mm, vão 800 mm, altura 100 mm, largura 220 mm, comprimento 1020 mm.

Gera projeto/montagem.json e site/montagem.html (a partir de projeto/montagem_modelo.html).

Convenções (mm):
- Cada treliça é montada deitada sobre o gabarito. Coordenadas locais: x ao longo do vão (0 e 800 = bordas dos blocos de apoio),
  y para cima no plano da treliça, z = espessura (empilhamento das camadas).
- Camadas em z: chapas da face 1 [0,2], camada 1 [2,4], camada 2 [4,6], camada 3 [6,8], chapas da face 2 [8,10].
- Todas as barras têm 3 camadas (núcleo de 6 mm). Barras maiores que um palito têm emendas desencontradas entre as camadas.
- Mundo (ponte de pé): x ao longo do vão, y para cima, z na largura. Treliça A em z = -110..-100, B em z = 100..110 (largura 220 mm).
"""
import json, math, os

D = os.path.dirname(os.path.abspath(__file__))
m = json.load(open(os.path.join(D, "ponte_ucb.json")))
W, T = 8.4, 2.0                  # largura e espessura do palito
L_PALITO, L_UTIL = 110.0, 101.6  # comprimento total e reto útil (sem as pontas arredondadas)
VAO, H, NP = 800.0, 100.0, 8
A_PAINEL = VAO / NP
BALANCO = 110.0                  # banzo inferior passa 110 mm além de cada apoio: comprimento total 1020 mm
GAP = 0.0
Y0 = 268.2                       # altura do eixo do banzo inferior com a ponte de pé sobre os apoios
ZA, ZB = -110.0, 100.0           # posição (z do mundo) da face 1 de cada treliça em pé
LARG_TOTAL = 220.0
FRAC_EMENDA = {0: 0.25, 1: 0.5, 2: 0.75}   # posição da emenda em cada camada, ao longo da barra
# ---------------------------------------------------------------- geometria 2D
def clip(poly, a, b, c):
    """Mantém a parte do polígono com a*x + b*y <= c (Sutherland-Hodgman)."""
    out = []
    n = len(poly)
    for i in range(n):
        P, Q = poly[i], poly[(i + 1) % n]
        fp, fq = a * P[0] + b * P[1] - c, a * Q[0] + b * Q[1] - c
        if fp <= 1e-9: out.append(P)
        if (fp < -1e-9 and fq > 1e-9) or (fp > 1e-9 and fq < -1e-9):
            t = fp / (fp - fq)
            out.append([P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])])
    return out

def faixa(p, d, s0, s1, w=W):
    """Retângulo de largura w ao longo da reta p + s*d, de s0 a s1."""
    nx, ny = -d[1], d[0]
    h = w / 2
    pts = []
    for s, k in ((s0, -1), (s1, -1), (s1, 1), (s0, 1)):
        pts.append([p[0] + s * d[0] + k * h * nx, p[1] + s * d[1] + k * h * ny])
    return pts

def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2

def extensao(poly, d):
    pr = [q[0] * d[0] + q[1] * d[1] for q in poly]
    return min(pr), max(pr)

# linhas dos banzos: (origem, direção unitária)
LPOST = math.hypot(A_PAINEL, H)
ESQ = ((0.0, 0.0), (A_PAINEL / LPOST, H / LPOST))              # montante inclinado da ponta esquerda (b0 -> t1)
DIR = ((VAO, 0.0), (-A_PAINEL / LPOST, H / LPOST))             # ponta direita (b8 -> t7)
INF = ((0.0, 0.0), (1.0, 0.0))                                 # banzo inferior (eixo y = 0; peças de -BALANCO a VAO + BALANCO)
TOPO = ((A_PAINEL, H), (1.0, 0.0))                             # banzo superior reto (t1 -> t7)
LTOPO = VAO - 2 * A_PAINEL

def lado_normal(linha):
    (px, py), (dx, dy) = linha
    nx, ny = -dy, dx
    if ny < 0 or (abs(ny) < 1e-12 and nx < 0): nx, ny = -nx, -ny
    return nx, ny, nx * px + ny * py

def abaixo_de(linha, off):
    nx, ny, c = lado_normal(linha)
    return (nx, ny, c + off)

def acima_de(linha, off):
    nx, ny, c = lado_normal(linha)
    return (-nx, -ny, -(c + off))

def recorta(poly, planos):
    for a, b, c in planos:
        poly = clip(poly, a, b, c)
        if len(poly) < 3: return []
    return poly

def emendas(s0, s1, primeira, passo=100.0, minimo=25.0):
    """Divide [s0,s1] em peças <= passo, com a primeira emenda em s0+primeira."""
    cortes = [s0]
    s = s0 + primeira
    while s < s1 - 1e-6:
        cortes.append(s); s += passo
    cortes.append(s1)
    if len(cortes) > 2 and cortes[-1] - cortes[-2] < minimo:
        cortes[-2] = (cortes[-3] + cortes[-1]) / 2 if cortes[-1] - cortes[-3] <= passo else cortes[-1] - minimo
    return [(cortes[i], cortes[i + 1]) for i in range(len(cortes) - 1)]

def divide(poly, d, k):
    """Se a peça for maior que um palito, corta em duas com a emenda na posição da camada k (desencontrada)."""
    a0, a1 = extensao(poly, d)
    if a1 - a0 <= L_UTIL: return [poly]
    s = a0 + FRAC_EMENDA[k] * (a1 - a0)
    p1 = recorta(poly, [(d[0], d[1], s)]); p2 = recorta(poly, [(-d[0], -d[1], -s)])
    out = []
    for q in (p1, p2):
        if q: out += divide(q, d, k) if extensao(q, d)[1] - extensao(q, d)[0] > L_UTIL else [q]
    return out

NOS = {k: tuple(v) for k, v in m["nos"].items()}
def no(k): return NOS[k]
DENTRO = [acima_de(INF, W / 2), abaixo_de(TOPO, -W / 2), abaixo_de(ESQ, -W / 2), abaixo_de(DIR, -W / 2)]

def pecas_trelica():
    camadas = {"f1": [], "L1": [], "L2": [], "L3": [], "f2": []}
    off_emenda = {"L1": 100.0, "L2": 66.67, "L3": 33.33}
    for k, cam in enumerate(("L1", "L2", "L3")):
        z0 = 2.0 + 2.0 * k
        # banzo inferior: inteiro em todas as camadas (as pontas das barras encostam nele)
        trechos = emendas(-BALANCO, VAO + BALANCO, off_emenda[cam])
        for i, (a, b) in enumerate(trechos):
            camadas[cam].append(dict(nome=f"Banzo inferior, camada {k+1}, peça {i+1} de {len(trechos)}",
                                     poly=faixa(INF[0], INF[1], a, b), z0=z0, eixo=INF[1], tipo="banzo"))
        # banzo superior reto: passa por cima dos montantes inclinados das pontas
        trechos = emendas(-W, LTOPO + W, off_emenda[cam])
        for i, (a, b) in enumerate(trechos):
            p = recorta(faixa(TOPO[0], TOPO[1], a, b), [abaixo_de(ESQ, W / 2), abaixo_de(DIR, W / 2)])
            if p: camadas[cam].append(dict(nome=f"Banzo superior, camada {k+1}, peça {i+1} de {len(trechos)}",
                                           poly=p, z0=z0, eixo=TOPO[1], tipo="banzo"))
        # montantes inclinados das pontas (b0-t1 e b8-t7): entre os dois banzos, com emenda desencontrada
        for lado, lin in (("esquerda", ESQ), ("direita", DIR)):
            p = recorta(faixa(lin[0], lin[1], -10, LPOST + 10), [acima_de(INF, W / 2), abaixo_de(TOPO, -W / 2)])
            partes = divide(p, lin[1], k)
            for i, q in enumerate(partes):
                camadas[cam].append(dict(nome=f"Barra inclinada da ponta {lado}, camada {k+1}, peça {i+1} de {len(partes)}",
                                         poly=q, z0=z0, eixo=lin[1], tipo="banzo"))
        # alma: montantes e diagonais, recortados pelos banzos e (diagonais) pelos montantes
        for bar in m["barras"]:
            i, j = bar["i"], bar["j"]
            if i[0] == j[0] or bar["id"] in ("b0-t1", "t7-b8"): continue
            P, Q = no(i), no(j)
            d = (Q[0] - P[0], Q[1] - P[1]); L = math.hypot(*d); d = (d[0] / L, d[1] / L)
            planos = list(DENTRO)
            if abs(d[0]) > 1e-6:
                for nk in (i, j):
                    x = no(nk)[0]; outro = Q if nk == i else P
                    planos.append((1, 0, x - W / 2) if outro[0] < x else (-1, 0, -(x + W / 2)))
            p = recorta(faixa(P, d, -20, L + 20), planos)
            if not p: continue
            tipo = "montante" if abs(d[0]) < 1e-6 else "diagonal"
            partes = divide(p, d, k)
            for n_, q in enumerate(partes):
                extra = f", peça {n_+1} de {len(partes)}" if len(partes) > 1 else ""
                camadas[cam].append(dict(nome=f"{tipo.capitalize()} {bar['id']}, camada {k+1}{extra}", poly=q, z0=z0,
                                         eixo=d, tipo=tipo, barra=bar["id"]))
    # chapas de ligação (2 faces)
    def chapas(z0, face):
        out = []
        for nk, (x, y) in NOS.items():
            pc = []
            if nk in ("b0", f"b{NP}"):
                pc.append(("sobre o banzo inferior", faixa((x, 0), (1, 0), -30, 30), (1, 0), []))
                lin = ESQ if nk == "b0" else DIR
                pc.append(("sobre a barra inclinada", faixa(lin[0], lin[1], 4, 52), lin[1], [acima_de(INF, W / 2)]))
            elif nk.startswith("b"):
                pc.append(("sobre o banzo", faixa((x, 0), (1, 0), -20, 20), (1, 0), []))
                for fx in (1, 2):
                    pc.append((f"faixa {fx} sobre as pontas das barras", faixa((x, fx * W), (1, 0), -20, 20), (1, 0),
                               [abaixo_de(TOPO, -W / 2), abaixo_de(ESQ, -W / 2), abaixo_de(DIR, -W / 2)]))
            else:
                ponta = nk in ("t1", f"t{NP-1}")
                lin_p = ESQ if nk == "t1" else DIR
                corte_ponta = [abaixo_de(ESQ, W / 2), abaixo_de(DIR, W / 2)]
                a, b = (-15, 25) if nk == "t1" else (-25, 15) if nk == f"t{NP-1}" else (-20, 20)
                pc.append(("sobre o banzo", faixa((x, y), (1, 0), a, b), (1, 0), corte_ponta))
                if ponta:
                    pc.append(("sobre a barra inclinada", faixa(lin_p[0], lin_p[1], LPOST - 50, LPOST), lin_p[1],
                               [abaixo_de(TOPO, -W / 2)]))
                for fx in (1, 2):
                    pc.append((f"faixa {fx} sobre as pontas das barras", faixa((x, y - fx * W), (1, 0), a, b), (1, 0),
                               [acima_de(INF, W / 2 + 2 * W), abaixo_de(ESQ, -W / 2), abaixo_de(DIR, -W / 2)]))
            for i, (onde, p, eixo, planos) in enumerate(pc):
                p = recorta(p, planos)
                if p and area(p) < 80: p = []
                if p: out.append(dict(nome=f"Chapa do nó {nk}, face {face}, peça {i+1} de {len(pc)} ({onde})",
                                      poly=p, z0=z0, eixo=eixo, tipo="chapa", no=nk))
        return out
    camadas["f1"] = chapas(0.0, 1)
    camadas["f2"] = chapas(8.0, 2)
    for k in camadas:
        camadas[k].sort(key=lambda p: (0 if p["tipo"] in ("banzo", "chapa") else 1,
                                       sum(q[0] for q in p["poly"]) / len(p["poly"])))
    return camadas

# ---------------------------------------------------------------- sequência
passos = []
def evento(tipo, cap, txt, det="", foco=None, dist=600):
    passos.append(dict(k="ev", ev=tipo, cap=cap, txt=txt, det=det, foco=foco, dist=dist))

def fmt1(v): return f"{v:.1f}".replace(".", ",")

def peca(g, cap, p, txt, det, cola, frame=None):
    d = p["eixo"]
    a0, a1 = extensao(p["poly"], d)
    comp = a1 - a0
    assert comp <= L_UTIL + 0.01 or p.get("inteiro"), (p["nome"], comp)
    reg = dict(k="pc", g=g, cap=cap, nome=p["nome"], poly=[[round(x, 3), round(y, 3)] for x, y in p["poly"]],
               z0=p.get("z0", 0.0), ax=[round(d[0], 6), round(d[1], 6)], a0=round(a0, 3), a1=round(a1, 3),
               comp=round(comp, 3), area=round(area(p["poly"]), 3), tipo=p["tipo"], inteiro=bool(p.get("inteiro")),
               txt=txt, det=det, cola=cola, fr=frame)
    passos.append(reg)
    return reg

camadas = pecas_trelica()
NOME_CAM = {"f1": "chapas da face de baixo", "L1": "camada 1", "L2": "camada 2", "L3": "camada 3", "f2": "chapas da face de cima"}

evento("gabarito", "Preparação", "Imprima o gabarito em tamanho real (1020 × 120 mm) e prenda na mesa com fita.",
       "Confira a escala: a régua do gabarito tem que medir exatamente 100 mm.", foco="mesa", dist=1300)
evento("filme", "Preparação", "Cubra o gabarito com plástico de polietileno (saco plástico transparente bem esticado).",
       "A cola branca não adere ao polietileno (ficha técnica da Cascorez Extra), então a treliça solta depois sem rasgar.",
       foco="mesa", dist=1300)
evento("materiais", "Preparação", "Separe os palitos, a cola branca, o estilete, a régua e o esquadro.",
       "Escolha palitos retos e sem rachaduras. Descarte os empenados: eles atrapalham a colagem.", foco="materiais", dist=420)

for g in ("A", "B"):
    T_ = f"Treliça {g}"
    for cam in ("f1", "L1", "L2", "L3", "f2"):
        cap = f"{T_} · {NOME_CAM[cam]}"
        for p in camadas[cam]:
            comp = extensao(p["poly"], p["eixo"])[1] - extensao(p["poly"], p["eixo"])[0]
            corte = f"corte {fmt1(comp)} mm"
            if cam == "f1":
                txt, cola = f"{p['nome']}: {corte} e coloque sobre o plástico, sem cola.", []
                det = "As chapas da face de baixo só ficam posicionadas; a cola entra quando a camada 1 for colocada por cima."
            elif cam == "L1":
                txt, cola = f"{p['nome']}: {corte}, passe cola onde ela apoia nas chapas e encoste de topo nas peças vizinhas.", "pontas"
                det = "Pontas cortadas no ângulo marcado no gabarito. Encoste bem: fresta na emenda vira ponto fraco."
            elif cam in ("L2", "L3"):
                txt, cola = f"{p['nome']}: {corte}, passe um cordão contínuo de cola sobre a camada de baixo e pressione por 30 s.", "toda"
                det = ("As emendas desta camada ficam desencontradas das emendas das outras camadas."
                       if "peça" in p["nome"] else "Alinhe as bordas com a camada de baixo antes de pressionar.")
            else:
                txt, cola = f"{p['nome']}: {corte}, passe cola em toda a face e pressione por 30 s.", "toda"
                det = "Limpe o excesso de cola que escorrer pelas bordas com um palito, antes de secar."
            peca(g, cap, p, txt, f"{det} Comprimento: {fmt1(comp)} mm · espessura 2,0 mm · largura 8,4 mm.", cola)
    evento(f"prensa{g}", f"{T_} · prensagem", f"Cubra a treliça {g} com um plástico e uma tábua reta e coloque peso por cima (livros).",
           "Pressão uniforme deixa a linha de cola fina e forte. Não deslize a tábua: só apoie.", foco=g, dist=1100)
    evento(f"cura{g}", f"{T_} · cura", f"Deixe a treliça {g} secar o máximo possível (ideal: 24 h; mínimo: uma noite).",
           "A cola branca só atinge a resistência total depois de 24 h. Pelo prazo da competição, monte as duas treliças no mesmo dia.",
           foco=g, dist=1100)

evento("desenforma", "Acabamento", "Retire as duas treliças do gabarito, puxando o plástico devagar.",
       "Se alguma peça descolar, recole e espere a cola firmar antes de continuar.", foco="AB", dist=1300)
evento("lixa", "Acabamento", "Lixe de leve as rebarbas de cola das bordas, sem afinar os palitos.",
       "Use lixa fina (grão 120 ou mais). Acabamento conta 20% da nota (estética).", foco="AB", dist=1300)

def unit(v):
    L = math.sqrt(sum(c * c for c in v)); return [c / L for c in v]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

def peca_mundo(cap, nome, o, u, v, n, comp, larg, txt, det, cola, tipo, g="W"):
    poly = [[0, -larg / 2], [comp, -larg / 2], [comp, larg / 2], [0, larg / 2]]
    p = dict(nome=nome, poly=poly, eixo=(1, 0), tipo=tipo)
    fr = dict(o=[round(c, 4) for c in o], u=[round(c, 6) for c in u], v=[round(c, 6) for c in v], n=[round(c, 6) for c in n])
    return peca(g, cap, p, txt, det, cola, frame=fr)

def barra_longa(cap, nome_base, P0, d, v, n, L, camadas_n, txt_base, det, tipo, g="W", pos_cola=None, sobe=True):
    """Barra transversal maior que um palito: camadas empilhadas (para cima ou para baixo), cada uma em peças
    com emendas desencontradas. n é sempre a normal da face de cima da peça."""
    out = []
    for k in range(camadas_n):
        first = L / 3 if k % 2 == 0 else L / 6
        trechos = emendas(0, L, first, passo=L / 3 if L / 3 <= L_UTIL else L_UTIL - 2, minimo=20)
        for i, (a, b) in enumerate(trechos):
            o = [P0[c] + d[c] * a + (1 if sobe else -1) * n[c] * T * k for c in range(3)]
            cola = (pos_cola or ("pontas" if k == 0 else "toda"))
            out.append(peca_mundo(cap, f"{nome_base}, camada {k+1}, peça {i+1} de {len(trechos)}", o, d, v, n, b - a, W,
                                  f"{nome_base}, camada {k+1}, peça {i+1} de {len(trechos)}: corte {fmt1(b - a)} mm. {txt_base}",
                                  det, cola, tipo, g=g))
    return out

# espaçadores provisórios de palito (2 blocos), montados na mesa; grupo "E" = posição final entre as treliças
X_ESP = (150.0, 650.0)            # no meio dos painéis b1-b2 e b6-b7, fora das chapas
Z_IN_A, Z_IN_B = ZA + 8.0, ZB + 2.0    # faces internas dos banzos (sem chapa): -102 e 102
L_ESP = Z_IN_B - Z_IN_A           # 204 mm
for e, xc in enumerate(X_ESP):
    barra_longa("Espaçadores provisórios", f"Espaçador {e+1}", [xc, Y0 - W / 2, Z_IN_A], [0, 0, 1], [1, 0, 0], [0, 1, 0],
                L_ESP, 4, "Cole camada sobre camada, com as emendas desencontradas.",
                f"Feito só de palito e cola. É provisório: não é colado na ponte, só segura as duas treliças paralelas. "
                f"Comprimento total {fmt1(L_ESP)} mm (distância entre as faces dos banzos).", "espacador", g="E")
evento("secaE", "Espaçadores provisórios", "Deixe os dois espaçadores secarem por pelo menos 1 h.",
       "Eles só seguram as treliças no lugar, então não precisam das 24 h de cura da ponte.", foco="espacadores", dist=700)
evento("levantaA", "Montagem 3D", "Coloque a treliça A de pé sobre os apoios.",
       "A face com as chapas da face de cima fica virada para dentro da ponte.", foco="ponte", dist=1300)
evento("levantaB", "Montagem 3D", "Coloque a treliça B de pé, paralela à A, com 210 mm entre os eixos (220 mm por fora).",
       "Os espaçadores de palito entram no próximo passo para garantir essa distância. A largura tem de ficar entre 200 e 250 mm (regulamento).",
       foco="ponte", dist=1300)
evento("colocaE", "Montagem 3D", "Encaixe os dois espaçadores de palito entre os banzos inferiores, sem cola.",
       "Um no meio do painel b1-b2 e outro no meio do painel b6-b7, fora das chapas. Confira o esquadro nas duas pontas antes de colar qualquer peça.",
       foco="ponte", dist=1300)

ZMIN, ZMAX = ZA, ZB + 10.0
yb = Y0 - W / 2
# transversinas inferiores (2 camadas) em todos os nós do banzo inferior menos o central
for i in range(NP + 1):
    if i == NP // 2: continue
    x = i * A_PAINEL
    barra_longa("Transversinas inferiores", f"Transversina inferior do nó b{i}", [x, yb - 2.0, ZMIN], [0, 0, 1], [1, 0, 0], [0, 1, 0],
                LARG_TOTAL, 2, f"Cole por baixo dos dois banzos, no nó b{i}.",
                "Dica: é mais fácil colar com a ponte de cabeça para baixo. Comprimento total 220 mm, de uma face externa à outra.",
                "transversina", sobe=False)
# contraventamento inferior em zigue-zague (1 diagonal de 2 camadas por painel), por baixo dos banzos
for i in range(NP):
    x0, x1 = i * A_PAINEL + 12, (i + 1) * A_PAINEL - 12
    za, zb = (ZA + 5, ZB + 5) if i % 2 == 0 else (ZB + 5, ZA + 5)
    P0, P1 = [x0, yb - 2.0, za], [x1, yb - 2.0, zb]
    d = unit([P1[0] - P0[0], 0, P1[2] - P0[2]])
    L = math.hypot(P1[0] - P0[0], P1[2] - P0[2]) + 6
    o = [P0[0] - 3 * d[0], P0[1], P0[2] - 3 * d[2]]
    barra_longa("Contraventamento inferior", f"Diagonal inferior do painel {i+1}", o, d, cross([0, 1, 0], d), [0, 1, 0], L, 2,
                "Cole por baixo dos banzos, entre as transversinas.",
                "Diagonais alternadas (zigue-zague) travam a ponte contra torção, que encerra o ensaio pelo regulamento.", "contravento",
                sobe=False)
# escoras superiores (2 camadas) sobre o banzo superior nos nós t1..t7
ytop = Y0 + H + W / 2
for i in range(1, NP):
    x = i * A_PAINEL
    barra_longa("Escoras superiores", f"Escora superior do nó t{i}", [x, ytop, ZMIN], [0, 0, 1], [1, 0, 0], [0, 1, 0],
                LARG_TOTAL, 2, f"Cole por cima dos dois banzos superiores, no nó t{i}.",
                "Trava os nós do banzo superior. Sem ela, o banzo flamba de lado (hipótese do cálculo).", "escora")
# contraventamento superior em zigue-zague nos painéis t1-t2 ... t6-t7
for i in range(1, NP - 1):
    x0, x1 = i * A_PAINEL + 12, (i + 1) * A_PAINEL - 12
    za, zb = (ZA + 5, ZB + 5) if i % 2 == 0 else (ZB + 5, ZA + 5)
    P0, P1 = [x0, ytop, za], [x1, ytop, zb]
    d = unit([P1[0] - P0[0], 0, P1[2] - P0[2]])
    L = math.hypot(P1[0] - P0[0], P1[2] - P0[2]) + 6
    o = [P0[0] - 3 * d[0], P0[1], P0[2] - 3 * d[2]]
    barra_longa("Contraventamento superior", f"Diagonal superior do painel t{i}-t{i+1}", o, d, cross([0, 1, 0], d), [0, 1, 0], L, 2,
                "Cole sobre os banzos superiores, entre as escoras.",
                "Fecha o travamento do plano de cima. Confira que a ponte não ficou torta antes de colar.", "contravento")

# consolos (3 camadas, 30 mm) nas faces internas do nó b4 e mini-treliça transversal que recebe a haste de carga
xc = VAO / 2
ZI_A, ZI_B = ZA + 10.0, ZB             # faces internas das chapas: -100 e 100
for lado, zface, sgn in (("A", ZI_A, 1), ("B", ZI_B, -1)):
    for k in range(3):
        peca_mundo("Ponto de carga", f"Consolo da treliça {lado}, camada {k+1}", [xc - 15, Y0, zface + sgn * 2.0 * k],
                   [1, 0, 0], [0, sgn, 0], [0, 0, sgn], 30.0, W,
                   f"Consolo da treliça {lado}, camada {k+1}: corte 30,0 mm e cole na face interna do nó b4, alinhado com o banzo.",
                   "Os consolos sustentam a mini-treliça do ponto de carga. O topo deles fica na altura do topo do banzo.",
                   "toda", "consolo")
# mini-treliça no plano x = 400 (3 camadas empilhadas em x), vão entre as faces internas (200 mm), altura 50 mm
YB_M = Y0 + W / 2 + W / 2          # eixo do banzo de baixo da mini-treliça (apoiado nos consolos)
DM = 70.0                          # altura da mini-treliça (eixo a eixo)
PZ = [ZI_A + W / 2, -50.0, 0.0, 50.0, ZI_B - W / 2]      # nós (montantes) ao longo da largura
def mini_pecas():
    pcs = []
    INFm, SUPm = ((ZI_A, YB_M), (1.0, 0.0)), ((ZI_A, YB_M + DM), (1.0, 0.0))
    for k in range(3):
        xk = xc + 3.0 - 2.0 * k
        fr = dict(o=[xk, 0, 0], u=[0, 0, 1], v=[0, 1, 0], n=[-1, 0, 0])
        for nome, lin in (("banzo de baixo", INFm), ("banzo de cima", SUPm)):
            trechos = emendas(0, ZI_B - ZI_A, {0: 33.3, 1: 66.7, 2: 100.0}[k], passo=100.0)
            for i, (a, b) in enumerate(trechos):
                pcs.append((k, dict(nome=f"Mini-treliça, {nome}, camada {k+1}, peça {i+1} de {len(trechos)}",
                                    poly=faixa(lin[0], lin[1], a, b), eixo=(1.0, 0.0), tipo="transversina"), fr))
        dentro = [acima_de(INFm, W / 2), abaixo_de(SUPm, -W / 2)]
        for zz in PZ:
            p = recorta(faixa((zz, YB_M), (0.0, 1.0), -10, DM + 10), dentro)
            if p: pcs.append((k, dict(nome=f"Mini-treliça, montante em z={fmt1(zz)}, camada {k+1}", poly=p, eixo=(0.0, 1.0),
                                      tipo="transversina"), fr))
        for z0, z1 in ((PZ[0], PZ[1]), (PZ[1], PZ[2]), (PZ[4], PZ[3]), (PZ[3], PZ[2])):
            Pt, Pb = (z0, YB_M + DM), (z1, YB_M)
            dd = (Pb[0] - Pt[0], Pb[1] - Pt[1]); L = math.hypot(*dd); dd = (dd[0] / L, dd[1] / L)
            pl = dentro + [(1, 0, max(z0, z1) - W / 2), (-1, 0, -(min(z0, z1) + W / 2))]
            p = recorta(faixa(Pt, dd, -15, L + 15), pl)
            if p: pcs.append((k, dict(nome=f"Mini-treliça, diagonal, camada {k+1}", poly=p, eixo=dd, tipo="transversina"), fr))
    # chapas da mini-treliça nas duas faces: peça sobre o banzo + 3 faixas sobre as pontas das barras, em cada nó
    for face, (x_face, sgn) in enumerate(((xc + 5.0, -1), (xc - 3.0, -1))):
        fr = dict(o=[x_face, 0, 0], u=[0, 0, 1], v=[0, 1, 0], n=[-1, 0, 0])
        k_ordem = -1 if face == 0 else 3          # face +x vai antes da camada 1; face -x depois da camada 3
        limite = [(1, 0, ZI_B), (-1, 0, -ZI_A)]
        for zz in PZ:
            for nome, y_chapa, dy in (("de baixo", YB_M, 1), ("de cima", YB_M + DM, -1)):
                pecas_no = [("sobre o banzo", faixa((zz, y_chapa), (1.0, 0.0), -20, 20))]
                for fx in (1, 2, 3):
                    pecas_no.append((f"faixa {fx}", faixa((zz, y_chapa + dy * fx * W), (1.0, 0.0), -20, 20)))
                for i, (onde, p) in enumerate(pecas_no):
                    p = recorta(p, limite)
                    if p and area(p) >= 80:
                        pcs.append((k_ordem, dict(nome=f"Mini-treliça, chapa do nó z={fmt1(zz)} {nome}, face {face+1}, {onde}",
                                                  poly=p, eixo=(1.0, 0.0), tipo="chapa"), fr))
    pcs.sort(key=lambda t: t[0])
    return pcs
for k, p, fr in mini_pecas():
    comp_ = extensao(p['poly'], p['eixo'])[1] - extensao(p['poly'], p['eixo'])[0]
    if k == -1:
        txt, cola = f"{p['nome']}: corte {fmt1(comp_)} mm e coloque sobre o plástico, sem cola.", []
    else:
        txt, cola = f"{p['nome']}: corte {fmt1(comp_)} mm" + (" e cole sobre a camada anterior." if k else ", cole onde apoia nas chapas."), ("toda" if k else "pontas")
    peca("W", "Ponto de carga", p, txt,
         "A mini-treliça leva a carga da haste de aço até as duas treliças. Monte deitada sobre o plástico (chapas, 3 camadas, chapas) e depois encaixe entre os consolos.",
         cola, frame=fr)
evento("tiraesp", "Finalização", "Retire os dois espaçadores de palito.",
       "Eles só seguravam as treliças paralelas durante a colagem. Agora a ponte já está travada pelas transversinas, escoras e diagonais.",
       foco="ponte", dist=1300)
evento("curafinal", "Finalização", "Deixe a ponte inteira secar até a hora da entrega.",
       "Quanto mais tempo de cura, mais forte. Não teste a ponte antes da competição.", foco="ponte", dist=1300)
evento("pesagem", "Finalização", "Pese a ponte e confira as medidas: comprimento 1020 mm, largura 220 mm, altura até 300 mm, peso até 1 kg.", "", foco="ponte", dist=1300)
evento("ensaio", "Ensaio", "Na competição, a haste de aço é pendurada no meio da mini-treliça e a carga sobe a partir de 10 kg.",
       "Peça incrementos pequenos depois dos 30 kg (bônus). Use luvas e óculos de proteção, como manda o regulamento.", foco="ponte", dist=1400)

# ---------------------------------------------------------------- numeração e tipos de peça (manual estilo LEGO)
CAT = {"banzo": ("B", "Banzo"), "diagonal": ("D", "Diagonal"), "montante": ("M", "Montante"), "chapa": ("C", "Chapa de ligação"),
       "transversina": ("T", "Transversina"), "escora": ("E", "Escora superior"), "contravento": ("X", "Diagonal de contraventamento"),
       "consolo": ("K", "Consolo"), "espacador": ("P", "Espaçador provisório")}
ORDEM_CAT = list(CAT)

def forma_canonica(p):
    """Contorno da peça no próprio eixo (x ao longo do palito, y na largura), normalizado para que peças iguais
    (mesmo comprimento e mesmos cortes, mesmo que viradas) tenham a mesma chave."""
    ang = math.atan2(p["ax"][1], p["ax"][0]); c, s_ = math.cos(-ang), math.sin(-ang)
    r = [(x * c - y * s_, x * s_ + y * c) for x, y in p["poly"]]
    x0 = min(q[0] for q in r); vc = (max(q[1] for q in r) + min(q[1] for q in r)) / 2
    r = [(x - x0, y - vc) for x, y in r]; L = max(q[0] for q in r)
    melhor = None
    for fx in (1, -1):
        for fy in (1, -1):
            q = [(round(((x if fx > 0 else L - x)) / .5) * .5 + 0.0, round(y * fy / .5) * .5 + 0.0) for x, y in r]
            q2 = []
            for v in q:
                if not q2 or v != q2[-1]: q2.append(v)
            if len(q2) > 1 and q2[0] == q2[-1]: q2.pop()
            a = sum(q2[i][0] * q2[(i + 1) % len(q2)][1] - q2[(i + 1) % len(q2)][0] * q2[i][1] for i in range(len(q2)))
            if a < 0: q2 = q2[::-1]
            i0 = q2.index(min(q2)); q2 = q2[i0:] + q2[:i0]
            k = tuple(q2)
            if melhor is None or k < melhor: melhor = k
    return melhor

def contorno_exato(p):
    """Contorno sem arredondar, no eixo do próprio palito: x de 0 a L, y centrado (-4,2 a 4,2)."""
    ang = math.atan2(p["ax"][1], p["ax"][0]); c, s_ = math.cos(-ang), math.sin(-ang)
    r = [(x * c - y * s_, x * s_ + y * c) for x, y in p["poly"]]
    x0 = min(q[0] for q in r); vc = (max(q[1] for q in r) + min(q[1] for q in r)) / 2
    r = [(x - x0, y - vc) for x, y in r]
    q2 = []
    for v in r:
        if not q2 or math.hypot(v[0] - q2[-1][0], v[1] - q2[-1][1]) > .05: q2.append(v)
    if len(q2) > 1 and math.hypot(q2[0][0] - q2[-1][0], q2[0][1] - q2[-1][1]) < .05: q2.pop()
    return q2

def dados_corte(p):
    """Comprimento total, comprimento de cada borda longa e ângulo de cada corte (medido entre o corte e a borda)."""
    pts = contorno_exato(p); n = len(pts); L = max(x for x, _ in pts)
    bordas, pontas = [], {"esq": [], "dir": []}
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        if abs(y1 - y2) < .05 and abs(abs(y1) - W / 2) < .3:
            bordas.append(abs(x2 - x1))
        else:
            ang = math.degrees(math.atan2(abs(y2 - y1), abs(x2 - x1)))
            pontas["esq" if (x1 + x2) / 2 < L / 2 else "dir"].append(round(ang, 1))
    bordas = sorted(bordas, reverse=True)[:2] + [0.0] * max(0, 2 - len(bordas))
    if len(pontas["esq"]) > len(pontas["dir"]) or (len(pontas["esq"]) == len(pontas["dir"]) and pontas["esq"] < pontas["dir"]):
        pontas["esq"], pontas["dir"] = pontas["dir"], pontas["esq"]      # ponta mais simples à esquerda
        pts = [(L - x, y) for x, y in pts]
    return dict(L=round(L, 1), bordaA=round(bordas[0], 1), bordaB=round(bordas[1], 1), esq=pontas["esq"], dir=pontas["dir"],
                poly=[[round(x, 2), round(y, 2)] for x, y in pts])

# ---------------------------------------------------------------- numeração travada
# As peças já foram cortadas e numeradas com o manual de corte enviado em 15/11 (commit e90e7b9).
# Os números ficam congelados em projeto/manual/numeracao_corte.json: dentro de cada etapa, as peças seguem essa ordem.
ARQ_NUM = os.path.join(D, "manual", "numeracao_corte.json")
TRAVA = json.load(open(ARQ_NUM))["numeros"] if os.path.exists(ARQ_NUM) else None
if TRAVA:
    _cont = {}
    for p in passos:
        if p["k"] != "pc": continue
        k = (p["g"], p["nome"]); _cont[k] = _cont.get(k, 0) + 1
        p["_trava"] = TRAVA.get(f"{p['g']}|{p['nome']}|{_cont[k]}")
    i = 0
    while i < len(passos):
        if passos[i]["k"] != "pc": i += 1; continue
        j = i
        while j < len(passos) and passos[j]["k"] == "pc" and passos[j]["cap"] == passos[i]["cap"]: j += 1
        if all(p["_trava"] is not None for p in passos[i:j]):
            passos[i:j] = sorted(passos[i:j], key=lambda p: p["_trava"])
        i = j

pecas_todas = [p for p in passos if p["k"] == "pc"]
grupos_forma = {}
for p in pecas_todas:
    grupos_forma.setdefault((p["tipo"], forma_canonica(p)), []).append(p)
tipos = []
for cat in ORDEM_CAT:
    ks = [k for k in grupos_forma if k[0] == cat]
    ks.sort(key=lambda k: (-max(x for x, _ in k[1]), k[1]))
    for i, k in enumerate(ks):
        cod = f"{CAT[cat][0]}{i+1}"
        info = dados_corte(grupos_forma[k][0])
        for p in grupos_forma[k]: p["cod"] = cod
        tipos.append(dict(cod=cod, cat=cat, nome_cat=CAT[cat][1], qtd=len(grupos_forma[k]), **info))
for i, p in enumerate(pecas_todas): p["num"] = i + 1
if TRAVA:
    difs = [p["nome"] for p in pecas_todas if p.pop("_trava", None) != p["num"]]
    if difs: raise SystemExit(f"Numeração diferente da que já foi cortada em {len(difs)} peças, ex.: {difs[:3]}")
for t in tipos: t["nums"] = [p["num"] for p in pecas_todas if p["cod"] == t["cod"]]

def desc_ponta(angs):
    if not angs: return "sem corte"
    if len(angs) == 1: return "reta (90°)" if abs(angs[0] - 90) < .3 else f"inclinada a {fmt1(angs[0])}°"
    return "em bico: " + " e ".join(f"{fmt1(a)}°" for a in angs)
for t in tipos:
    t["txt_esq"], t["txt_dir"] = desc_ponta(t["esq"]), desc_ponta(t["dir"])

# ---------------------------------------------------------------- lista de corte, cola e orçamento
todas = [p for p in passos if p["k"] == "pc"]
pcs = [p for p in todas if p["g"] != "E"]          # só a ponte (os espaçadores são provisórios)
esp = [p for p in todas if p["g"] == "E"]
comps = sorted((p["comp"] for p in pcs), reverse=True)
sobras = []                     # first-fit decreasing em palitos de comprimento útil L_UTIL
for c in comps:
    for i, s in enumerate(sobras):
        if s >= c + 0.5:
            sobras[i] = s - c - 0.5; break
    else:
        sobras.append(L_UTIL - c - 0.5)
n_palitos_ponte = len(sobras)
area_cola = 0.0
for p in todas:
    if p["cola"] == "toda": area_cola += p["area"]
    elif p["cola"] == "pontas": area_cola += min(p["area"], 2 * 15 * W)
g_cola = area_cola / 100.0 * 0.02 * 1.0      # área em cm² x 0,02 g/cm² (200 g/m², limite alto da ficha técnica)
g_cola_compra = g_cola * 3                    # perdas, frasco, excesso que escorre
palitos_ensaio = 10 + 20 + 20                 # tração, pares de flambagem, juntas coladas
palitos_esp = len(esp)                        # 1 peça de 74 mm por palito
total_palitos = math.ceil((n_palitos_ponte + palitos_ensaio + palitos_esp) * 1.15)
area_cola_ponte = sum(p["area"] if p["cola"] == "toda" else min(p["area"], 2 * 15 * W) if p["cola"] == "pontas" else 0 for p in pcs)
massa_g = sum(p["area"] * T for p in pcs) * 560e-9 * 1000 + area_cola_ponte / 100 * 0.02 * 0.5   # madeira + resíduo seco de cola

# lista de corte agrupada
grupos = {}
for p in todas:
    k = (round(p["comp"]), p["tipo"])
    grupos[k] = grupos.get(k, 0) + 1
lista = sorted(((c, t, n) for (c, t), n in grupos.items()), key=lambda x: (-x[0], x[1]))

resumo = dict(pecas=len(pcs), pecas_esp=len(esp), passos=len(passos), palitos_ponte=n_palitos_ponte,
              palitos_ensaio=palitos_ensaio, palitos_esp=palitos_esp,
              palitos_comprar=total_palitos, area_cola_cm2=round(area_cola / 100, 5), cola_g=round(g_cola, 5),
              cola_comprar_g=round(g_cola_compra, 5), massa_g=round(massa_g, 5), lista=lista)
NOS_LOCAIS = {k: list(v) for k, v in NOS.items()}
dados = dict(passos=passos, resumo=resumo, tipos=tipos, nos=NOS_LOCAIS, barras=[[b["i"], b["j"]] for b in m["barras"]],
             const=dict(W=W, T=T, Y0=Y0, ZA=ZA, ZB=ZB, VAO=VAO, H=H, BAL=BALANCO, LARG=LARG_TOTAL, XC=VAO / 2, YBM=YB_M, DM=DM))
json.dump(dados, open(os.path.join(D, "montagem.json"), "w"), ensure_ascii=False)
print(json.dumps({k: v for k, v in resumo.items() if k != "lista"}, ensure_ascii=False, indent=1))
for c, t, n in lista: print(f"  {c:>4} mm  {t:12} x{n}")

modelo = os.path.join(D, "montagem_modelo.html")
if os.path.exists(modelo):
    html = (open(modelo).read().replace("__NAVEGADOR__", open(os.path.join(D, "navegador.js")).read())
            .replace("__NPECAS__", str(len(pecas_todas)))
            .replace("__DADOS__", json.dumps(dados, ensure_ascii=False, separators=(",", ":"))))
    os.makedirs(os.path.join(D, "..", "site"), exist_ok=True)
    open(os.path.join(D, "..", "site", "montagem.html"), "w").write(html)
    print("site/montagem.html", len(html), "bytes")
