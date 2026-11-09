// Gera as imagens do site (docs/img/*.jpg) a partir da página de montagem 3D (docs/montagem.html).
// Uso: node projeto/renderizar_imagens.js <pasta com node_modules/three> [pasta temporária]
// Precisa do Playwright com Chromium. O Three.js do CDN é servido a partir da cópia local.
const { chromium } = require("playwright");
const path = require("path"), fs = require("fs");
const RAIZ = path.join(__dirname, "..");
const THREE_DIR = process.argv[2];
const TMP = process.argv[3] || path.join(RAIZ, "docs", "img");
const dados = JSON.parse(fs.readFileSync(path.join(__dirname, "montagem.json"), "utf8"));
const P = dados.passos, N = P.length, Y0 = dados.const.Y0;
const ev = Object.fromEntries(P.map((p, i) => [p.ev, i]).filter(([k]) => k));
const iCorte = P.findIndex(p => p.k === "pc" && p.cap === "Treliça A · camada 2" && p.tipo === "diagonal");
const iB = P.findIndex(p => p.cap.startsWith("Treliça B"));
const fotos = [
  { nome: "ponte_teste", t: N, cam: [-250, 430, 560, 250, 228, 40] },
  { nome: "passo_corte", t: iCorte + 0.12, foco: [-55, 95, 120] },
  { nome: "passo_trelica", t: iB, cam: [110, 250, 470, 250, 0, 255] },
  { nome: "passo_levantar", t: ev.colocaE + 1, cam: [-170, 470, 430, 250, 262, 40] },
  { nome: "por_dentro", t: N - 1, cam: [-30, Y0 + 24, 40, 120, Y0 + 24, 40] },
  { nome: "capa", t: N, cam: [-90, 400, 400, 250, 215, 40], w: 800, h: 420 },
];
(async () => {
  const b = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"] });
  const ctx = await b.newContext({ viewport: { width: 800, height: 760 }, deviceScaleFactor: 2, colorScheme: "light" });
  const p = await ctx.newPage();
  p.on("pageerror", e => console.log("ERRO", e.message));
  await p.route("https://cdn.jsdelivr.net/npm/three@0.160.0/**", r =>
    r.fulfill({ path: path.join(THREE_DIR, "build", r.request().url().split("/build/")[1]), contentType: "application/javascript" }));
  await p.route("https://fonts.**", r => r.abort());
  await p.goto("file://" + path.join(RAIZ, "docs", "montagem.html"));
  await p.addStyleTag({ content: `.sitenav,.hud,.rotulos,.dica,.voo,.cure{display:none!important}
    .wrap{max-width:none;padding:0} .bench{border:0;border-radius:0} #cena{width:800px!important;height:500px!important}` });
  await p.waitForTimeout(3000);
  await p.evaluate(() => { const b = document.getElementById("bnum"); if (b.getAttribute("aria-pressed") === "true") b.click(); });
  for (const f of fotos) {
    await p.evaluate(v => { const s = document.getElementById("t"); s.value = v; s.dispatchEvent(new Event("input")); }, f.t);
    await p.waitForTimeout(800);
    let cam = f.cam;
    if (f.foco) { const c = await p.evaluate(() => window.__foco()); cam = [c[0] + f.foco[0], c[1] + f.foco[1], c[2] + f.foco[2], ...c]; }
    await p.evaluate(([w, h]) => { const c = document.getElementById("cena"); c.style.setProperty("width", w + "px", "important"); c.style.setProperty("height", h + "px", "important"); }, [f.w || 800, f.h || 500]);
    await p.evaluate(c => window.__cam(c), cam);
    await p.waitForTimeout(3500);
    await p.locator("#cena").screenshot({ path: path.join(TMP, f.nome + ".png") });
    console.log("ok", f.nome, "t =", f.t);
  }
  await b.close();
})();
