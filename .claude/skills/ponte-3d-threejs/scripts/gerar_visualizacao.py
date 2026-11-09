#!/usr/bin/env python3
"""Gera uma página HTML com visualização 3D (Three.js) da treliça, colorida por esforço.

Uso: python3 gerar_visualizacao.py entrada.json saida.html [--largura 80]
Roda a análise (skill analise-trelica) e colore: azul = tração, vermelho = compressão, cinza = nula.
Para dim=2 replica a treliça em z=0 e z=largura e liga os nós com transversinas (cinza).
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "analise-trelica", "scripts"))
from trelica import resolver
p = argparse.ArgumentParser(); p.add_argument("ent"); p.add_argument("sai")
p.add_argument("--largura", type=float, default=80.0); a = p.parse_args()
m = json.load(open(a.ent)); r = resolver(m)
N = {b["id"]: b["N"] for b in r["barras"]}; Nmax = max(abs(v) for v in N.values()) or 1
def p3(c, z): return [c[0], c[1], c[2] if len(c) > 2 else z]
barras = []
planos = [0.0, a.largura] if m.get("dim", 2) == 2 else [0.0]
for z in planos:
    for b in m["barras"]:
        barras.append({"id": b["id"], "a": p3(m["nos"][b["i"]], z), "b": p3(m["nos"][b["j"]], z), "N": N[b["id"]]})
if m.get("dim", 2) == 2:
    for k, c in m["nos"].items():
        barras.append({"id": "t" + k, "a": p3(c, 0), "b": p3(c, a.largura), "N": None})
HTML = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Ponte 3D</title>
<style>:root{--bg:#f6f7f9;--fg:#1d2329;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#14171b;--fg:#e8eaed;--card:#1f2328}}
html,body{margin:0;height:100%;background:var(--bg);color:var(--fg);font:14px system-ui,sans-serif}
#info{position:absolute;left:16px;top:16px;background:var(--card);padding:10px 12px;border-radius:8px;max-width:calc(100% - 56px);box-shadow:0 1px 4px #0003}
.sw{display:inline-block;width:12px;height:12px;border-radius:2px;vertical-align:middle;margin-right:4px}</style>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>
</head><body><div id="info"><b>Ponte de palito — esforços</b><br>
<span class="sw" style="background:#2563eb"></span>tração <span class="sw" style="background:#dc2626"></span>compressão <span class="sw" style="background:#9ca3af"></span>nula/transversina
<div id="sel">Toque em uma barra para ver o esforço.</div></div>
<script type="module">
import * as THREE from "three"; import {OrbitControls} from "three/addons/controls/OrbitControls.js";
const B=__BARRAS__, NMAX=__NMAX__;
const scene=new THREE.Scene(); const r=new THREE.WebGLRenderer({antialias:true,alpha:true});
r.setPixelRatio(Math.min(devicePixelRatio,2)); r.setSize(innerWidth,innerHeight); document.body.appendChild(r.domElement);
const cam=new THREE.PerspectiveCamera(45,innerWidth/innerHeight,1,10000);
scene.add(new THREE.HemisphereLight(0xffffff,0x444444,2.2)); const dl=new THREE.DirectionalLight(0xffffff,1.5); dl.position.set(300,600,400); scene.add(dl);
const box=new THREE.Box3(), meshes=[];
for(const b of B){const A=new THREE.Vector3(...b.a),C=new THREE.Vector3(...b.b),d=C.clone().sub(A),L=d.length();
 let col=0x9ca3af; if(b.N!==null&&Math.abs(b.N)>1e-6){const t=0.35+0.65*Math.abs(b.N)/NMAX; col=b.N>0?new THREE.Color(0x2563eb).multiplyScalar(t):new THREE.Color(0xdc2626).multiplyScalar(t);}
 const m=new THREE.Mesh(new THREE.BoxGeometry(4,4,L),new THREE.MeshStandardMaterial({color:col}));
 m.position.copy(A).addScaledVector(d,0.5); m.lookAt(C); m.userData=b; scene.add(m); meshes.push(m); box.expandByPoint(A).expandByPoint(C);}
const c=box.getCenter(new THREE.Vector3()), s=box.getSize(new THREE.Vector3()).length();
cam.position.set(c.x+s*0.3,c.y+s*0.35,c.z+s*0.9); const ctl=new OrbitControls(cam,r.domElement); ctl.target.copy(c); ctl.update();
const ray=new THREE.Raycaster(), p=new THREE.Vector2();
r.domElement.addEventListener("pointerdown",e=>{p.set(e.clientX/innerWidth*2-1,-e.clientY/innerHeight*2+1); ray.setFromCamera(p,cam);
 const h=ray.intersectObjects(meshes)[0]; if(!h) return; const b=h.object.userData;
 document.getElementById("sel").textContent=b.N===null?`${b.id}: transversina (não calculada)`:`${b.id}: N = ${b.N.toFixed(1)} N (${b.N>0?"tração":b.N<0?"compressão":"nula"})`;});
addEventListener("resize",()=>{cam.aspect=innerWidth/innerHeight; cam.updateProjectionMatrix(); r.setSize(innerWidth,innerHeight);});
r.setAnimationLoop(()=>r.render(scene,cam));
</script></body></html>"""
open(a.sai, "w").write(HTML.replace("__BARRAS__", json.dumps(barras)).replace("__NMAX__", str(Nmax)))
print(f"{len(barras)} barras -> {a.sai}")
