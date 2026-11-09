function criaNavegador(THREE) {
  /* Navegação livre: girar, mover (pan), zoom na direção do dedo/cursor, toque duplo para aproximar,
     modo "voar" (olhar em volta + andar), teclado WASD/QE e animação para vistas prontas. */
  const V = THREE.Vector3;
  return class Navegador {
    constructor(cam, el) {
      this.cam = cam; this.el = el; this.target = new V();
      this.modo = "orbitar"; this.autoRotate = false; this.autoRotateSpeed = 2;
      this.minDistance = 2; this.maxDistance = 8000; this.velVoo = 160;
      this.dT = 0; this.dP = 0; this.ptr = new Map(); this.par = null;
      this.ouv = { start: [], end: [], toque: [], duplo: [], interagiu: [] };
      this.joy = { f: 0, r: 0, u: 0 }; this.teclas = new Set(); this.rapido = false;
      this.ultToque = { t: 0, x: 0, y: 0 }; this.anim = null; this.antes = performance.now();
      this.pick = null;   // função (x, y) -> ponto 3D sob o cursor, definida pela página
      this.limites = null; // { min: [x, y, z], max: [x, y, z] }: a câmera não sai desta caixa (min[1] = chão)
      el.addEventListener("contextmenu", e => e.preventDefault());
      el.addEventListener("pointerdown", e => this._down(e));
      el.addEventListener("pointermove", e => this._move(e));
      for (const ev of ["pointerup", "pointercancel"]) el.addEventListener(ev, e => this._up(e));
      el.addEventListener("wheel", e => { e.preventDefault(); this._avisa("zoom"); this.zoomEm(e.clientX, e.clientY, Math.exp(e.deltaY * .0012)); }, { passive: false });
      addEventListener("keydown", e => {
        if (e.target && /INPUT|TEXTAREA|SELECT/.test(e.target.tagName) && e.target.type !== "range") return;
        const k = e.key.length === 1 ? e.key.toLowerCase() : "";
        if (k && "wasdqe".includes(k)) { this.teclas.add(k); this._avisa("andar"); e.preventDefault(); }
        if (e.key === "Shift") this.rapido = true;
      });
      addEventListener("keyup", e => { this.teclas.delete(e.key.length === 1 ? e.key.toLowerCase() : e.key); if (e.key === "Shift") this.rapido = false; });
      addEventListener("blur", () => { this.teclas.clear(); this.rapido = false; });
    }
    addEventListener(n, f) { if (this.ouv[n]) this.ouv[n].push(f); }
    _emite(n, ...a) { this.ouv[n].forEach(f => f(...a)); }
    _avisa(tipo) { this.anim = null; this._emite("interagiu", tipo); }
    _down(e) {
      try { this.el.setPointerCapture(e.pointerId); } catch (_) {}
      this.ptr.set(e.pointerId, { x: e.clientX, y: e.clientY, x0: e.clientX, y0: e.clientY, b: e.button, mod: e.shiftKey || e.ctrlKey || e.metaKey, andou: 0 });
      if (this.ptr.size === 1) this._emite("start");
      this.par = this.ptr.size === 2 ? this._medePar() : null;
    }
    _medePar() { const [a, b] = [...this.ptr.values()]; return { d: Math.hypot(a.x - b.x, a.y - b.y), x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }; }
    _move(e) {
      const q = this.ptr.get(e.pointerId); if (!q) return;
      const dx = e.clientX - q.x, dy = e.clientY - q.y; q.x = e.clientX; q.y = e.clientY; q.andou += Math.abs(dx) + Math.abs(dy);
      if (this.ptr.size === 1) {
        if (q.andou < 4) return;
        const mover = q.b === 1 || q.b === 2 || q.mod;
        if (mover) { this._avisa("mover"); this.pan(dx, dy); }
        else if (this.modo === "voar") { this._avisa("olhar"); this.olhar(dx, dy); }
        else { this._avisa("girar"); const k = 2 * Math.PI / Math.max(240, this.el.clientHeight); this.dT -= dx * k; this.dP -= dy * k; }
      } else if (this.ptr.size === 2 && this.par) {
        const p = this._medePar();
        this._avisa("mover");
        this.pan(p.x - this.par.x, p.y - this.par.y);
        if (this.par.d > 0 && p.d > 0) {
          if (this.modo === "voar") this.andar((p.d - this.par.d) * 1.2, 0, 0);
          else this.zoomEm(p.x, p.y, this.par.d / p.d);
        }
        this.par = p;
      }
    }
    _up(e) {
      const q = this.ptr.get(e.pointerId); if (!q) return;
      this.ptr.delete(e.pointerId);
      if (q.andou < 8 && this.ptr.size === 0) {
        const agora = performance.now(), u = this.ultToque;
        if (agora - u.t < 330 && Math.hypot(e.clientX - u.x, e.clientY - u.y) < 35) { this._emite("duplo", e.clientX, e.clientY); this.focarEm(e.clientX, e.clientY); u.t = 0; }
        else { this._emite("toque", e.clientX, e.clientY); this.ultToque = { t: agora, x: e.clientX, y: e.clientY }; }
      }
      this.par = this.ptr.size === 2 ? this._medePar() : null;
      if (this.ptr.size === 0) this._emite("end");
    }
    _base() {
      const f = this.target.clone().sub(this.cam.position); const d = f.length() || 1; f.divideScalar(d);
      const r = new V().crossVectors(f, new V(0, 1, 0)); if (r.lengthSq() < 1e-8) r.set(1, 0, 0); r.normalize();
      const u = new V().crossVectors(r, f).normalize();
      return { f, r, u, d };
    }
    pan(dx, dy) {
      const { r, u, d } = this._base();
      const dist = this.modo === "voar" ? 150 : d;
      const k = 2 * dist * Math.tan(THREE.MathUtils.degToRad(this.cam.fov) / 2) / Math.max(1, this.el.clientHeight);
      const delta = r.multiplyScalar(-dx * k).add(u.multiplyScalar(dy * k));
      this.cam.position.add(delta); this.target.add(delta);
    }
    olhar(dx, dy) {
      const k = 2 * Math.PI / Math.max(240, this.el.clientHeight) * .6;
      const s = new THREE.Spherical().setFromVector3(this.target.clone().sub(this.cam.position));
      s.theta += dx * k; s.phi = Math.min(Math.PI - .01, Math.max(.01, s.phi - dy * k)); s.radius = 150;
      this.target.copy(this.cam.position).add(new V().setFromSpherical(s));
    }
    andar(f, r, u) {
      const b = this._base();
      const delta = b.f.multiplyScalar(f).add(b.r.multiplyScalar(r)).add(new V(0, u, 0));
      this.cam.position.add(delta); this.target.add(delta);
    }
    _raio(x, y) {
      const rc = this.el.getBoundingClientRect();
      const ndc = new THREE.Vector2((x - rc.left) / rc.width * 2 - 1, -(y - rc.top) / rc.height * 2 + 1);
      const ray = new THREE.Raycaster(); ray.setFromCamera(ndc, this.cam); return ray.ray;
    }
    zoomEm(x, y, s) {
      if (this.modo === "voar") { this.andar((1 - s) * 220, 0, 0); return; }
      if (s > 1) {   // afastar: recua a câmera mantendo o ponto de foco
        const off = this.cam.position.clone().sub(this.target);
        const d = Math.min(this.maxDistance, off.length() * s);
        this.cam.position.copy(this.target).add(off.setLength(d)); return;
      }
      const ray = this._raio(x, y), d = this.cam.position.distanceTo(this.target);
      let P = this.pick ? this.pick(x, y) : null;
      if (!P) P = ray.origin.clone().addScaledVector(ray.direction, d);
      const nc = P.clone().add(this.cam.position.clone().sub(P).multiplyScalar(s));
      if (nc.distanceTo(P) < this.minDistance && s < 1) return;
      if (nc.distanceTo(P) > this.maxDistance && s > 1) return;
      this.target.copy(P.clone().add(this.target.clone().sub(P).multiplyScalar(s)));
      this.cam.position.copy(nc);
    }
    focarEm(x, y) {
      const P = this.pick ? this.pick(x, y) : null; if (!P) return;
      this._avisa("focar");
      const off = this.cam.position.clone().sub(this.target), d = off.length();
      const nd = Math.min(d, 140);
      this.irPara(P.clone().add(off.normalize().multiplyScalar(nd)), P);
    }
    irPara(pos, alvo, dur = .7) {
      this.anim = { t: 0, dur, p0: this.cam.position.clone(), a0: this.target.clone(), p1: pos.clone(), a1: alvo.clone() };
      this.dT = this.dP = 0;
    }
    _limita() {
      const L = this.limites; if (!L) return;
      const c = this.cam.position, t = this.target;
      for (let i = 0; i < 3; i++) {
        const k = "xyz"[i];
        c[k] = Math.min(L.max[i], Math.max(L.min[i], c[k]));
        const A = L.alvo || L;
        t[k] = Math.min(A.max[i], Math.max(A === L && i === 1 ? 0 : A.min[i], t[k]));
      }
    }
    update() {
      const agora = performance.now(), dt = Math.min(.05, (agora - this.antes) / 1000); this.antes = agora;
      if (this.anim) {
        const a = this.anim; a.t += dt / a.dur; const k = Math.min(1, a.t), e = k * k * (3 - 2 * k);
        this.cam.position.lerpVectors(a.p0, a.p1, e); this.target.lerpVectors(a.a0, a.a1, e);
        if (k >= 1) this.anim = null;
        this._limita(); this.cam.lookAt(this.target); return;
      }
      const T = this.teclas;
      const f = (T.has("w") ? 1 : 0) - (T.has("s") ? 1 : 0) + this.joy.f;
      const r = (T.has("d") ? 1 : 0) - (T.has("a") ? 1 : 0) + this.joy.r;
      const u = (T.has("e") ? 1 : 0) - (T.has("q") ? 1 : 0) + this.joy.u;
      if (f || r || u) {
        const base = this.modo === "voar" ? this.velVoo : Math.max(60, this.cam.position.distanceTo(this.target) * .8);
        const v = base * (this.rapido ? 3 : 1) * dt;
        this.andar(f * v, r * v, u * v);
      }
      if (this.modo === "orbitar") {
        const off = this.cam.position.clone().sub(this.target), s = new THREE.Spherical().setFromVector3(off);
        if (this.autoRotate && this.ptr.size === 0) s.theta -= 2 * Math.PI / 3600 * this.autoRotateSpeed;
        const k = .22;
        s.theta += this.dT * k; s.phi += this.dP * k; this.dT *= 1 - k; this.dP *= 1 - k;
        s.phi = Math.min(Math.PI - .001, Math.max(.001, s.phi));
        s.radius = Math.min(this.maxDistance, Math.max(this.minDistance, s.radius));
        off.setFromSpherical(s); this.cam.position.copy(this.target).add(off);
      } else if (this.autoRotate && this.ptr.size === 0) {
        const s = new THREE.Spherical().setFromVector3(this.target.clone().sub(this.cam.position));
        s.theta -= 2 * Math.PI / 3600 * this.autoRotateSpeed; this.target.copy(this.cam.position).add(new V().setFromSpherical(s));
      }
      this._limita();
      this.cam.lookAt(this.target);
    }
  };
}
