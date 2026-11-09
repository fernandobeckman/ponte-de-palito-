#!/usr/bin/env python3
"""Monta o site público (GitHub Pages) na pasta docs/.

- docs/index.html: página inicial para família e amigos (imagens, como funciona, montagem).
- docs/montagem.html e docs/projeto.html: as páginas 3D (site/*.html) embrulhadas como documentos completos, com menu.
- docs/manual_de_corte.pdf e docs/gabarito_lateral_1-1.svg para baixar.
As imagens de docs/img/ são geradas por projeto/renderizar_imagens.js (Playwright).
"""
import json, math, os, re, shutil, sys

D = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(D, "..")
OUT = os.path.join(R, "docs")
URL = "https://ponte-de-palito.netlify.app/"   # endereço principal (Netlify)
os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
sys.path.insert(0, D)
from estudo_geometrias import gerar, avaliar, VAO  # noqa: E402

mont = json.load(open(os.path.join(D, "montagem.json")))
res = mont["resumo"]
modelo = json.load(open(os.path.join(D, "ponte_parker_8x90.json")))
calc = json.load(open(os.path.join(D, "resultados_ponte.json")))
N_PECAS = res["pecas"] + res["pecas_esp"]
MASSA = res["massa_g"]
VEZES = 45000 / MASSA
fmt = lambda v, d=0: f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")

ICONE = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M2 24h28M4 24L16 9l12 15M10 24l6-15M22 24l-6-15' "
         "stroke='%23b98a45' stroke-width='3' fill='none' stroke-linejoin='round'/%3E%3C/svg%3E")

def cabeca_comum(titulo, descricao, imagem="img/capa.jpg"):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{descricao}">
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:image" content="{URL}{imagem}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{ICONE}">"""

NAV_CSS = """
:root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; } img { max-width: 100%; } [hidden] { display: none !important; }
.sitenav { border-bottom: 1px solid var(--line, #d3dbd8); background: var(--card, #fff); }
.sitenav .in { max-width: 980px; margin: 0 auto; display: flex; gap: 4px 18px; align-items: center; flex-wrap: wrap;
  padding-block: 10px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.sitenav a { color: var(--ink, #18211f); text-decoration: none; font: 600 .92rem var(--body, system-ui, sans-serif); padding: 4px 0; border-bottom: 2px solid transparent; }
.sitenav a.marca { font: 700 1.1rem var(--display, sans-serif); margin-right: auto; }
.sitenav a[aria-current="page"] { border-bottom-color: var(--wood, #b98a45); }
.sitenav a:focus-visible { outline: 2px solid var(--tension, #2a66ad); outline-offset: 3px; }
"""

def nav(atual):
    itens = [("index.html", "Início"), ("manual.html", "Manual"), ("montagem.html", "Montagem 3D"), ("projeto.html", "Como foi calculada"), ("manual_de_corte.pdf", "Moldes (PDF)")]
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == atual else ""}>{t}</a>' for h, t in itens)
    return f'<nav class="sitenav" aria-label="Páginas do site"><div class="in"><a class="marca" href="index.html">Ponte de Palito</a>{links}</div></nav>'

def embrulha(fragmento, atual, titulo, descricao):
    """Fragmento de artifact (title/meta/link/style + conteúdo) -> documento completo com menu."""
    i = fragmento.index('<div class="wrap">')
    cabeca, corpo = fragmento[:i], fragmento[i:]
    cabeca = re.sub(r'<meta name="claude:[^>]*>\n?', "", cabeca)
    return (f'<!doctype html>\n<html lang="pt-BR">\n<head>\n{cabeca_comum(titulo, descricao)}\n{cabeca}<style>{NAV_CSS}</style>\n</head>\n'
            f'<body>\n{nav(atual)}\n{corpo}\n</body>\n</html>\n')

if __name__ != "__main__":
    pass
# ------------------------------------------------------------------ páginas 3D
pm = open(os.path.join(R, "site", "montagem.html")).read()
pm = pm.replace('O PDF com os moldes em tamanho real está no repositório, em <span class="mono">projeto/manual/manual_de_corte.pdf</span>.',
                'Os moldes em tamanho real estão no <a href="manual_de_corte.pdf" style="color:var(--tension)">manual de corte em PDF</a>.')
open(os.path.join(OUT, "montagem.html"), "w").write(embrulha(pm, "montagem.html", "Montagem da ponte de palito, peça por peça",
    "Animação 3D da montagem da ponte de palito de picolé: corte, cola, prensagem e o teste com 45 kg."))
pp = open(os.path.join(R, "site", "projeto.html")).read()
pp = re.sub(r'<a href="https://claude\.ai/artifact/[^"]+"', '<a href="montagem.html"', pp)
open(os.path.join(OUT, "projeto.html"), "w").write(embrulha(pp, "projeto.html", "Como a ponte de palito foi calculada",
    "Cálculo da ponte de palito: geometria escolhida, esforços em cada barra e fator de segurança."))
shutil.copy(os.path.join(D, "manual", "manual_de_corte.pdf"), os.path.join(OUT, "manual_de_corte.pdf"))
shutil.copy(os.path.join(D, "gabarito_lateral_1-1.svg"), os.path.join(OUT, "gabarito_lateral_1-1.svg"))
open(os.path.join(OUT, ".nojekyll"), "w").write("")

# ------------------------------------------------------------------ desenhos da página inicial
def svg_trelica(m, esforcos=None, alto=110, carga=False, classe=""):
    """Vista lateral da treliça. Com esforços: azul = tração, vermelho = compressão, cinza = sem esforço."""
    xs = [c[0] for c in m["nos"].values()]; ys = [c[1] for c in m["nos"].values()]
    pad = 16; H = max(ys); L = max(xs)
    vb_h = H + 2 * pad + (40 if carga else 0)
    Y = lambda y: H + pad - y
    out = [f'<svg class="{classe}" viewBox="{-pad} 0 {L + 2 * pad} {vb_h}" role="img" aria-label="Desenho lateral da treliça">']
    for b in m["barras"]:
        a, c = m["nos"][b["i"]], m["nos"][b["j"]]
        cls = "z"
        if esforcos:
            n = esforcos[b["id"]]
            cls = "t" if n > 1e-6 else "c" if n < -1e-6 else "z"
        out.append(f'<line class="{cls}" x1="{a[0]:.1f}" y1="{Y(a[1]):.1f}" x2="{c[0]:.1f}" y2="{Y(c[1]):.1f}"/>')
    for x in (0, L):   # apoios
        out.append(f'<path class="apoio" d="M{x} {Y(0) + 4} l-9 13 h18 z"/>')
    if carga:
        y0 = Y(0) + 6
        out.append(f'<line class="seta" x1="{L/2}" y1="{y0}" x2="{L/2}" y2="{y0 + 26}"/><path class="seta-p" d="M{L/2 - 7} {y0 + 20} l7 12 l7 -12 z"/>')
        out.append(f'<text class="rot" x="{L/2 + 12}" y="{y0 + 26}">45 kg</text>')
    out.append("</svg>")
    return "".join(out)

esf = {x["id"]: x["N"] for x in calc["linhas"]}
svg_funciona = svg_trelica(modelo, esf, carga=True, classe="trelica-grande")
formas = [("Pratt", "pratt", 4, 80, "36,5", "10 emendas"), ("Howe", "howe", 4, 70, "35,4", "10 emendas"),
          ("Warren", "warren", 4, 60, "33,1", "7 emendas"), ("Parker", "parker", 8, 90, "33,9", "nenhuma emenda")]
cartoes_formas = "".join(
    f'<figure class="forma{" vence" if k == "parker" else ""}">{svg_trelica(gerar(k, p, float(h)), classe="mini")}'
    f'<figcaption><b>{nome}</b><span>{pal} palitos por lado · {em}</span>{"<em>escolhida</em>" if k == "parker" else ""}</figcaption></figure>'
    for nome, k, p, h, pal, em in formas)

# ------------------------------------------------------------------ página inicial
DESCR = f"Uma ponte feita só de palito de picolé e cola branca, calculada para aguentar 45 kg com {fmt(MASSA)} g de peso."
INDEX = f"""<!doctype html>
<html lang="pt-BR">
<head>
{cabeca_comum("Ponte de palito que aguenta 45 kg", DESCR)}
<title>Ponte de Palito</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Layout: uma coluna de leitura; a foto da ponte abre a página, depois números grandes, como funciona, formato, montagem e teste. */
:root {{
  --bg: #f3f4ef; --card: #ffffff; --ink: #1b211e; --muted: #59645f; --line: #d9ddd6;
  --wood: #b98a45; --wood-soft: #f2e6d2; --tension: #2a66ad; --compression: #bf3b28; --zero: #a4ada8;
  --display: "Barlow Condensed", "Arial Narrow", "Roboto Condensed", sans-serif;
  --body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root {{
  --bg: #121614; --card: #1a201d; --ink: #e6ebe8; --muted: #9aa69f; --line: #2c3530;
  --wood: #d9b57a; --wood-soft: #2f281c; --tension: #6ea7ea; --compression: #f07a62; --zero: #5f6a65; color-scheme: dark }} }}
{NAV_CSS}
body {{ background: var(--bg); color: var(--ink); font: 17px/1.6 var(--body); }}
.wrap {{ max-width: 980px; margin: 0 auto; padding-block: 28px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 56px; }}
h1, h2, h3 {{ font-family: var(--display); line-height: 1.02; margin: 0; text-wrap: balance; }}
h1 {{ font-size: clamp(2.6rem, 9vw, 4.6rem); font-weight: 700; }}
h2 {{ font-size: clamp(1.9rem, 6vw, 2.6rem); font-weight: 700; }}
h3 {{ font-size: 1.35rem; font-weight: 600; }}
p {{ margin: 0; max-width: 64ch; }}
.eyebrow {{ font: 600 .78rem var(--mono); text-transform: uppercase; letter-spacing: .12em; color: var(--wood); }}
section {{ display: grid; gap: 16px; min-width: 0; }}
.hero {{ display: grid; gap: 18px; }}
.hero .lede {{ font-size: 1.15rem; color: var(--muted); }}
.foto {{ margin: 0; border-radius: 14px; overflow: hidden; border: 1px solid var(--line); background: var(--card); }}
.foto img {{ display: block; width: 100%; height: auto; }}
.foto figcaption {{ font-size: .88rem; color: var(--muted); padding: 8px 12px; }}
.acoes {{ display: flex; gap: 10px; flex-wrap: wrap; }}
.btn {{ display: inline-block; font: 600 1rem var(--body); text-decoration: none; padding: 11px 18px; border-radius: 999px; border: 1px solid var(--ink); color: var(--ink); }}
.btn.prim {{ background: var(--ink); color: var(--bg); }}
.btn:focus-visible {{ outline: 2px solid var(--tension); outline-offset: 3px; }}
.numeros {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1px; background: var(--line); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; }}
.numeros div {{ background: var(--card); padding: 16px; display: grid; gap: 2px; align-content: start; }}
.numeros b {{ font: 700 clamp(1.8rem, 6vw, 2.4rem) var(--display); line-height: 1; }}
.numeros span {{ color: var(--muted); font-size: .92rem; }}
.desenho {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px; overflow-x: auto; }}
.trelica-grande {{ width: 100%; min-width: 320px; height: auto; display: block; }}
svg line {{ stroke-width: 4.2; stroke-linecap: round; }}
svg line.t {{ stroke: var(--tension); }} svg line.c {{ stroke: var(--compression); }} svg line.z {{ stroke: var(--zero); }}
svg.mini line.z {{ stroke: var(--wood); stroke-width: 7; }}
svg .apoio {{ fill: var(--muted); }}
svg .seta {{ stroke: var(--ink); stroke-width: 2.5; }} svg .seta-p {{ fill: var(--ink); }}
svg .rot {{ fill: var(--ink); font: 700 15px var(--mono); }}
.legenda {{ display: flex; gap: 6px 18px; flex-wrap: wrap; font-size: .95rem; }}
.legenda i {{ display: inline-block; width: 22px; height: 6px; border-radius: 3px; vertical-align: middle; margin-right: 6px; }}
.formas {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }}
.forma {{ margin: 0; background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px; display: grid; gap: 8px; }}
.forma svg {{ width: 100%; height: auto; }}
.forma figcaption {{ display: grid; gap: 2px; font-size: .9rem; color: var(--muted); }}
.forma figcaption b {{ font: 700 1.2rem var(--display); color: var(--ink); }}
.forma em {{ font-style: normal; font: 600 .72rem var(--mono); text-transform: uppercase; letter-spacing: .08em; color: var(--wood); }}
.forma.vence {{ border: 2px solid var(--wood); background: var(--wood-soft); }}
.passos {{ display: grid; gap: 22px; counter-reset: p; }}
.passo {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.25fr); gap: 18px; align-items: center; }}
.passo .txt {{ display: grid; gap: 8px; }}
.passo .num {{ font: 700 1rem var(--mono); color: var(--wood); }}
@media (max-width: 680px) {{ .passo {{ grid-template-columns: 1fr; }} .passo .foto {{ order: -1; }} }}
.aviso {{ background: var(--wood-soft); border: 1px dashed var(--wood); border-radius: 12px; padding: 16px; display: grid; gap: 6px; }}
footer {{ border-top: 1px solid var(--line); padding-top: 18px; display: grid; gap: 8px; color: var(--muted); font-size: .92rem; }}
footer a {{ color: var(--tension); }}
</style>
</head>
<body>
{nav("index.html")}
<main class="wrap">
  <section class="hero">
    <span class="eyebrow">Projeto de engenharia · palito de picolé e cola branca</span>
    <h1>Uma ponte de palito que aguenta 45 kg</h1>
    <p class="lede">Ela tem 50 cm entre os apoios, é feita só com palitos de picolé e cola branca e pesa cerca de {fmt(MASSA)} g. O cálculo mostra que ela segura 45 kg pendurados no meio: mais de {fmt(math.floor(VEZES / 10) * 10)} vezes o próprio peso.</p>
    <div class="acoes"><a class="btn prim" href="montagem.html">Ver a montagem em 3D</a><a class="btn" href="#como-funciona">Como ela funciona</a></div>
    <figure class="foto"><img src="img/ponte_teste.jpg" width="1600" height="842" alt="Ponte de palito pronta, apoiada em dois pilares, com pesos de 45 kg pendurados no meio"><figcaption>Modelo 3D da ponte pronta, com a carga de 45 kg pendurada no meio.</figcaption></figure>
  </section>

  <section aria-label="Números da ponte">
    <div class="numeros">
      <div><b>45 kg</b><span>carga que ela precisa aguentar</span></div>
      <div><b>{fmt(MASSA)} g</b><span>peso da ponte (estimado)</span></div>
      <div><b>{N_PECAS}</b><span>peças cortadas e numeradas</span></div>
      <div><b>{res['palitos_comprar']}</b><span>palitos comprados, com sobra para testes</span></div>
      <div><b>50 cm</b><span>de vão livre entre os apoios</span></div>
      <div><b>≈ R$ 74</b><span>de material (palitos, cola, estilete, lixa)</span></div>
    </div>
  </section>

  <section id="como-funciona">
    <h2>Como ela funciona</h2>
    <p>A ponte é uma <b>treliça</b>: um conjunto de triângulos. Triângulo não deforma, então o peso do meio se divide pelas barras até chegar aos apoios. Cada barra trabalha de um jeito só: ou é <b>esticada</b> ou é <b>apertada</b>.</p>
    <div class="desenho">{svg_funciona}</div>
    <div class="legenda"><span><i style="background:var(--compression)"></i>apertadas (compressão)</span><span><i style="background:var(--tension)"></i>esticadas (tração)</span><span><i style="background:var(--zero)"></i>travam a estrutura</span></div>
    <p>A parte de cima, em vermelho, é a mais difícil: barra apertada tende a entortar de lado, como uma régua empurrada pelas pontas. Por isso cada barra tem três palitos colados e as duas laterais da ponte são travadas entre si por cima e por baixo.</p>
  </section>

  <section>
    <h2>Por que esse formato</h2>
    <p>Antes de escolher, o computador testou 208 formatos de treliça e calculou quantos palitos cada um precisa para aguentar a carga com folga de segurança. Os melhores de cada família:</p>
    <div class="formas">{cartoes_formas}</div>
    <p>O formato escolhido (Parker) tem o topo em triângulo, que acompanha o jeito como o peso do meio "puxa" a ponte. Ele gasta quase o mesmo tanto de palito que o melhor, mas <b>nenhuma barra é maior que um palito</b>, então não precisa de emendas, que costumam ser o ponto fraco.</p>
  </section>

  <section>
    <h2>Como vai ser montada</h2>
    <div class="passos">
      <div class="passo"><div class="txt"><span class="num">1 · cortar</span><h3>Cada peça tem número e código</h3><p>São {N_PECAS} peças em 37 formatos diferentes, como num manual de LEGO. Cada uma é cortada no tamanho e no ângulo certos, usando moldes impressos em tamanho real.</p></div>
        <figure class="foto"><img src="img/passo_corte.jpg" width="1600" height="1000" alt="Palito sendo cortado no tamanho certo, com a linha de corte marcada em vermelho" loading="lazy"></figure></div>
      <div class="passo"><div class="txt"><span class="num">2 · colar</span><h3>As laterais são montadas deitadas</h3><p>Cada lateral é montada sobre um desenho em tamanho real, em três camadas de palitos, com cola branca entre elas. Depois fica 24 h prensada para a cola secar.</p></div>
        <figure class="foto"><img src="img/passo_trelica.jpg" width="1600" height="1000" alt="Uma lateral da ponte pronta, deitada sobre o desenho impresso" loading="lazy"></figure></div>
      <div class="passo"><div class="txt"><span class="num">3 · levantar</span><h3>As duas laterais ficam de pé e são travadas</h3><p>Espaçadores de palito seguram as duas laterais paralelas enquanto são coladas as peças de baixo, de cima e as diagonais que travam tudo.</p></div>
        <figure class="foto"><img src="img/passo_levantar.jpg" width="1600" height="1000" alt="As duas laterais de pé, com os espaçadores provisórios entre elas" loading="lazy"></figure></div>
      <div class="passo"><div class="txt"><span class="num">4 · por dentro</span><h3>Dá para passear por dentro dela</h3><p>No modelo 3D você gira, aproxima e até "voa" por dentro da ponte para ver cada palito, com o número de cada peça.</p><p><a class="btn" href="montagem.html">Abrir a montagem em 3D</a></p></div>
        <figure class="foto"><img src="img/por_dentro.jpg" width="1600" height="1000" alt="Vista de dentro da ponte, olhando ao longo do vão entre as duas laterais" loading="lazy"></figure></div>
    </div>
  </section>

  <section>
    <h2>O teste</h2>
    <div class="aviso"><b>Em breve.</b><p>A ponte ainda vai ser construída e testada. Quando o teste acontecer, as fotos, o vídeo e quanto peso ela realmente aguentou vão aparecer aqui.</p></div>
  </section>

  <footer>
    <span>Quer ver os detalhes? <a href="projeto.html">Como foi calculada</a> · <a href="montagem.html">Montagem 3D peça por peça</a> · <a href="manual_de_corte.pdf">Manual de corte (PDF)</a> · <a href="https://github.com/fernandobeckman/ponte-de-palito-">Arquivos do projeto no GitHub</a></span>
    <span>Os números deste site vêm do cálculo do projeto. O resultado real só vale depois do teste.</span>
  </footer>
</main>
</body>
</html>
"""
open(os.path.join(OUT, "index.html"), "w").write(INDEX)
print("docs/ pronto:", sorted(os.listdir(OUT)))
