// Imagens do manual (docs/img/manual/pNN.png -> convertidas em jpg) e posição de cada peça na imagem.
// Uso: node projeto/renderizar_manual.js <pasta three> <pasta temporária>
const { chromium } = require("playwright");
const path = require("path"), fs = require("fs");
const RAIZ = path.join(__dirname, ".."), THREE_DIR = process.argv[2], TMP = process.argv[3];
const plano = JSON.parse(fs.readFileSync(path.join(__dirname, "manual", "plano.json"), "utf8"));
(async () => {
  const b = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const ctx = await b.newContext({ viewport: { width: 960, height: 800 }, deviceScaleFactor: 1.25, colorScheme: "light" });
  const p = await ctx.newPage();
  p.on("pageerror", e => console.log("ERRO", e.message));
  await p.route("https://cdn.jsdelivr.net/npm/three@0.160.0/**", r =>
    r.fulfill({ path: path.join(THREE_DIR, "build", r.request().url().split("/build/")[1]), contentType: "application/javascript" }));
  await p.route("https://fonts.**", r => r.abort());
  await p.goto("file://" + path.join(RAIZ, "docs", "montagem.html") + "#passo-1");
  await p.addStyleTag({ content: `.sitenav,.hud,.rotulos,.dica,.voo,.cure,.btela{display:none!important}
    .wrap{max-width:none;padding:0} .bench{border:0;border-radius:0} #cena{width:960px!important;height:640px!important}` });
  await p.waitForTimeout(3000);
  await p.evaluate(() => { const b = document.getElementById("bnum"); if (b.getAttribute("aria-pressed") === "true") b.click(); });
  const posicoes = {};
  for (const s of plano) {
    if (s.t === null || s.t === undefined) continue;
    await p.evaluate(v => { const e = document.getElementById("t"); e.value = v; e.dispatchEvent(new Event("input")); }, s.t);
    await p.waitForTimeout(400);
    await p.evaluate(s => { window.__destaque(s.destaque || []); window.__enquadra(s.quadro, s.dir, s.pecas.length > 10 ? 1.05 : 1.2, s.extra); }, s);
    await p.waitForTimeout(2600);
    await p.locator("#cena").screenshot({ path: path.join(TMP, `p${String(s.n).padStart(2, "0")}.png`) });
    posicoes[s.n] = (await p.evaluate(ids => window.__proj(ids), s.pecas)).filter(q => q.ok).map(q => [q.j, +q.x.toFixed(4), +q.y.toFixed(4)]);
    console.log("passo", s.n, "ok");
  }
  fs.writeFileSync(path.join(__dirname, "manual", "posicoes.json"), JSON.stringify(posicoes));
  await b.close();
})();
