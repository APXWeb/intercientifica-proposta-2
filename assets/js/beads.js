/* Microesferas em WebGL (Three.js), só na home.
   É uma representação ilustrativa: as figuras SVG estáticas já estão na página
   e continuam valendo sem WebGL, com movimento reduzido ou economia de dados. */

const THREE_URL = 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.min.js';
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const saveData = !!(navigator.connection && navigator.connection.saveData);
const lowEnd = (navigator.deviceMemory && navigator.deviceMemory < 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4);
const SPECTRAL = [0xff5a47, 0xffb547, 0x5fd3c2, 0x9daaff];
const CHAMBER = 0x0a0c0f;

function webglOk() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (_) { return false; }
}

// gerador determinístico, para a cena ser sempre a mesma
function rng(seed) { return () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646; }
const gauss = (r) => { let u = 0, v = 0; while (!u) u = r(); while (!v) v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
const smooth = (t) => t * t * (3 - 2 * t);
const clamp01 = (t) => Math.max(0, Math.min(1, t));

/* ---------------------------------------------------------- pausa global (WCAG 2.2.2) */
const pauseState = { paused: false, subs: new Set() };
function wirePause() {
  document.querySelectorAll('[data-pause]').forEach((btn) => {
    btn.hidden = false;
    btn.addEventListener('click', () => {
      pauseState.paused = !pauseState.paused;
      document.querySelectorAll('[data-pause]').forEach((b) => {
        b.setAttribute('aria-pressed', String(pauseState.paused));
        b.querySelector('span').textContent = pauseState.paused ? 'Retomar animação' : 'Pausar animação';
      });
      pauseState.subs.forEach((fn) => fn(pauseState.paused));
    });
  });
}

function makeRenderer(THREE, canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !lowEnd, powerPreference: 'low-power', alpha: false });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, lowEnd ? 1 : 1.75));
  renderer.setClearColor(CHAMBER, 1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  return renderer;
}

function lights(THREE, scene) {
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const key = new THREE.DirectionalLight(0xffffff, 2.2);
  key.position.set(-4, 6, 8);
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xbfd4ff, 1.6);
  rim.position.set(5, -2, -6);
  scene.add(rim);
}

function material(THREE) {
  return new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.32, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.25, sheen: 0.4, sheenColor: new THREE.Color(0xffffff) });
}

/* Liga e desliga o laço de render conforme visibilidade e pausa. */
function runLoop(el, step) {
  let visible = false, raf = 0, last = performance.now();
  const tick = (now) => {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    step(dt, pauseState.paused);
    raf = visible && !document.hidden ? requestAnimationFrame(tick) : 0;
  };
  const start = () => { if (!raf && visible && !document.hidden) { last = performance.now(); raf = requestAnimationFrame(tick); } };
  new IntersectionObserver((e) => { visible = e[0].isIntersecting; start(); }, { rootMargin: '100px' }).observe(el);
  document.addEventListener('visibilitychange', start);
  return { kick: start };
}

function fit(renderer, camera, el) {
  const w = el.clientWidth, h = el.clientHeight;
  if (!w || !h) return;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}

/* ---------------------------------------------------------- herói: nuvem em suspensão */
function hero(THREE) {
  const canvas = document.getElementById('hero-gl');
  if (!canvas) return;
  const box = canvas.parentElement;
  const N = lowEnd ? 260 : 560;
  const r = rng(11);
  const renderer = makeRenderer(THREE, canvas);
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(CHAMBER, 7, 17);
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 60);
  camera.position.set(0, 0, 11);
  lights(THREE, scene);
  const geo = new THREE.SphereGeometry(1, lowEnd ? 14 : 24, lowEnd ? 10 : 16);
  const mesh = new THREE.InstancedMesh(geo, material(THREE), N);
  const base = [], m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3(), c = new THREE.Color();
  for (let i = 0; i < N; i++) {
    const a = r() * Math.PI * 2, u = r() * 2 - 1, rad = Math.cbrt(r()) * 4.6;
    const x = Math.cos(a) * Math.sqrt(1 - u * u) * rad * 0.9, y = u * rad * 1.15, z = Math.sin(a) * Math.sqrt(1 - u * u) * rad * 0.9;
    const size = 0.045 + Math.pow(r(), 2.6) * 0.13;
    base.push({ x, y, z, size, ph: r() * 100, sp: 0.25 + r() * 0.5 });
    c.setHex(i % 3 === 0 ? SPECTRAL[(i / 3) % 4 | 0] : 0xb9c0c8);
    mesh.setColorAt(i, c);
  }
  scene.add(mesh);
  const group = new THREE.Group();
  group.add(mesh);
  scene.add(group);
  let t = 0, px = 0, py = 0, tx = 0, ty = 0;
  box.addEventListener('pointermove', (e) => {
    const b = box.getBoundingClientRect();
    tx = ((e.clientX - b.left) / b.width - 0.5) * 2;
    ty = ((e.clientY - b.top) / b.height - 0.5) * 2;
  });
  box.addEventListener('pointerleave', () => { tx = 0; ty = 0; });
  const draw = (dt, paused) => {
    if (!paused) t += dt;
    px += (tx - px) * 0.05; py += (ty - py) * 0.05;
    for (let i = 0; i < N; i++) {
      const b = base[i];
      p.set(b.x + Math.sin(t * b.sp + b.ph) * 0.18, b.y + Math.cos(t * b.sp * 0.8 + b.ph) * 0.22, b.z + Math.sin(t * b.sp * 0.6 + b.ph * 2) * 0.18);
      s.setScalar(b.size);
      m.compose(p, q, s);
      mesh.setMatrixAt(i, m);
    }
    mesh.instanceMatrix.needsUpdate = true;
    group.rotation.y = t * 0.06 + px * 0.25;
    group.rotation.x = py * 0.15;
    renderer.render(scene, camera);
  };
  const ro = new ResizeObserver(() => { fit(renderer, camera, box); draw(0, true); });
  ro.observe(box);
  fit(renderer, camera, box);
  draw(0, true);
  box.classList.add('has-gl');
  const loop = runLoop(box, draw);
  pauseState.subs.add(() => loop.kick());
}

/* ---------------------------------------------------------- princípio: quatro formações */
function story(THREE) {
  const canvas = document.getElementById('story-gl');
  if (!canvas) return;
  const stage = canvas.parentElement;
  const N = lowEnd ? 200 : 340;
  const r = rng(29);
  const renderer = makeRenderer(THREE, canvas);
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(CHAMBER, 9, 22);
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 80);
  camera.position.set(0, 0, 13);
  lights(THREE, scene);
  const geo = new THREE.SphereGeometry(1, lowEnd ? 14 : 22, lowEnd ? 10 : 14);
  const mesh = new THREE.InstancedMesh(geo, material(THREE), N);
  scene.add(mesh);

  const blood = (k) => new THREE.Color().setHSL(0.006, 0.72, 0.2 + k * 0.1);
  const grey = new THREE.Color(0xc9cfd6);
  // cada formação: posição, cor e escala por microesfera
  const F = [[], [], [], []];
  const narrow = stage.clientWidth < 600;
  const clusterC = narrow ? [[-1.9, -0.9], [-0.3, 0.95], [1.2, 0.05], [2.0, 1.55]] : [[-2.3, -1.4], [-0.3, 0.8], [1.5, -0.25], [2.5, 1.55]];
  for (let i = 0; i < N; i++) {
    const g = i % 4;
    const a = r() * Math.PI * 2, rad = Math.sqrt(r());
    const k = r();
    // 0: mancha de sangue seco no papel-filtro (disco largo, levemente inclinado)
    const sx = Math.cos(a) * rad * 3.4, sy = Math.sin(a) * rad * 2.6;
    F[0].push({ p: [sx, sy, (r() - 0.5) * 0.25], c: blood(k), s: 0.085 + r() * 0.06 });
    // 1: o picote. Só o que está dentro do disco de 3 mm permanece
    const inside = rad < 0.36;
    const pa = r() * Math.PI * 2, pr = Math.sqrt(r()) * 1.25;
    F[1].push({ p: inside ? [Math.cos(pa) * pr, Math.sin(pa) * pr, (r() - 0.5) * 0.3] : [sx * 1.6, sy * 1.6, -2 - r() * 3], c: inside ? blood(k + 0.25) : blood(k * 0.4), s: inside ? 0.12 + r() * 0.05 : 0 });
    // 2: ensaio em suspensão. Quatro conjuntos identificados por cor
    const u = r() * 2 - 1, b2 = r() * Math.PI * 2, rr = Math.cbrt(r()) * 4;
    F[2].push({ p: [Math.cos(b2) * Math.sqrt(1 - u * u) * rr * 1.3, u * rr * 0.9, Math.sin(b2) * Math.sqrt(1 - u * u) * rr], c: new THREE.Color(SPECTRAL[g]), s: 0.055 + Math.pow(r(), 2) * 0.07 });
    // 3: leitura. Mapa de classificação por cor (eixo x) e sinal (eixo y)
    F[3].push({ p: [clusterC[g][0] + gauss(r) * 0.3, clusterC[g][1] + gauss(r) * 0.3, (r() - 0.5) * 0.2], c: new THREE.Color(SPECTRAL[g]), s: 0.07 + r() * 0.03 });
  }
  const delay = Array.from({ length: N }, () => r());
  const ph = Array.from({ length: N }, () => r() * 100);
  const m = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3(), c = new THREE.Color();
  const tags = [...stage.querySelectorAll('[data-tag]')];
  const v = new THREE.Vector3();
  let t = 0;
  const draw = (dt, paused) => {
    if (!paused) t += dt;
    const prog = window.__storyProgress || 0;
    const k = Math.min(2, Math.floor(prog));
    const f = prog - k;
    const A = F[k], B = F[k + 1];
    // brownian só na suspensão; na leitura as microesferas param
    const wob = Math.max(0, 1 - Math.abs(prog - 2)) * 0.12 + 0.02;
    for (let i = 0; i < N; i++) {
      const e = smooth(clamp01((f - delay[i] * 0.35) / 0.65));
      const a = A[i], b = B[i];
      p.set(
        a.p[0] + (b.p[0] - a.p[0]) * e + Math.sin(t * 0.7 + ph[i]) * wob,
        a.p[1] + (b.p[1] - a.p[1]) * e + Math.cos(t * 0.6 + ph[i] * 1.3) * wob,
        a.p[2] + (b.p[2] - a.p[2]) * e + Math.sin(t * 0.5 + ph[i] * 0.7) * wob
      );
      s.setScalar(a.s + (b.s - a.s) * e);
      m.compose(p, q, s);
      mesh.setMatrixAt(i, m);
      c.copy(a.c).lerp(b.c, e);
      mesh.setColorAt(i, c);
    }
    mesh.instanceMatrix.needsUpdate = true;
    mesh.instanceColor.needsUpdate = true;
    // a câmera gira na suspensão e volta de frente para o mapa
    const spin = Math.max(0, 1 - Math.abs(prog - 2));
    mesh.rotation.y = Math.sin(t * 0.15) * 0.5 * spin;
    mesh.rotation.x = (prog < 1 ? 0.35 * (1 - prog) : 0) + Math.cos(t * 0.12) * 0.15 * spin;
    renderer.render(scene, camera);
    if (prog > 2.4) {
      tags.forEach((tag, g) => {
        v.set(clusterC[g][0], clusterC[g][1] + 0.75, 0).applyMatrix4(mesh.matrixWorld).project(camera);
        tag.style.left = ((v.x + 1) / 2 * 100).toFixed(2) + '%';
        tag.style.top = ((1 - v.y) / 2 * 100).toFixed(2) + '%';
      });
    }
  };
  const ro = new ResizeObserver(() => { fit(renderer, camera, stage); draw(0, true); });
  ro.observe(stage);
  fit(renderer, camera, stage);
  draw(0, true);
  stage.classList.add('has-gl');
  const loop = runLoop(stage, draw);
  addEventListener('scroll', () => loop.kick(), { passive: true });
  pauseState.subs.add(() => loop.kick());
}

/* ---------------------------------------------------------- inicialização preguiçosa */
async function boot() {
  let THREE;
  try { THREE = await import(THREE_URL); } catch (_) { return; } // sem rede: ficam as figuras SVG
  try { hero(THREE); story(THREE); wirePause(); } catch (err) { console.warn('Microesferas indisponíveis:', err); }
}

if (!reduce && !saveData && webglOk()) {
  const targets = ['hero-gl', 'story-gl'].map((id) => document.getElementById(id)).filter(Boolean);
  let started = false;
  const go = () => { if (started) return; started = true; boot(); };
  const io = new IntersectionObserver((e) => { if (e.some((x) => x.isIntersecting)) { io.disconnect(); (window.requestIdleCallback || setTimeout)(go, { timeout: 1200 }); } }, { rootMargin: '300px' });
  targets.forEach((t) => io.observe(t));
}
