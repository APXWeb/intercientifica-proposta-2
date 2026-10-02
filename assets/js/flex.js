/* Automação, de perto: Opentrons® Flex controlado pelo scroll.
 *
 * MODELO: não existe modelo 3D oficial público do Flex. A máquina abaixo é
 * construída em código a partir de fontes oficiais da Opentrons:
 *   - Manual do Flex, "System Specifications" e "Robot components"
 *     (docs.opentrons.com/flex): 87 × 69 × 84 cm (L × P × A), estrutura de aço e
 *     alumínio usinado, porta frontal e janelas laterais de policarbonato,
 *     tela de 7" na frente à direita, faixa de luz de status no topo frontal,
 *     câmera no canto superior esquerdo, deck de alumínio usinado, pórtico X/Y.
 *   - Definição de deck do código aberto (Opentrons/opentrons,
 *     shared-data/deck/definitions/5/ot3_standard.json): posições de 128 × 86 mm,
 *     passo de 164 mm (colunas) e 107 mm (linhas), A1 no fundo à esquerda.
 * Peças internas (forma exata do carro das pipetas, trilhos) são aproximações
 * visuais das fotos oficiais. SUBSTITUIR por asset oficial (GLB) se a Opentrons
 * ou o cliente fornecerem: basta trocar buildMachine() mantendo os nomes dos
 * grupos (door, gantry, carriage, pipettes, slots, screen, status).
 *
 * INTERAÇÃO: mesma lógica do NOIR (APX): cada [data-pose] do texto é uma âncora;
 * o scroll mistura a pose atual com a seguinte, com platôs para leitura, e a
 * câmera persegue a pose com amortecimento. Nada dispara por tempo.
 */

const THREE_URL = 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.min.js';
const ADDONS = 'https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/';

const root = document.getElementById('automacao-3d');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const saveData = !!(navigator.connection && navigator.connection.saveData);
const lowEnd = (navigator.deviceMemory && navigator.deviceMemory < 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4);

const clamp01 = (t) => Math.max(0, Math.min(1, t));
const smoother = (t) => t * t * t * (t * (t * 6 - 15) + 10);
const lerp = (a, b, t) => a + (b - a) * t;

/* ---------------------------------------------------------- poses
   cam/target em metros (máquina com a base no chão, frente para +z).
   shift: deslocamento horizontal do enquadramento (o texto fica à esquerda). */
const POSES = {
  intro:     { cam: [1.7, 1.1, 2.45], tgt: [0.02, 0.42, 0], fov: 30, shift: 0.15, door: 0, gz: 0.02, cx: 0.02, pz: 0, slots: 0, screen: 0.25, status: 0.6, led: 0.35, dims: 0 },
  estrutura: { cam: [-2.15, 1.25, 2.55], tgt: [0.02, 0.6, 0], fov: 30, shift: 0.15, door: 1, gz: 0.02, cx: 0.02, pz: 0, slots: 0, screen: 0.25, status: 0.6, led: 0.6, dims: 1 },
  deck:      { cam: [-0.62, 1.9, 1.8], tgt: [0.06, 0.24, -0.02], fov: 33, shift: 0.17, door: 0, gz: -0.22, cx: -0.12, pz: 0, slots: 1, screen: 0.25, status: 0.6, led: 1, dims: 0 },
  portico:   { cam: [-1.2, 1.12, 2.2], tgt: [0.02, 0.44, 0], fov: 30, shift: 0.15, door: 0, gz: 0.1, cx: 0.06, pz: 1, slots: 0.25, screen: 0.25, status: 0.6, led: 1, dims: 0 },
  interface: { cam: [0.9, 0.82, 1.9], tgt: [0.1, 0.56, 0.28], fov: 29, shift: 0.17, door: 0, gz: -0.05, cx: 0.0, pz: 0, slots: 0, screen: 1, status: 1, led: 0.6, dims: 0 },
  final:     { cam: [1.9, 1.12, 2.7], tgt: [0.02, 0.42, 0], fov: 30, shift: 0.15, door: 0, gz: 0.02, cx: 0.02, pz: 0, slots: 0, screen: 0.6, status: 1, led: 0.5, dims: 0 },
};
const KEYS = ['door', 'gz', 'cx', 'pz', 'slots', 'screen', 'status', 'led', 'dims', 'fov', 'shift'];

/* ---------------------------------------------------------- trilho de poses (lógica NOIR) */
const track = { anchors: [], target: {}, cur: null, weights: {} };
function measure() {
  const sy = scrollY;
  track.anchors = [...root.querySelectorAll('[data-pose]')].map((el) => {
    const r = el.getBoundingClientRect();
    return { el, name: el.dataset.pose, center: r.top + sy + r.height / 2 };
  });
}
function resolve(mobile) {
  // modo de captura das imagens estáticas (usado só pelas ferramentas de build)
  if (window.__forcePose && POSES[window.__forcePose]) {
    const P = POSES[window.__forcePose];
    track.weights = {}; Object.keys(POSES).forEach((n) => { track.weights[n] = n === window.__forcePose ? 1 : 0; });
    track.active = window.__forcePose;
    const out = { cam: P.cam.slice(), tgt: P.tgt.slice() };
    KEYS.forEach((k) => { out[k] = P[k]; });
    if (window.__noShift) out.shift = 0;
    return out;
  }
  const list = track.anchors;
  if (!list.length) return null;
  const y = scrollY + innerHeight * (mobile ? 0.68 : 0.5);
  let i = 0;
  while (i < list.length - 1 && list[i + 1].center <= y) i++;
  const a = list[i], b = list[Math.min(i + 1, list.length - 1)];
  const span = b.center - a.center;
  const raw = span > 0 ? clamp01((y - a.center) / span) : 0;
  const t = smoother(clamp01((raw - 0.18) / 0.64)); // platô: segura início e fim para leitura
  const A = POSES[a.name], B = POSES[b.name];
  const out = { cam: [0, 0, 0], tgt: [0, 0, 0] };
  for (let k = 0; k < 3; k++) { out.cam[k] = lerp(A.cam[k], B.cam[k], t); out.tgt[k] = lerp(A.tgt[k], B.tgt[k], t); }
  KEYS.forEach((k) => { out[k] = lerp(A[k], B[k], t); });
  track.weights = {};
  Object.keys(POSES).forEach((n) => { track.weights[n] = 0; });
  track.weights[a.name] += 1 - t;
  track.weights[b.name] += t;
  track.active = raw < 0.5 ? a.name : b.name;
  return out;
}

/* ---------------------------------------------------------- materiais e texturas */
function canvasTex(THREE, w, h, draw) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}

function brushedTex(THREE) {
  // alumínio escovado: ruído horizontal fino, usado como mapa de rugosidade
  const t = canvasTex(THREE, 512, 512, (g, w, h) => {
    g.fillStyle = '#8a8a8a'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 2600; i++) {
      const y = Math.random() * h, l = 40 + Math.random() * 260, x = Math.random() * w;
      const v = 110 + Math.random() * 60;
      g.strokeStyle = `rgba(${v},${v},${v},0.35)`; g.lineWidth = Math.random() * 1.2;
      g.beginPath(); g.moveTo(x, y); g.lineTo(x + l, y + (Math.random() - 0.5) * 0.6); g.stroke();
    }
  });
  t.colorSpace = THREE.NoColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

function plateTex(THREE) {
  // microplaca de 96 poços (8 × 12), ilustrativa
  return canvasTex(THREE, 512, 344, (g, w, h) => {
    g.fillStyle = '#e9edf0'; g.fillRect(0, 0, w, h);
    const px = w / 13.2, py = h / 9.2;
    for (let r = 0; r < 8; r++) for (let c = 0; c < 12; c++) {
      const x = px * (1.1 + c), y = py * (1.1 + r);
      const grd = g.createRadialGradient(x, y, 1, x, y, px * 0.42);
      grd.addColorStop(0, '#b9c1c8'); grd.addColorStop(1, '#d8dee3');
      g.fillStyle = grd; g.beginPath(); g.arc(x, y, px * 0.4, 0, Math.PI * 2); g.fill();
      g.strokeStyle = '#a7b0b8'; g.lineWidth = 1; g.stroke();
    }
  });
}

function screenTex(THREE) {
  // tela ligada: brilho neutro, sem simular a interface do fabricante
  return canvasTex(THREE, 512, 300, (g, w, h) => {
    const grd = g.createLinearGradient(0, 0, w, h);
    grd.addColorStop(0, '#22262b'); grd.addColorStop(1, '#111316');
    g.fillStyle = grd; g.fillRect(0, 0, w, h);
    g.fillStyle = 'rgba(230,234,238,0.08)';
    g.fillRect(0, 0, w, 46);
    g.fillStyle = 'rgba(230,234,238,0.05)';
    for (let i = 0; i < 3; i++) g.fillRect(28 + i * 160, 86, 140, 170);
  });
}

function contactTex(THREE) {
  // sombra de contato pré-calculada: o equipamento nunca flutua, mesmo sem sombras em tempo real
  return canvasTex(THREE, 512, 512, (g, w, h) => {
    const grd = g.createRadialGradient(w / 2, h / 2, w * 0.05, w / 2, h / 2, w * 0.5);
    grd.addColorStop(0, 'rgba(0,0,0,0.85)'); grd.addColorStop(0.45, 'rgba(0,0,0,0.55)'); grd.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = grd; g.fillRect(0, 0, w, h);
  });
}

function floorTex(THREE) {
  // piso que se dissolve no fundo da câmara: sem linha de horizonte
  return canvasTex(THREE, 1024, 1024, (g, w, h) => {
    const grd = g.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, w / 2);
    grd.addColorStop(0, 'rgba(34,36,40,1)'); grd.addColorStop(0.35, 'rgba(20,22,25,1)'); grd.addColorStop(1, 'rgba(10,12,15,0)');
    g.fillStyle = grd; g.fillRect(0, 0, w, h);
  });
}

function roundedRect(THREE, x0, y0, x1, y1, r) {
  const s = new THREE.Shape();
  s.moveTo(x0 + r, y0); s.lineTo(x1 - r, y0); s.quadraticCurveTo(x1, y0, x1, y0 + r);
  s.lineTo(x1, y1 - r); s.quadraticCurveTo(x1, y1, x1 - r, y1); s.lineTo(x0 + r, y1);
  s.quadraticCurveTo(x0, y1, x0, y1 - r); s.lineTo(x0, y0 + r); s.quadraticCurveTo(x0, y0, x0 + r, y0);
  return s;
}
function holePath(THREE, x0, y0, x1, y1, r) {
  const p = new THREE.Path();
  p.moveTo(x0 + r, y0); p.lineTo(x1 - r, y0); p.quadraticCurveTo(x1, y0, x1, y0 + r);
  p.lineTo(x1, y1 - r); p.quadraticCurveTo(x1, y1, x1 - r, y1); p.lineTo(x0 + r, y1);
  p.quadraticCurveTo(x0, y1, x0, y1 - r); p.lineTo(x0, y0 + r); p.quadraticCurveTo(x0, y0, x0 + r, y0);
  return p;
}

/* ---------------------------------------------------------- a máquina (87 × 69 × 84 cm) */
function buildMachine(THREE, { RoundedBoxGeometry }, quality) {
  const W = 0.87, D = 0.69, H = 0.84, FZ = D / 2;
  const m = new THREE.Group();
  const parts = {};
  const brushed = brushedTex(THREE);

  const black = new THREE.MeshPhysicalMaterial({ color: 0x15171a, roughness: 0.48, metalness: 0.15, clearcoat: 0.35, clearcoatRoughness: 0.5 });
  const blackMatte = new THREE.MeshStandardMaterial({ color: 0x0f1113, roughness: 0.85, metalness: 0.05 });
  const alu = new THREE.MeshStandardMaterial({ color: 0xc8ccd1, metalness: 0.88, roughness: 0.34, roughnessMap: brushed });
  const aluLight = new THREE.MeshStandardMaterial({ color: 0xdfe3e7, metalness: 0.75, roughness: 0.3, roughnessMap: brushed });
  const deckMat = new THREE.MeshStandardMaterial({ color: 0x9da3aa, metalness: 0.8, roughness: 0.38, roughnessMap: brushed });
  const interior = new THREE.MeshStandardMaterial({ color: 0x1d2126, roughness: 0.9, metalness: 0.1 });
  const glass = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.04, metalness: 0, transparent: true, opacity: 0.1, envMapIntensity: 1.6, side: THREE.DoubleSide, depthWrite: false });
  const tint = new THREE.MeshPhysicalMaterial({ color: 0x0b0d10, roughness: 0.05, metalness: 0, transparent: true, opacity: 0.42, envMapIntensity: 1.3, side: THREE.DoubleSide, depthWrite: false });
  const setShadow = (o) => { if (quality.shadows) { o.castShadow = true; o.receiveShadow = true; } return o; };
  const add = (geo, mat, x, y, z, parent = m) => { const o = setShadow(new THREE.Mesh(geo, mat)); o.position.set(x, y, z); parent.add(o); return o; };
  const ext = (shape, depth, bevel = 0.004) => new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 3, curveSegments: 16 });

  // base, tampo e fundo
  add(new RoundedBoxGeometry(W - 0.03, 0.13, D - 0.03, 3, 0.01), blackMatte, 0, 0.075, 0);
  add(new RoundedBoxGeometry(W - 0.02, 0.022, D - 0.02, 3, 0.008), black, 0, H - 0.011, 0);
  add(new THREE.BoxGeometry(W - 0.05, H - 0.05, 0.012), interior, 0, H / 2, -FZ + 0.012);
  [-1, 1].forEach((sx) => [-1, 1].forEach((sz) => add(new THREE.CylinderGeometry(0.018, 0.02, 0.012, 20), blackMatte, sx * (W / 2 - 0.07), 0.006, sz * (D / 2 - 0.07))));

  // moldura frontal preta de cantos arredondados, com a abertura da porta
  const front = roundedRect(THREE, -W / 2, 0.01, W / 2, H, 0.045);
  front.holes.push(holePath(THREE, -0.405, 0.135, 0.405, 0.75, 0.018));
  add(ext(front, 0.026), black, 0, 0, FZ - 0.03);
  // rebaixo da pega na faixa inferior
  add(new RoundedBoxGeometry(0.4, 0.024, 0.01, 2, 0.004), blackMatte, -0.07, 0.07, FZ + 0.0);

  // laterais em alumínio com janela escura
  [-1, 1].forEach((sx) => {
    const side = roundedRect(THREE, -D / 2, 0.01, D / 2, H, 0.045);
    side.holes.push(holePath(THREE, -0.29, 0.17, 0.27, 0.77, 0.016));
    const g = ext(side, 0.016, 0.003);
    const o = add(g, alu, sx > 0 ? W / 2 - 0.016 : -W / 2, 0, 0);
    o.rotation.y = sx > 0 ? -Math.PI / 2 : -Math.PI / 2;
    o.position.x = sx > 0 ? W / 2 : -W / 2 + 0.016;
    const win = add(new THREE.PlaneGeometry(0.56, 0.6), tint, sx * (W / 2 - 0.006), 0.47, -0.01);
    win.rotation.y = Math.PI / 2;
    win.castShadow = false;
    // tampas das alças e ventilação na faixa inferior
    [-0.2, 0.2].forEach((z) => { const cap = add(new THREE.CylinderGeometry(0.014, 0.014, 0.006, 24), aluLight, sx * (W / 2 + 0.002), 0.09, z); cap.rotation.z = Math.PI / 2; });
    [-0.09, 0.07].forEach((z) => add(new RoundedBoxGeometry(0.004, 0.035, 0.11, 2, 0.002), blackMatte, sx * (W / 2 + 0.001), 0.075, z));
  });

  // interior: deck de alumínio usinado (855 × 582 mm)
  const deckY = 0.145;
  add(new RoundedBoxGeometry(0.84, 0.012, 0.58, 2, 0.004), deckMat, 0, deckY - 0.006, 0);
  // posições: 128 × 86 mm, passo 164 × 107 mm; A1 no fundo à esquerda
  const colX = [-0.19, -0.026, 0.138, 0.302];
  const rowZ = { A: -0.16, B: -0.053, C: 0.054, D: 0.161 };
  const slotGeo = new RoundedBoxGeometry(0.128, 0.004, 0.086, 2, 0.003);
  const slotMat = new THREE.MeshStandardMaterial({ color: 0x8f969e, metalness: 0.82, roughness: 0.4, roughnessMap: brushed });
  const clipMat = new THREE.MeshStandardMaterial({ color: 0x8e959d, metalness: 0.7, roughness: 0.45 });
  const clipGeo = new THREE.BoxGeometry(0.012, 0.006, 0.004);
  parts.slots = [];
  const lineMat = new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 });
  Object.entries(rowZ).forEach(([row, z]) => colX.forEach((x, ci) => {
    const name = row + (ci + 1);
    const s = add(slotGeo, slotMat, x, deckY - 0.0005 + (ci === 3 ? 0.006 : 0), z);
    s.castShadow = false;
    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([a, b]) => add(clipGeo, clipMat, x + a * 0.058, deckY + 0.006, z + b * 0.04));
    const edge = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(0.13, 0.001, 0.088)), lineMat.clone());
    edge.position.set(x, deckY + 0.009 + (ci === 3 ? 0.006 : 0), z);
    m.add(edge);
    parts.slots.push({ name, edge, order: ci === 3 ? 12 + Object.keys(rowZ).indexOf(row) : Object.keys(rowZ).indexOf(row) * 3 + ci, staging: ci === 3, x, z });
  }));
  // área à esquerda das colunas (posição de expansão)
  add(new RoundedBoxGeometry(0.11, 0.004, 0.4, 2, 0.003), slotMat, -0.345, deckY + 0.002, -0.05);

  // material de laboratório ilustrativo: ponteiras azuis e microplacas
  const rackMat = new THREE.MeshPhysicalMaterial({ color: 0x9aa3ad, roughness: 0.3, metalness: 0, transparent: true, opacity: 0.9, clearcoat: 0.6 });
  const tipMat = new THREE.MeshPhysicalMaterial({ color: 0xeef1f4, roughness: 0.25, transparent: true, opacity: 0.9 });
  const tipGeo = new THREE.CylinderGeometry(0.0034, 0.0016, 0.034, quality.lite ? 6 : 10, 1, true);
  const racks = [['A', 0], ['A', 1], ['B', 0]];
  const tips = new THREE.InstancedMesh(tipGeo, tipMat, racks.length * 96);
  let ti = 0;
  const mtx = new THREE.Matrix4();
  racks.forEach(([row, ci]) => {
    const x = colX[ci], z = rowZ[row];
    add(new RoundedBoxGeometry(0.124, 0.052, 0.082, 2, 0.004), rackMat, x, deckY + 0.032, z);
    for (let r = 0; r < 8; r++) for (let c = 0; c < 12; c++) {
      mtx.makeTranslation(x - 0.0495 + c * 0.009, deckY + 0.075, z - 0.0315 + r * 0.009);
      tips.setMatrixAt(ti++, mtx);
    }
  });
  m.add(tips);
  const plateTop = new THREE.MeshStandardMaterial({ map: plateTex(THREE), roughness: 0.4 });
  const plateSide = new THREE.MeshStandardMaterial({ color: 0xe6eaee, roughness: 0.45 });
  [['C', 1], ['D', 1], ['C', 0]].forEach(([row, ci]) => {
    const p = add(new THREE.BoxGeometry(0.127, 0.015, 0.085), [plateSide, plateSide, plateTop, plateSide, plateSide, plateSide], colX[ci], deckY + 0.012, rowZ[row]);
    p.userData.plate = true;
  });

  // pórtico: coberturas dos trilhos Y nas laterais, viga X móvel, carro e pipetas
  [-1, 1].forEach((sx) => add(new RoundedBoxGeometry(0.02, 0.1, 0.6, 2, 0.006), aluLight, sx * 0.395, 0.5, -0.02));
  const gantry = new THREE.Group(); m.add(gantry);
  add(new RoundedBoxGeometry(0.77, 0.085, 0.1, 3, 0.01), aluLight, 0, 0.5, 0, gantry);
  const carriage = new THREE.Group(); gantry.add(carriage);
  add(new RoundedBoxGeometry(0.15, 0.36, 0.09, 3, 0.01), black, 0, 0.5, 0.085, carriage);
  add(new RoundedBoxGeometry(0.06, 0.3, 0.012, 2, 0.004), alu, -0.035, 0.5, 0.133, carriage);
  const pip = new THREE.Group(); carriage.add(pip);
  [-0.04, 0.045].forEach((x, i) => {
    add(new RoundedBoxGeometry(0.048, 0.22, 0.052, 3, 0.008), i ? black : aluLight, x, 0.43, 0.16, pip);
    add(new THREE.CylinderGeometry(0.006, 0.0025, 0.05, 16), blackMatte, x, 0.296, 0.16, pip);
    [0.5, 0.38].forEach((y) => add(new THREE.BoxGeometry(0.05, 0.003, 0.054), blackMatte, x, y, 0.16, pip));
    add(new RoundedBoxGeometry(0.03, 0.04, 0.008, 2, 0.003), alu, x, 0.47, 0.19, pip);
  });
  parts.door = null; parts.gantry = gantry; parts.carriage = carriage; parts.pipettes = pip;

  // porta frontal de policarbonato: dobradiças no topo, abre para cima
  const doorPivot = new THREE.Group(); doorPivot.position.set(0, 0.75, FZ + 0.004); m.add(doorPivot);
  const doorFrame = roundedRect(THREE, -0.405, -0.615, 0.25, 0, 0.012);
  doorFrame.holes.push(holePath(THREE, -0.39, -0.6, 0.235, -0.015, 0.008));
  add(ext(doorFrame, 0.008, 0.002), blackMatte, 0, 0, 0, doorPivot);
  add(new THREE.PlaneGeometry(0.625, 0.585), glass, -0.0775, -0.3075, 0.005, doorPivot).castShadow = false;
  [-0.36, 0.2].forEach((x) => add(new RoundedBoxGeometry(0.03, 0.02, 0.02, 2, 0.004), blackMatte, x, 0.005, -0.004, doorPivot));
  parts.door = doorPivot;
  // painel fixo à direita da porta, com a tela de 7"
  add(new THREE.PlaneGeometry(0.15, 0.585), glass, 0.33, 0.4425, FZ + 0.004).castShadow = false;
  const screen = new THREE.Group(); screen.position.set(0.33, 0.52, FZ + 0.03); screen.rotation.x = -0.08; m.add(screen);
  add(new RoundedBoxGeometry(0.205, 0.135, 0.016, 3, 0.006), alu, 0, 0, -0.003, screen);
  add(new RoundedBoxGeometry(0.195, 0.125, 0.016, 3, 0.005), black, 0, 0, 0, screen);
  const screenMat = new THREE.MeshBasicMaterial({ map: screenTex(THREE), toneMapped: false });
  add(new THREE.PlaneGeometry(0.155, 0.093), screenMat, 0, 0, 0.0085, screen);
  add(new THREE.BoxGeometry(0.03, 0.05, 0.03), blackMatte, 0, -0.08, -0.02, screen);
  parts.screen = screenMat;

  // luz de status no topo frontal e câmera no canto superior esquerdo
  const statusMat = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  add(new RoundedBoxGeometry(0.38, 0.008, 0.006, 2, 0.003), statusMat, 0.03, 0.795, FZ - 0.001);
  parts.status = statusMat;
  const cam = add(new THREE.CylinderGeometry(0.008, 0.008, 0.006, 20), new THREE.MeshPhysicalMaterial({ color: 0x050607, roughness: 0.1, clearcoat: 1 }), -0.385, 0.795, FZ);
  cam.rotation.x = Math.PI / 2;

  // faixas de LED brancas nas bordas internas superiores
  const ledMat = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, transparent: true, opacity: 0.4 });
  add(new THREE.BoxGeometry(0.78, 0.006, 0.006), ledMat, 0, 0.738, FZ - 0.05);
  [-1, 1].forEach((sx) => add(new THREE.BoxGeometry(0.006, 0.006, 0.56), ledMat, sx * 0.4, 0.738, 0));
  parts.led = ledMat;

  return { group: m, parts, deckY, colX, rowZ, W, D, H };
}

/* ---------------------------------------------------------- cotas (linhas técnicas) */
function buildDims(THREE, M) {
  const mat = new THREE.MeshBasicMaterial({ color: 0xe6eaee, transparent: true, opacity: 0, toneMapped: false, depthWrite: false });
  const g = new THREE.Group();
  const a = new THREE.Vector3(), b = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);
  // cada par de pontos vira uma barra de 3 mm: legível em qualquer resolução
  const seg = (pts) => {
    for (let k = 0; k < pts.length; k += 2) {
      a.set(...pts[k]); b.set(...pts[k + 1]);
      const len = a.distanceTo(b);
      const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.0016, 0.0016, len, 6), mat);
      bar.position.copy(a).add(b).multiplyScalar(0.5);
      bar.quaternion.setFromUnitVectors(up, b.clone().sub(a).normalize());
      g.add(bar);
    }
  };
  const t = 0.025, W = M.W / 2, D = M.D / 2, H = M.H;
  // largura (frente, abaixo), altura (canto frontal esquerdo), profundidade (lado direito, abaixo)
  seg([[-W, -0.05, D + 0.06], [W, -0.05, D + 0.06], [-W, -0.05 - t, D + 0.06], [-W, -0.05 + t, D + 0.06], [W, -0.05 - t, D + 0.06], [W, -0.05 + t, D + 0.06]]);
  seg([[-W - 0.07, 0, D], [-W - 0.07, H, D], [-W - 0.07 - t, 0, D], [-W - 0.07 + t, 0, D], [-W - 0.07 - t, H, D], [-W - 0.07 + t, H, D]]);
  seg([[W + 0.07, -0.05, -D], [W + 0.07, -0.05, D], [W + 0.07 - t, -0.05, -D], [W + 0.07 + t, -0.05, -D], [W + 0.07 - t, -0.05, D], [W + 0.07 + t, -0.05, D]]);
  return { group: g, mat };
}

/* ---------------------------------------------------------- cena */
async function boot() {
  let THREE, RB, RE, RA;
  try {
    [THREE, RB, RE, RA] = await Promise.all([import(THREE_URL), import(ADDONS + 'geometries/RoundedBoxGeometry.js'), import(ADDONS + 'environments/RoomEnvironment.js'), import(ADDONS + 'lights/RectAreaLightUniformsLib.js')]);
  } catch (_) { return; } // sem rede: ficam as imagens estáticas
  const stage = root.querySelector('.auto__stage');
  const canvas = root.querySelector('canvas');
  const mobileQ = matchMedia('(max-width: 900px)');
  const quality = { shadows: !lowEnd && !mobileQ.matches, lite: lowEnd || mobileQ.matches };

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !quality.lite, powerPreference: 'high-performance', alpha: false });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, quality.lite ? 1.25 : 1.75));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.setClearColor(0x0a0c0f, 1);
  // fundo da câmara: cor única, sem horizonte
  if (quality.shadows) { renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap; }

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RE.RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.55;

  const floor = new THREE.Mesh(new THREE.PlaneGeometry(9, 9), new THREE.MeshBasicMaterial({ map: floorTex(THREE), transparent: true, depthWrite: false, toneMapped: false, fog: false }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -0.001; scene.add(floor);
  const contact = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.3), new THREE.MeshBasicMaterial({ map: contactTex(THREE), transparent: true, depthWrite: false, toneMapped: false }));
  contact.rotation.x = -Math.PI / 2; contact.position.y = 0.001; scene.add(contact);
  if (quality.shadows) {
    const catcher = new THREE.Mesh(new THREE.PlaneGeometry(6, 6), new THREE.ShadowMaterial({ opacity: 0.45 }));
    catcher.rotation.x = -Math.PI / 2; catcher.position.y = 0.002; catcher.receiveShadow = true; scene.add(catcher);
  }

  const hemi = new THREE.HemisphereLight(0xe8ecf0, 0x0a0c0f, 0.35); scene.add(hemi);
  const key = new THREE.DirectionalLight(0xfff4e8, 2.4); key.position.set(-2.2, 3.2, 2.6); scene.add(key);
  if (quality.shadows) { key.castShadow = true; key.shadow.mapSize.set(2048, 2048); key.shadow.camera.left = -1.2; key.shadow.camera.right = 1.2; key.shadow.camera.top = 1.4; key.shadow.camera.bottom = -0.6; key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02; key.shadow.radius = 4; }
  const rim = new THREE.DirectionalLight(0xdfe7f0, 1.5); rim.position.set(2.6, 1.6, -2.4); scene.add(rim);
  // faixas de LED brancas nas bordas superiores internas iluminam o deck (luz de área)
  RA.RectAreaLightUniformsLib.init();
  const inner = new THREE.RectAreaLight(0xffffff, 0, 0.76, 0.5);
  inner.position.set(0, 0.73, 0.0); inner.lookAt(0, 0, 0); scene.add(inner);

  const M = buildMachine(THREE, { RoundedBoxGeometry: RB.RoundedBoxGeometry }, quality);
  scene.add(M.group);
  const dims = buildDims(THREE, M); scene.add(dims.group);

  const camera = new THREE.PerspectiveCamera(30, 1, 0.05, 30);
  const pins = [...root.querySelectorAll('[data-pin]')];
  const pinVec = new THREE.Vector3();

  // estado amortecido
  let cur = null;
  const fit = () => {
    const w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  fit();
  new ResizeObserver(() => { fit(); measure(); }).observe(stage);
  measure();
  addEventListener('load', measure);
  document.fonts && document.fonts.ready.then(measure);

  let pointerX = 0, pointerY = 0, px = 0, py = 0;
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    stage.addEventListener('pointermove', (e) => { const b = stage.getBoundingClientRect(); pointerX = (e.clientX - b.left) / b.width - 0.5; pointerY = (e.clientY - b.top) / b.height - 0.5; });
    stage.addEventListener('pointerleave', () => { pointerX = 0; pointerY = 0; });
  }

  const rail = [...root.querySelectorAll('.auto__rail button')];
  let lastActive = '';
  const tmpCam = new THREE.Vector3(), tmpTgt = new THREE.Vector3();

  function frame(dt) {
    const mobile = mobileQ.matches;
    const target = resolve(mobile);
    if (!target) return;
    if (!cur) cur = JSON.parse(JSON.stringify(target));
    const k = 1 - Math.exp(-dt * 7);
    for (let i = 0; i < 3; i++) { cur.cam[i] = lerp(cur.cam[i], target.cam[i], k); cur.tgt[i] = lerp(cur.tgt[i], target.tgt[i], k); }
    KEYS.forEach((n) => { cur[n] = lerp(cur[n], target[n], k); });

    // câmera: no celular afasta para caber e centraliza
    tmpTgt.set(cur.tgt[0], cur.tgt[1], cur.tgt[2]);
    tmpCam.set(cur.cam[0], cur.cam[1], cur.cam[2]);
    const fitK = mobile ? Math.max(1, 1.12 / camera.aspect) : Math.max(1, 1.5 / camera.aspect);
    tmpCam.sub(tmpTgt).multiplyScalar(fitK).add(tmpTgt);
    px = lerp(px, pointerX, 0.05); py = lerp(py, pointerY, 0.05);
    camera.position.set(tmpCam.x + px * 0.12, tmpCam.y - py * 0.06, tmpCam.z);
    camera.fov = cur.fov;
    camera.lookAt(tmpTgt);
    camera.filmOffset = mobile ? 0 : -cur.shift * camera.filmGauge;
    camera.updateProjectionMatrix();

    // peças
    M.parts.door.rotation.x = -cur.door * 2.45; // dobradiças no topo: a porta sobe
    M.parts.gantry.position.z = cur.gz;
    M.parts.carriage.position.x = cur.cx;
    M.parts.pipettes.position.y = -cur.pz * 0.075;
    M.parts.screen.color.setScalar(0.35 + cur.screen * 0.75);
    M.parts.status.color.setScalar(0.45 + cur.status * 0.55);
    M.parts.led.opacity = 0.25 + cur.led * 0.75;
    inner.intensity = cur.led * 3.2;
    M.parts.slots.forEach((s) => {
      const t = clamp01(cur.slots * 17 - s.order);
      s.edge.material.opacity = t * (s.staging ? 0.45 : 0.9);
    });
    dims.mat.opacity = cur.dims * 0.75;

    renderer.render(scene, camera);

    // marcadores DOM projetados
    const w = stage.clientWidth, h = stage.clientHeight;
    pins.forEach((p) => {
      const weight = p.dataset.for.split(' ').reduce((s, n) => s + (track.weights[n] || 0), 0);
      const vis = clamp01((weight - 0.55) / 0.3);
      if (vis <= 0.001) { p.style.opacity = 0; p.style.visibility = 'hidden'; return; }
      const [x, y, z] = p.dataset.pin.split(',').map(Number);
      pinVec.set(x, y, z);
      if (p.dataset.part === 'carriage') pinVec.x += cur.cx, pinVec.z += cur.gz;
      pinVec.project(camera);
      p.style.visibility = 'visible';
      p.style.opacity = vis;
      const sx = (pinVec.x + 1) / 2 * w;
      if (!p.classList.contains('pin--tag')) p.classList.toggle('pin--left', sx > w * (mobile ? 0.55 : 0.72)); // rótulo para dentro da tela
      p.style.transform = `translate(${sx.toFixed(1)}px, ${((1 - pinVec.y) / 2 * h).toFixed(1)}px)`;
    });

    if (track.active !== lastActive) {
      lastActive = track.active;
      rail.forEach((b) => b.setAttribute('aria-current', b.dataset.go === lastActive ? 'step' : 'false'));
      root.querySelectorAll('[data-pose]').forEach((s) => s.classList.toggle('is-active', s.dataset.pose === lastActive));
    }
  }

  // laço apenas com a seção visível
  let visible = false, raf = 0, last = performance.now(), settle = 0;
  const loop = (now) => {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    frame(dt);
    settle = Math.max(0, settle - dt);
    raf = visible && !document.hidden ? requestAnimationFrame(loop) : 0;
  };
  const start = () => { if (!raf && visible && !document.hidden) { last = performance.now(); raf = requestAnimationFrame(loop); } };
  new IntersectionObserver((e) => { visible = e[0].isIntersecting; start(); }, { rootMargin: '200px' }).observe(root);
  document.addEventListener('visibilitychange', start);
  addEventListener('resize', measure);

  root.classList.add('has-gl');
  frame(1);
  window.__flexReady = true;
}

/* ---------------------------------------------------------- trilho de navegação e estado sem WebGL */
function wireRail() {
  root.querySelectorAll('.auto__rail button').forEach((b) => b.addEventListener('click', () => {
    const el = root.querySelector(`[data-pose="${b.dataset.go}"]`);
    if (el) el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
  }));
  // sem WebGL ou com movimento reduzido: troca a imagem estática conforme a etapa
  const imgs = [...root.querySelectorAll('.auto__still img')];
  const steps = [...root.querySelectorAll('[data-pose]')];
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      const name = e.target.dataset.pose;
      steps.forEach((s) => s.classList.toggle('is-active', s === e.target));
      imgs.forEach((i) => i.classList.toggle('is-on', i.dataset.still === name));
      root.querySelectorAll('.auto__rail button').forEach((b) => b.setAttribute('aria-current', b.dataset.go === name ? 'step' : 'false'));
    });
  }, { rootMargin: '-45% 0px -45% 0px' });
  steps.forEach((s) => io.observe(s));
}

if (root) {
  wireRail();
  const ok = (() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (_) { return false; } })();
  if (!reduce && !saveData && ok) {
    const io = new IntersectionObserver((e) => {
      if (!e.some((x) => x.isIntersecting)) return;
      io.disconnect();
      (window.requestIdleCallback || setTimeout)(boot, { timeout: 800 });
    }, { rootMargin: '1200px 0px' });
    io.observe(root);
  }
}
