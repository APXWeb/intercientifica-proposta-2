/* Leitura multiplex: a antiga etapa 4 das microesferas, agora isolada.
   As microesferas em suspensão se organizam no mapa de classificação
   (cor × sinal) conforme a seção atravessa a tela. Representação ilustrativa;
   a figura SVG estática já está na página e vale sem WebGL ou com movimento reduzido. */

const THREE_URL = 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.min.js';
const SPECTRAL = [0xff5a47, 0xffb547, 0x5fd3c2, 0x9daaff];
const CHAMBER = 0x0a0c0f;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const saveData = !!(navigator.connection && navigator.connection.saveData);
const lowEnd = (navigator.deviceMemory && navigator.deviceMemory < 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4);

function rng(seed) { return () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646; }
const gauss = (r) => { let u = 0, v = 0; while (!u) u = r(); while (!v) v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
const smooth = (t) => t * t * (3 - 2 * t);
const clamp01 = (t) => Math.max(0, Math.min(1, t));

async function boot(stage) {
  let THREE;
  try { THREE = await import(THREE_URL); } catch (_) { return; }
  const canvas = stage.querySelector('canvas');
  const section = stage.closest('section');
  const N = lowEnd ? 200 : 320;
  const r = rng(29);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !lowEnd, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, lowEnd ? 1 : 1.75));
  renderer.setClearColor(CHAMBER, 1);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(CHAMBER, 9, 22);
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 80);
  camera.position.set(0, 0, 13);
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-4, 6, 8); scene.add(key);
  const rim = new THREE.DirectionalLight(0xbfd4ff, 1.6); rim.position.set(5, -2, -6); scene.add(rim);
  const mat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.32, clearcoat: 1, clearcoatRoughness: 0.25, sheen: 0.4 });
  const mesh = new THREE.InstancedMesh(new THREE.SphereGeometry(1, lowEnd ? 14 : 22, lowEnd ? 10 : 14), mat, N);
  scene.add(mesh);

  const narrow = () => stage.clientWidth < 600;
  const centers = () => (narrow() ? [[-1.9, -0.9], [-0.3, 0.95], [1.2, 0.05], [2.0, 1.55]] : [[-2.3, -1.4], [-0.3, 0.8], [1.5, -0.25], [2.5, 1.55]]);
  const from = [], to = [], size = [], delay = [], ph = [], jitter = [];
  for (let i = 0; i < N; i++) {
    const g = i % 4;
    const u = r() * 2 - 1, b = r() * Math.PI * 2, rr = Math.cbrt(r()) * 4;
    from.push([Math.cos(b) * Math.sqrt(1 - u * u) * rr * 1.3, u * rr * 0.9, Math.sin(b) * Math.sqrt(1 - u * u) * rr]);
    jitter.push([gauss(r) * 0.3, gauss(r) * 0.3, (r() - 0.5) * 0.2]);
    size.push([0.055 + Math.pow(r(), 2) * 0.07, 0.07 + r() * 0.03]);
    delay.push(r()); ph.push(r() * 100);
    mesh.setColorAt(i, new THREE.Color(SPECTRAL[g]));
  }
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), s = new THREE.Vector3(), p = new THREE.Vector3(), v = new THREE.Vector3();
  const tags = [...stage.querySelectorAll('[data-tag]')];
  let t = 0, prog = 0, cur = 0;

  const measure = () => {
    // 0 quando a seção entra pela base, 1 quando o palco está centralizado
    const b = stage.getBoundingClientRect();
    const mid = b.top + b.height / 2;
    prog = clamp01((innerHeight * 1.08 - mid) / (innerHeight * 0.48));
  };
  const draw = (dt) => {
    const prev = cur;
    cur += (prog - cur) * (1 - Math.exp(-dt * 6));
    t += Math.abs(cur - prev) * 9; // o tempo só anda com o scroll: nada se move sozinho
    const C = centers();
    const wob = Math.sin(Math.PI * cur) * 0.12;
    for (let i = 0; i < N; i++) {
      const g = i % 4;
      const e = smooth(clamp01((cur - delay[i] * 0.3) / 0.7));
      const a = from[i], j = jitter[i];
      p.set(
        a[0] + (C[g][0] + j[0] - a[0]) * e + Math.sin(t * 0.7 + ph[i]) * wob,
        a[1] + (C[g][1] + j[1] - a[1]) * e + Math.cos(t * 0.6 + ph[i] * 1.3) * wob,
        a[2] + (j[2] - a[2]) * e + Math.sin(t * 0.5 + ph[i] * 0.7) * wob
      );
      s.setScalar(size[i][0] + (size[i][1] - size[i][0]) * e);
      m4.compose(p, q, s);
      mesh.setMatrixAt(i, m4);
    }
    mesh.instanceMatrix.needsUpdate = true;
    mesh.rotation.y = Math.sin(t * 0.15) * 0.5 * (1 - cur) * Math.min(1, t);
    renderer.render(scene, camera);
    stage.dataset.formed = cur > 0.66 ? 'true' : 'false';
    tags.forEach((tag, g) => {
      v.set(C[g][0], C[g][1] + 0.75, 0).applyMatrix4(mesh.matrixWorld).project(camera);
      tag.style.left = ((v.x + 1) / 2 * 100).toFixed(2) + '%';
      tag.style.top = ((1 - v.y) / 2 * 100).toFixed(2) + '%';
    });
  };
  const fit = () => {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.position.z = 13 * Math.max(1, 1.2 / camera.aspect);
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(() => { fit(); measure(); draw(0); }).observe(stage);
  fit(); measure(); draw(0);
  stage.classList.add('has-gl');
  addEventListener('scroll', measure, { passive: true });

  let visible = false, raf = 0, last = performance.now();
  const loop = (now) => { const dt = Math.min(0.05, (now - last) / 1000); last = now; draw(dt); raf = visible && !document.hidden ? requestAnimationFrame(loop) : 0; };
  const start = () => { if (!raf && visible && !document.hidden) { last = performance.now(); raf = requestAnimationFrame(loop); } };
  new IntersectionObserver((e) => { visible = e[0].isIntersecting; start(); }, { rootMargin: '100px' }).observe(section);
  document.addEventListener('visibilitychange', start);
}

const stage = document.getElementById('multiplex-stage');
if (stage && !reduce && !saveData) {
  const ok = (() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (_) { return false; } })();
  if (ok) {
    const io = new IntersectionObserver((e) => { if (e.some((x) => x.isIntersecting)) { io.disconnect(); boot(stage); } }, { rootMargin: '600px 0px' });
    io.observe(stage);
  }
}
