#!/usr/bin/env python3
"""Modelo físico da ponte palito por palito + sequência de montagem + lista de corte + orçamento.

Gera projeto/montagem.json e site/montagem.html (a partir de projeto/montagem_modelo.html).

Convenções (mm):
- Cada treliça é montada deitada sobre o gabarito. Coordenadas locais da treliça: x ao longo do vão,
  y para cima no plano da treliça, z = espessura (empilhamento das camadas).
- Camadas em z: chapas da face 1 [0,2], camada 1 [2,4], camada 2 [4,6], camada 3 [6,8], chapas da face 2 [8,10].
- Todas as barras têm 3 camadas (núcleo de 6 mm), para que as chapas das duas faces fiquem planas.
- Mundo (ponte de pé): x ao longo do vão, y para cima, z na largura. Treliça A em z = -5..5, B em z = 75..85.
"""
import json, math, os

D = os.path.dirname(os.path.abspath(__file__))
m = json.load(open(os.path.join(D, "ponte_parker_8x90.json")))
W, T = 8.4, 2.0                  # largura e espessura do palito
L_PALITO, L_UTIL = 110.0, 101.6  # comprimento total e reto útil (sem as pontas arredondadas)
VAO, H, NP = 500.0, 90.0, 8
A_PAINEL = VAO / NP
BALANCO = 15.0                   # banzo inferior passa 15 mm além de cada apoio
GAP = 0.3                        # folga visível nas emendas de topo
TH = math.atan2(H, VAO / 2)      # inclinação do banzo superior
LADO = math.hypot(VAO / 2, H)    # comprimento de cada metade do banzo superior
Y0 = 268.2                       # altura do eixo do banzo inferior com a ponte de pé sobre os apoios
ZA, ZB = -5.0, 75.0              # posição (z do mundo) da face 1 de cada treliça em pé

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

# linhas dos banzos: (origem, direção unitária); semi-planos "abaixo/acima" de cada borda
ESQ = ((0.0, 0.0), (math.cos(TH), math.sin(TH)))             # metade esquerda do banzo superior
DIR = ((VAO, 0.0), (-math.cos(TH), math.sin(TH)))            # metade direita (orientada do apoio para o topo)
INF = ((-BALANCO, 0.0), (1.0, 0.0))

def lado_normal(linha):
    (px, py), (dx, dy) = linha
    nx, ny = -dy, dx               # normal à esquerda da direção
    if ny < 0: nx, ny = -nx, -ny   # normal apontando para cima
    return nx, ny, nx * px + ny * py

def abaixo_de(linha, off):
    """semi-plano: distância (com sinal, normal para cima) ao eixo <= off"""
    nx, ny, c = lado_normal(linha)
    return (nx, ny, c + off)

def acima_de(linha, off):
    nx, ny, c = lado_normal(linha)
    return (-nx, -ny, -(c + off))

def ao_longo(linha, s0, s1):
    """semi-planos que limitam o trecho s em [s0, s1] da linha"""
    (px, py), (dx, dy) = linha
    c0 = dx * px + dy * py
    return [(-dx, -dy, -(c0 + s0)), (dx, dy, c0 + s1)]

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
    if len(cortes) > 2 and cortes[-1] - cortes[-2] < minimo:   # evita peça final minúscula
        cortes[-2] = (cortes[-3] + cortes[-1]) / 2 if cortes[-1] - cortes[-3] <= passo else cortes[-1] - minimo
    return [(cortes[i], cortes[i + 1]) for i in range(len(cortes) - 1)]

# ---------------------------------------------------------------- peças de uma treliça
NOS = {k: tuple(v) for k, v in m["nos"].items()}
def no(k): return NOS[k]

def pecas_trelica():
    """Lista de peças (no referencial local da treliça), agrupadas por camada, na ordem de montagem."""
    camadas = {"f1": [], "L1": [], "L2": [], "L3": [], "f2": []}
    off_emenda = {"L1": 100.0, "L2": 66.67, "L3": 33.33}
    for k, cam in enumerate(("L1", "L2", "L3")):
        z0 = 2.0 + 2.0 * k
        passa = (k != 1)     # camadas 1 e 3: banzo inferior e metade esquerda passam; camada 2: o contrário
        # banzo inferior
        planos_inf = []
        if not passa:        # camada 2: o banzo superior passa no apoio; o inferior começa depois dele
            planos_inf = [abaixo_de(ESQ, -W / 2), abaixo_de(DIR, -W / 2)]
        trechos = emendas(-BALANCO, VAO + BALANCO, off_emenda[cam])
        for i, (a, b) in enumerate(trechos):
            p = faixa(INF[0], INF[1], a + (GAP if i else 0), b)
            p = recorta(p, planos_inf)
            if p: camadas[cam].append(dict(nome=f"Banzo inferior, camada {k+1}, peça {i+1} de {len(trechos)}",
                                           poly=p, z0=z0, eixo=INF[1], tipo="banzo"))
        # banzo superior: duas metades retas
        for lado, linha, outra in (("esquerda", ESQ, DIR), ("direita", DIR, ESQ)):
            planos = []
            pa = (lado == "esquerda") == passa       # esta metade passa no topo?
            if passa:   # banzo inferior passa: a metade começa acima dele
                planos.append(acima_de(INF, W / 2))
                s_ini = 0.0
            else:       # metade passa até a ponta, cortada no fundo do banzo inferior e no fim do balanço
                planos += [acima_de(INF, -W / 2), (-1, 0, BALANCO) if lado == "esquerda" else (1, 0, VAO + BALANCO)]
                s_ini = -BALANCO / math.cos(TH) - 2
            if pa:      # passa no topo: estende e corta rente à face de cima da outra metade
                planos.append(abaixo_de(outra, W / 2)); s_fim = LADO + 15
            else:       # termina contra a face de baixo da outra metade
                planos.append(abaixo_de(outra, -W / 2)); s_fim = LADO
            trechos = emendas(s_ini, s_fim, off_emenda[cam] - s_ini * 0)
            for i, (a, b) in enumerate(trechos):
                p = faixa(linha[0], linha[1], a + (GAP if i else 0), b)
                p = recorta(p, planos)
                if p: camadas[cam].append(dict(nome=f"Banzo superior ({lado}), camada {k+1}, peça {i+1} de {len(trechos)}",
                                               poly=p, z0=z0, eixo=linha[1], tipo="banzo"))
        # barras de alma: recortadas pelos banzos; diagonais recortadas pelo montante do mesmo nó
        for bar in m["barras"]:
            i, j = bar["i"], bar["j"]
            if i[0] == j[0] or bar["id"] in ("b0-t1", "t7-b8"): continue   # banzos já feitos
            P, Q = no(i), no(j)
            d = (Q[0] - P[0], Q[1] - P[1]); L = math.hypot(*d); d = (d[0] / L, d[1] / L)
            p = faixa(P, d, -20, L + 20)
            planos = [acima_de(INF, W / 2), abaixo_de(ESQ, -W / 2), abaixo_de(DIR, -W / 2)]
            if abs(d[0]) > 1e-6:      # diagonal: não invade o montante dos nós das pontas
                for nk in (i, j):
                    x = no(nk)[0]
                    outro = Q if nk == i else P
                    planos.append((1, 0, x - W / 2) if outro[0] < x else (-1, 0, -(x + W / 2)))
            p = recorta(p, planos)
            tipo = "montante" if abs(d[0]) < 1e-6 else "diagonal"
            if p: camadas[cam].append(dict(nome=f"{tipo.capitalize()} {bar['id']}, camada {k+1}", poly=p, z0=z0,
                                           eixo=d, tipo=tipo, barra=bar["id"]))
    # chapas de ligação (2 faces), 40 mm por peça
    def chapas(z0, face):
        out = []
        for nk, (x, y) in NOS.items():
            pc = []
            if nk in ("b0", f"b{NP}"):
                sx = 1 if nk == "b0" else -1
                a, b = (-BALANCO, 25) if sx == 1 else (VAO - 25, VAO + BALANCO)
                pc.append(("ao longo do banzo inferior", faixa(INF[0], INF[1], a, b), INF[1], []))
                lin = ESQ if sx == 1 else DIR
                pc.append(("ao longo do banzo superior", faixa(lin[0], lin[1], 8, 48), lin[1], [acima_de(INF, W / 2)]))
            elif nk.startswith("b"):
                pc.append(("sobre o banzo", faixa((x, 0), (1, 0), -20, 20), (1, 0), []))
                for fx in (1, 2):   # 2 faixas: 16,8 mm de sobreposição nas pontas das barras (cálculo pede 13,4 mm)
                    pc.append((f"faixa {fx} sobre as pontas das barras", faixa((x, fx * W), (1, 0), -20, 20), (1, 0),
                               [abaixo_de(ESQ, -W / 2), abaixo_de(DIR, -W / 2)]))
            elif nk == f"t{NP//2}":
                s = LADO
                pc.append(("sobre a metade esquerda", faixa(ESQ[0], ESQ[1], s - 30, s + 15), ESQ[1], [abaixo_de(DIR, W / 2)]))
                pc.append(("sobre a metade direita", faixa(DIR[0], DIR[1], s - 30, s), DIR[1], [abaixo_de(ESQ, -W / 2)]))
                pc.append(("sobre o montante", faixa((x, y), (0, -1), 0, 46), (0, -1),
                           [abaixo_de(ESQ, -W / 2), abaixo_de(DIR, -W / 2)]))
            else:
                lin = ESQ if x < VAO / 2 else DIR
                s = math.hypot(x - lin[0][0], y - lin[0][1])
                nx, ny, _ = lado_normal(lin)
                pc.append(("sobre o banzo", faixa(lin[0], lin[1], s - 20, s + 20), lin[1], []))
                for fx in (1, 2):   # faixas abaixo do banzo superior, sem invadir as faixas dos nós de baixo
                    base = (lin[0][0] - fx * W * nx, lin[0][1] - fx * W * ny)
                    pc.append((f"faixa {fx} sobre as pontas das barras", faixa(base, lin[1], s - 20, s + 20), lin[1],
                               [acima_de(INF, W / 2 + 2 * W)]))
            for i, (onde, p, eixo, planos) in enumerate(pc):
                p = recorta(p, planos)
                if p: out.append(dict(nome=f"Chapa do nó {nk}, face {face}, peça {i+1} de {len(pc)} ({onde})",
                                      poly=p, z0=z0, eixo=eixo, tipo="chapa", no=nk))
        return out
    camadas["f1"] = chapas(0.0, 1)
    camadas["f2"] = chapas(8.0, 2)
    # ordem dentro de cada camada: da esquerda para a direita
    for k in camadas:
        camadas[k].sort(key=lambda p: (0 if p["tipo"] in ("banzo", "chapa") else 1,
                                       sum(q[0] for q in p["poly"]) / len(p["poly"])))
    return camadas

# ---------------------------------------------------------------- sequência
passos = []   # cada passo: evento ou peça
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

evento("gabarito", "Preparação", "Imprima o gabarito em tamanho real e prenda na mesa com fita.",
       "Confira a escala: a régua do gabarito tem que medir exatamente 100 mm.", foco="mesa", dist=900)
evento("filme", "Preparação", "Cubra o gabarito com plástico de polietileno (saco plástico transparente bem esticado).",
       "A cola branca não adere ao polietileno (ficha técnica da Cascorez Extra), então a treliça solta depois sem rasgar.",
       foco="mesa", dist=900)
evento("materiais", "Preparação", "Separe os palitos, a cola branca, o estilete, a régua e o esquadro.",
       "Escolha palitos retos e sem rachaduras. Descarte os empenados: eles atrapalham a colagem.", foco="materiais", dist=420)

for g in ("A", "B"):
    T_ = f"Treliça {g}"
    for cam in ("f1", "L1", "L2", "L3", "f2"):
        lst = camadas[cam]
        cap = f"{T_} · {NOME_CAM[cam]}"
        for p in lst:
            comp = extensao(p["poly"], p["eixo"])[1] - extensao(p["poly"], p["eixo"])[0]
            corte = f"Corte {fmt1(comp)} mm"
            if cam == "f1":
                txt = f"{p['nome']}: {corte.lower()} e coloque sobre o plástico, sem cola."
                cola = []
                det = "As chapas da face de baixo só ficam posicionadas; a cola entra quando a camada 1 for colocada por cima."
            elif cam == "L1":
                txt = f"{p['nome']}: {corte.lower()}, passe cola onde ela apoia nas chapas e encoste de topo nas peças vizinhas."
                cola = "pontas"
                det = "Pontas cortadas no ângulo marcado no gabarito. Encoste bem: fresta na emenda vira ponto fraco."
            elif cam in ("L2", "L3"):
                txt = f"{p['nome']}: {corte.lower()}, passe um cordão contínuo de cola sobre a camada de baixo e pressione por 30 s."
                cola = "toda"
                det = ("As emendas desta camada ficam desencontradas pelo menos 30 mm das emendas da camada de baixo."
                       if p["tipo"] == "banzo" else "Alinhe as bordas com a camada de baixo antes de pressionar.")
            else:
                txt = f"{p['nome']}: {corte.lower()}, passe cola em toda a face e pressione por 30 s."
                cola = "toda"
                det = "Limpe o excesso de cola que escorrer pelas bordas com um palito, antes de secar."
            peca(g, cap, p, txt, f"{det} Comprimento: {fmt1(comp)} mm · espessura 2,0 mm · largura 8,4 mm.", cola)
    evento(f"prensa{g}", f"{T_} · prensagem", f"Cubra a treliça {g} com um plástico e uma tábua reta e coloque peso por cima (livros).",
           "Pressão uniforme deixa a linha de cola fina e forte. Não deslize a tábua: só apoie.", foco=g, dist=700)
    evento(f"cura{g}", f"{T_} · cura", f"Deixe a treliça {g} curar por 24 h sem mexer.",
           "A cola branca só atinge a resistência total depois de 24 h. Antes disso, não tire do gabarito.", foco=g, dist=700)

evento("desenforma", "Acabamento", "Retire as duas treliças do gabarito, puxando o plástico devagar.",
       "Se alguma peça descolar, recole e espere mais 24 h antes de continuar.", foco="AB", dist=900)
evento("lixa", "Acabamento", "Lixe de leve as rebarbas de cola das bordas, sem afinar os palitos.",
       "Use lixa fina (grão 120 ou mais). Lixar demais reduz a seção e a resistência.", foco="AB", dist=900)
evento("levantaA", "Montagem 3D", "Coloque a treliça A de pé sobre os apoios.",
       "A face com as chapas da face de cima fica virada para dentro da ponte.", foco="ponte", dist=900)
evento("levantaB", "Montagem 3D", "Coloque a treliça B de pé, paralela, com 80 mm entre os eixos.",
       "Coloque dois blocos espaçadores soltos (sem cola) de 74 mm entre os banzos inferiores, fora das chapas: "
       "um entre os nós b2 e b3 e outro entre b5 e b6. Eles não fazem parte da ponte e saem no fim. Confira o esquadro nas duas pontas.",
       foco="ponte", dist=900)

def peca_mundo(cap, nome, o, u, v, n, comp, larg, txt, det, cola, tipo, inteiro=False):
    """Peça retangular no referencial do mundo: origem o (meio da face de baixo, no início), eixo u, largura v, espessura n."""
    poly = [[0, -larg / 2], [comp, -larg / 2], [comp, larg / 2], [0, larg / 2]]
    p = dict(nome=nome, poly=poly, eixo=(1, 0), tipo=tipo, inteiro=inteiro)
    fr = dict(o=[round(c, 4) for c in o], u=[round(c, 6) for c in u], v=[round(c, 6) for c in v], n=[round(c, 6) for c in n])
    return peca("W", cap, p, txt, det, cola, frame=fr)

def unit(v):
    L = math.sqrt(sum(c * c for c in v)); return [c / L for c in v]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

ZMIN, ZMAX = ZA, ZB + 10.0        # faces externas: -5 e 85
LARG_TOTAL = ZMAX - ZMIN          # 90 mm
yb = Y0 - W / 2                   # face de baixo do banzo inferior
# transversinas inferiores (2 camadas) em todos os nós do banzo inferior menos o central
for k in range(2):
    for i in range(NP + 1):
        if i == NP // 2: continue
        x = i * A_PAINEL
        y = yb - 2.0 * (k + 1)
        peca_mundo("Transversinas inferiores", f"Transversina inferior do nó b{i}, camada {k+1}",
                   [x, y, ZMIN], [0, 0, 1], [1, 0, 0], [0, 1, 0], LARG_TOTAL, W,
                   f"Transversina inferior do nó b{i}, camada {k+1}: corte {fmt1(LARG_TOTAL)} mm e cole por baixo dos dois banzos, no nó b{i}.",
                   "Fica embaixo do banzo, centrada no nó, de uma face externa à outra (90,0 mm).", "pontas" if k == 0 else "toda",
                   "transversina")
# contraventamento inferior em zigue-zague (1 diagonal por painel), por baixo dos banzos
for i in range(NP):
    x0, x1 = i * A_PAINEL + 10, (i + 1) * A_PAINEL - 10
    za, zb = 0.0, 80.0
    if i % 2: za, zb = zb, za
    P0, P1 = [x0, yb - 2.0, za], [x1, yb - 2.0, zb]
    d = unit([P1[0] - P0[0], 0, P1[2] - P0[2]])
    L = math.hypot(P1[0] - P0[0], P1[2] - P0[2]) + 6
    o = [P0[0] - 3 * d[0], P0[1], P0[2] - 3 * d[2]]
    peca_mundo("Contraventamento inferior", f"Diagonal inferior do painel {i+1}", o, d, cross([0, 1, 0], d), [0, 1, 0], L, W,
               f"Diagonal inferior do painel {i+1}: corte {fmt1(L)} mm e cole por baixo dos banzos, entre as transversinas.",
               "Diagonais alternadas (zigue-zague) travam a ponte contra torção e deslocamento lateral.", "pontas", "contravento")
# escoras superiores (2 camadas) sobre o banzo superior nos nós t1..t7
def topo_no(i):
    """ponto na face de cima do banzo superior no nó t_i, direção v (ao longo do banzo) e normal n, com u = z."""
    x = i * A_PAINEL
    if i == NP // 2:
        return [x, Y0 + H + (W / 2) / math.cos(TH), 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]
    c, s_ = math.cos(TH), math.sin(TH)
    h_no = H * (1 - abs(x - VAO / 2) / (VAO / 2))
    if x < VAO / 2: v, n = [c, s_, 0.0], [-s_, c, 0.0]
    else:           v, n = [c, -s_, 0.0], [s_, c, 0.0]
    return [x + n[0] * W / 2, Y0 + h_no + n[1] * W / 2, 0.0], v, n
for k in range(2):
    for i in range(1, NP):
        o, vv, nn = topo_no(i)
        o2 = [o[0] + nn[0] * 2.0 * k, o[1] + nn[1] * 2.0 * k, ZMIN]
        peca_mundo("Escoras superiores", f"Escora superior do nó t{i}, camada {k+1}", o2, [0, 0, 1], vv, nn, LARG_TOTAL, W,
                   f"Escora superior do nó t{i}, camada {k+1}: corte {fmt1(LARG_TOTAL)} mm e cole por cima dos dois banzos superiores.",
                   "Trava os nós do banzo superior. Sem ela, o banzo flamba de lado (é a hipótese do cálculo).",
                   "pontas" if k == 0 else "toda", "escora")
# contraventamento superior em zigue-zague nos painéis t1-t2 ... t6-t7, na face de cima dos banzos
for i in range(1, NP - 1):
    xa, xb = i * A_PAINEL, (i + 1) * A_PAINEL
    c, s_ = math.cos(TH), math.sin(TH)
    esq = xb <= VAO / 2
    n = [-s_, c, 0.0] if esq else [s_, c, 0.0]
    def sup(x):
        h_x = H * (1 - abs(x - VAO / 2) / (VAO / 2))
        return [x + n[0] * W / 2, Y0 + h_x + n[1] * W / 2]
    dx = 12 * c
    p0, p1 = sup(xa + dx), sup(xb - dx)
    za, zb = (0.0, 80.0) if i % 2 == 0 else (80.0, 0.0)
    P0, P1 = [p0[0], p0[1], za], [p1[0], p1[1], zb]
    d = unit([P1[k] - P0[k] for k in range(3)])
    L = math.sqrt(sum((P1[k] - P0[k]) ** 2 for k in range(3))) + 6
    o = [P0[k] - 3 * d[k] for k in range(3)]
    peca_mundo("Contraventamento superior", f"Diagonal superior do painel t{i}-t{i+1}", o, d, unit(cross(n, d)), n, L, W,
               f"Diagonal superior do painel t{i}-t{i+1}: corte {fmt1(L)} mm e cole sobre os banzos superiores, entre as escoras.",
               "Fecha o travamento do plano de cima. Confira que a ponte não ficou torta antes de colar.", "pontas", "contravento")
# consolos (3 camadas, 30 mm) nas faces internas, no nó b4, e transversina central (2 x 10 camadas)
xc = VAO / 2
for lado, zface, sgn in (("A", ZA + 10.0, 1), ("B", ZB, -1)):
    for k in range(3):
        z = zface + sgn * 2.0 * k
        peca_mundo("Transversina central", f"Consolo da treliça {lado}, camada {k+1}", [xc - 15, Y0, z], [1, 0, 0], [0, sgn, 0],
                   [0, 0, sgn], 30.0, W,
                   f"Consolo da treliça {lado}, camada {k+1}: corte 30,0 mm e cole na face interna do nó b4, alinhado com o banzo.",
                   "Os consolos sustentam a transversina central. O topo deles fica na mesma altura do topo do banzo.",
                   "toda", "consolo")
for k in range(10):
    for s, xs in enumerate((xc - W / 2, xc + W / 2)):
        y = Y0 + W / 2 + 2.0 * k
        peca_mundo("Transversina central", f"Transversina central, camada {k+1} de 10, palito {s+1} de 2",
                   [xs, y, ZA + 10.0], [0, 0, 1], [1, 0, 0], [0, 1, 0], 70.0, W,
                   f"Transversina central, camada {k+1} de 10, palito {s+1}: corte 70,0 mm e cole {'sobre os consolos' if k == 0 else 'sobre a camada de baixo'}.",
                   "É aqui que a carga de 45 kg fica pendurada. Cole camada por camada, apertando bem cada uma.",
                   "pontas" if k == 0 else "toda", "transversina")
evento("tiraesp", "Finalização", "Retire os dois blocos espaçadores provisórios.", "Eles só seguravam as treliças paralelas durante a colagem. Agora a ponte já está travada pelas transversinas, escoras e diagonais.",
       foco="ponte", dist=900)
evento("curafinal", "Finalização", "Deixe a ponte inteira curar por mais 24 h.",
       "Só aplique carga depois desse tempo (recomendação do fabricante da cola).", foco="ponte", dist=900)
evento("pesagem", "Finalização", "Pese a ponte e anote a massa.", "", foco="ponte", dist=900)
evento("ensaio", "Ensaio", "Pendure a carga no meio da transversina central e aumente aos poucos até 45 kg.",
       "Carga aplicada devagar e centrada. Ninguém embaixo da carga. Use óculos de proteção.", foco="ponte", dist=1000)

# ---------------------------------------------------------------- lista de corte, cola e orçamento
pcs = [p for p in passos if p["k"] == "pc"]
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
for p in pcs:
    if p["cola"] == "toda": area_cola += p["area"]
    elif p["cola"] == "pontas": area_cola += min(p["area"], 2 * 15 * W)
g_cola = area_cola / 100.0 * 0.02 * 1.0      # área em cm² x 0,02 g/cm² (200 g/m², limite alto da ficha técnica)
g_cola_compra = g_cola * 3                    # perdas, frasco, excesso que escorre
palitos_ensaio = 10 + 20 + 20                 # tração, pares de flambagem, juntas coladas
total_palitos = math.ceil((n_palitos_ponte + palitos_ensaio) * 1.15)
massa_g = sum(p["area"] * T for p in pcs) * 560e-9 * 1000 + g_cola * 0.5   # madeira + resíduo seco de cola

# lista de corte agrupada
grupos = {}
for p in pcs:
    k = (round(p["comp"]), p["tipo"])
    grupos[k] = grupos.get(k, 0) + 1
lista = sorted(((c, t, n) for (c, t), n in grupos.items()), key=lambda x: (-x[0], x[1]))

resumo = dict(pecas=len(pcs), passos=len(passos), palitos_ponte=n_palitos_ponte, palitos_ensaio=palitos_ensaio,
              palitos_comprar=total_palitos, area_cola_cm2=round(area_cola / 100, 5), cola_g=round(g_cola, 5),
              cola_comprar_g=round(g_cola_compra, 5), massa_g=round(massa_g, 5), lista=lista)
NOS_LOCAIS = {k: list(v) for k, v in NOS.items()}
dados = dict(passos=passos, resumo=resumo, nos=NOS_LOCAIS, barras=[[b["i"], b["j"]] for b in m["barras"]],
             const=dict(W=W, T=T, Y0=Y0, ZA=ZA, ZB=ZB, VAO=VAO, H=H, BAL=BALANCO))
json.dump(dados, open(os.path.join(D, "montagem.json"), "w"), ensure_ascii=False)
print(json.dumps({k: v for k, v in resumo.items() if k != "lista"}, ensure_ascii=False, indent=1))
for c, t, n in lista: print(f"  {c:>4} mm  {t:12} x{n}")

modelo = os.path.join(D, "montagem_modelo.html")
if os.path.exists(modelo):
    html = open(modelo).read().replace("__DADOS__", json.dumps(dados, ensure_ascii=False, separators=(",", ":")))
    os.makedirs(os.path.join(D, "..", "site"), exist_ok=True)
    open(os.path.join(D, "..", "site", "montagem.html"), "w").write(html)
    print("site/montagem.html", len(html), "bytes")
