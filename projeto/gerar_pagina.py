#!/usr/bin/env python3
"""Gera site/projeto.html ("Como foi calculada"): 3D das barras com cores por esforço, números e tabelas.
Lê ponte_ucb.json e resultados_ucb_ponte.json (calculo_ucb.py), montagem.json e resultados_ucb.json (estudo_ucb.py)."""
import json, math, os
d = os.path.dirname(os.path.abspath(__file__))
G = 9.80665
m = json.load(open(os.path.join(d, "ponte_ucb.json")))
r = json.load(open(os.path.join(d, "resultados_ucb_ponte.json")))
mo = json.load(open(os.path.join(d, "montagem.json")))
est = json.load(open(os.path.join(d, "resultados_ucb.json")))
res = mo["resumo"]
ZT = 105.0                         # plano médio de cada treliça (faces externas em ±110)
P30 = 30 * G / 1000.0              # fator: esforço para 1000 N -> esforço com 30 kg no meio
f5 = lambda v: f"{v + 0.0:.5f}".replace(".", ",")
N = {x["id"]: x for x in r["linhas"]}

bars = []
for z in (-ZT, ZT):
    for b in m["barras"]:
        a, c = m["nos"][b["i"]], m["nos"][b["j"]]; x = N[b["id"]]
        bars.append({"id": b["id"], "a": [a[0], a[1], z], "b": [c[0], c[1], z], "N": round(x["N"] * P30, 5),
                     "Nd": round(x["N_desloc"] * P30, 5), "n": x["n"], "L": round(x["L_mm"], 5),
                     "P": round(x["P_kgf"], 5) if x["P_kgf"] < 1e9 else 0, "modo": x["modo"]})
for k, c in m["nos"].items():
    if k.startswith("b") and k != "b4":
        bars.append({"id": "transversina " + k, "a": [c[0], -7, -110], "b": [c[0], -7, 110], "N": None,
                     "txt": "trava as duas treliças por baixo (220 mm)."})
    elif k.startswith("t"):
        bars.append({"id": "escora " + k, "a": [c[0], c[1] + 7, -110], "b": [c[0], c[1] + 7, 110], "N": None,
                     "txt": "trava o banzo de cima contra a flambagem de lado."})
for i in range(8):
    za, zb = (-ZT, ZT) if i % 2 == 0 else (ZT, -ZT)
    bars.append({"id": f"contravento inferior {i+1}", "a": [i * 100 + 12, -7, za], "b": [(i + 1) * 100 - 12, -7, zb], "N": None,
                 "txt": "zigue-zague que trava a ponte contra torção."})
    if 1 <= i <= 6:
        bars.append({"id": f"contravento superior {i}", "a": [i * 100 + 12, 107, za], "b": [(i + 1) * 100 - 12, 107, zb], "N": None,
                     "txt": "zigue-zague que trava o plano de cima."})
PZ, YB, DM = [-95.8, -50.0, 0.0, 50.0, 95.8], 8.4, 70.0
mini = [((PZ[0], YB), (PZ[4], YB)), ((PZ[0], YB + DM), (PZ[4], YB + DM))] + [((z, YB), (z, YB + DM)) for z in PZ] + \
       [((PZ[0], YB + DM), (PZ[1], YB)), ((PZ[1], YB + DM), (PZ[2], YB)), ((PZ[4], YB + DM), (PZ[3], YB)), ((PZ[3], YB + DM), (PZ[2], YB))]
for (z0, y0), (z1, y1) in mini:
    bars.append({"id": "mini-treliça do ponto de carga", "a": [400, y0, z0], "b": [400, y1, z1], "N": None,
                 "txt": "recebe a haste de aço no meio e passa a carga para os consolos das duas treliças."})

# vista lateral (SVG) de uma treliça: x + 20, y invertido
Y = lambda y: 120 - y
svg = []
for b in m["barras"]:
    a, c = m["nos"][b["i"]], m["nos"][b["j"]]; x = N[b["id"]]["N"]
    cls = "t" if x > 1e-6 else "c" if x < -1e-6 else "z"
    svg.append(f'<line class="{cls}" x1="{a[0]+20}" y1="{Y(a[1])}" x2="{c[0]+20}" y2="{Y(c[1])}"/>')
for k, c in m["nos"].items():
    svg.append(f'<circle cx="{c[0]+20}" cy="{Y(c[1])}" r="2.6"/>')
svg = "".join(svg)

# tabela: a barra mais crítica de cada grupo + ligações + ponto de carga
grupos = [("Banzo de baixo", lambda i: i.startswith("b") and "-b" in i), ("Banzo de cima", lambda i: i.startswith("t") and "-t" in i),
          ("Barras inclinadas das pontas", lambda i: i in ("b0-t1", "t7-b8")),
          ("Montantes", lambda i: i.startswith("b") and "-t" in i and i not in ("b0-t1",)),
          ("Diagonais do meio", lambda i: i in ("t3-b4", "t5-b4")),
          ("Demais diagonais", lambda i: i.startswith("t") and "-b" in i and i not in ("t3-b4", "t5-b4", "t7-b8"))]
linhas = []
for nome, filt in grupos:
    xs = [x for x in r["linhas"] if filt(x["id"])]
    x = min(xs, key=lambda x: x["P_kgf"])
    cl = "tr" if x["N"] > 1e-6 else "co" if x["N"] < -1e-6 else ""
    linhas.append((nome + f" ({x['id']})", f5(x["L_mm"]), cl, f5(x["N"]), f5(x["N_desloc"]), f5(x["R"]), f5(x["P_kgf"]), x["modo"], x["P_kgf"]))
linhas.append(("Ligações coladas (chapas, 40 mm)", "—", "", "—", "—", f5(2.0 * 2 * 8.4 * 40), f5(r["P_lig"]), "cola", r["P_lig"]))
linhas.append(("Mini-treliça do ponto de carga", "—", "", "—", "—", "—", f5(r["P_tr"]), "ligações", r["P_tr"]))
linhas.append(("Consolos (cola 30 × 8,4 mm por lado)", "—", "", "—", "—", f5(2 * 2.0 * 30 * 8.4), f5(r["P_tr_tau"]), "cola", r["P_tr_tau"]))
pmin = min(l[-1] for l in linhas)
rows = "".join(
    f'<tr><td>{n}</td><td class="num">{L}</td><td class="num {cl}">{Nc}</td><td class="num">{Nd}</td><td class="num">{R}</td>'
    f'<td class="num">{"<b>" + P + "</b>" if abs(v - pmin) < 1e-9 else P}</td><td>{modo}</td></tr>'
    for n, L, cl, Nc, Nd, R, P, modo, v in linhas)

melhor = {}
for x in est:
    if x["tipo"] not in melhor or x["ef"] > melhor[x["tipo"]]["ef"]: melhor[x["tipo"]] = x
formas = "".join(f'<tr><td>{t.capitalize()}</td><td>{x["paineis"]}</td><td>{x["h"]}</td><td>{f5(x["ef"])}</td><td>{f5(x["Lmax"])}</td><td>{x["nmax"]}</td></tr>'
                 for t, x in sorted(melhor.items(), key=lambda t: -t[1]["ef"]))
razao = r["P_final"] / (res["massa_g"] / 1000)
formas += (f'<tr class="win"><td>Pratt (escolhida)</td><td>8</td><td>100</td><td>{f5(razao)}</td>'
           f'<td>{f5(max(x["L_mm"] for x in r["linhas"]))}</td><td>3</td></tr>')

html = open(os.path.join(d, "pagina_modelo.html")).read().replace("__NAVEGADOR__", open(os.path.join(d, "navegador.js")).read())
for k, v in {"__BARS__": json.dumps(bars, ensure_ascii=False), "__SVG__": svg, "__ROWS__": rows, "__FORMAS__": formas,
             "__NCOMB__": str(len(est)), "__PCOL__": f5(r["P_final"]), "__FS__": f5(r["P_final"] / 30),
             "__MASSA__": f5(res["massa_g"]), "__RAZAO__": f5(razao), "__PALITOS__": str(res["palitos_ponte"]),
             "__COMPRAR__": str(res["palitos_comprar"])}.items():
    html = html.replace(k, v)
os.makedirs(os.path.join(d, "..", "site"), exist_ok=True)
open(os.path.join(d, "..", "site", "projeto.html"), "w").write(html)
print("site/projeto.html", len(html), "bytes")
