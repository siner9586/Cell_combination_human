import './style.css';
import * as THREE from 'three';

const canvas = document.querySelector('#scene');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);

const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x030712, 0.045);

const camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(0, 0.8, 14);

scene.add(new THREE.AmbientLight(0xaecbff, 0.42));
const key = new THREE.PointLight(0xfef3c7, 2.2, 80); key.position.set(7, 7, 8); scene.add(key);
const rim = new THREE.PointLight(0x93c5fd, 1.4, 80); rim.position.set(-8, -4, 9); scene.add(rim);

const stages = [
  ['单细胞：生命的起点', '边界、信息、能量与响应能力在一个动态系统中聚合。'],
  ['分裂：从一到多', '数量增加只是表象，真正重要的是细胞之间的关系开始出现。'],
  ['分化：细胞获得身份', '相同起点的细胞在不同位置与时间中走向不同命运。'],
  ['形态发生：身体蓝图浮现', '组织层折叠、迁移与反馈，生成整体形态。'],
  ['器官形成：局部功能模块生成', '神经、循环、骨骼、肌肉与代谢结构从细胞群中涌现。'],
  ['系统耦合：生命体成为整体', '多系统以节律、信号和反馈共同维持动态秩序。'],
  ['涌现：从细胞到人', '微观行为跨越尺度，汇聚成完整的人形生命轮廓。'],
  ['边界：理解生命，而非制造生命', '科学理解必须伴随敬畏、边界与责任。']
];

const stageText = document.querySelector('#stageText');
const progressBar = document.querySelector('#progressBar');

const group = new THREE.Group();
scene.add(group);

function glowMaterial(color, opacity = 0.62) {
  return new THREE.MeshPhysicalMaterial({ color, transparent: true, opacity, roughness: 0.25, metalness: 0.05, transmission: 0.25, clearcoat: 0.4, emissive: color, emissiveIntensity: 0.16, depthWrite: false });
}

const membrane = new THREE.Mesh(new THREE.SphereGeometry(1.35, 96, 96), glowMaterial(0x9dd6ff, 0.26));
group.add(membrane);
const nucleus = new THREE.Mesh(new THREE.SphereGeometry(0.42, 64, 64), glowMaterial(0xf8e7ff, 0.54));
group.add(nucleus);

const helixPts = [];
for (let i = 0; i < 220; i++) {
  const t = i / 18;
  helixPts.push(new THREE.Vector3(Math.cos(t) * 0.32, (i - 110) / 150, Math.sin(t) * 0.32));
}
const helix = new THREE.Line(new THREE.BufferGeometry().setFromPoints(helixPts), new THREE.LineBasicMaterial({ color: 0xfff2a8, transparent: true, opacity: 0.7 }));
group.add(helix);

function makeParticles(count, spread, palette) {
  const geo = new THREE.BufferGeometry();
  const pos = new Float32Array(count * 3);
  const col = new Float32Array(count * 3);
  const colors = palette.map(c => new THREE.Color(c));
  for (let i = 0; i < count; i++) {
    const r = spread * Math.cbrt(Math.random());
    const th = Math.random() * Math.PI * 2;
    const ph = Math.acos(2 * Math.random() - 1);
    pos[i*3] = r * Math.sin(ph) * Math.cos(th);
    pos[i*3+1] = r * Math.cos(ph);
    pos[i*3+2] = r * Math.sin(ph) * Math.sin(th);
    const c = colors[i % colors.length]; col[i*3]=c.r; col[i*3+1]=c.g; col[i*3+2]=c.b;
  }
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  return new THREE.Points(geo, new THREE.PointsMaterial({ size: 0.045, vertexColors: true, transparent: true, opacity: 0.86, blending: THREE.AdditiveBlending, depthWrite: false }));
}
const particles = makeParticles(1200, 1.18, [0x9dd6ff, 0xfff2a8, 0xc4b5fd]);
group.add(particles);

const lineage = new THREE.Group();
scene.add(lineage);
const lineageColors = [0x8b5cf6, 0xf59e0b, 0xf8fafc, 0xef4444, 0x67e8f9];
for (let i = 0; i < 60; i++) {
  const mat = glowMaterial(lineageColors[i % lineageColors.length], 0.45);
  const s = new THREE.Mesh(new THREE.SphereGeometry(0.12 + Math.random()*0.035, 24, 24), mat);
  const a = i * 0.55;
  const r = 1.6 + 0.045*i;
  s.position.set(Math.cos(a)*r, Math.sin(i*.27)*0.9, Math.sin(a)*r);
  lineage.add(s);
}
lineage.visible = false;

const body = new THREE.Group();
scene.add(body); body.visible = false;
function addEllipsoid(name, pos, scale, color, opacity) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(1, 48, 48), glowMaterial(color, opacity));
  m.name = name; m.position.set(...pos); m.scale.set(...scale); body.add(m); return m;
}
addEllipsoid('head', [0, 2.6, 0], [0.75, 0.9, 0.62], 0x9dd6ff, .22);
addEllipsoid('torso', [0, .65, 0], [1.05, 1.65, .58], 0xffffff, .13);
addEllipsoid('heart', [-.24, .95, .16], [.22,.25,.2], 0xf97316, .58);
addEllipsoid('lungsL', [-.45, 1.2, .05], [.33,.55,.18], 0xa5b4fc, .28);
addEllipsoid('lungsR', [.45, 1.2, .05], [.33,.55,.18], 0xa5b4fc, .28);
addEllipsoid('abdomen', [0, -.2, 0], [.72,.55,.25], 0xfef3c7, .24);
for (let side of [-1,1]) {
  addEllipsoid('arm', [side*1.15,.55,0], [.18,1.2,.18], 0xfca5a5, .18).rotation.z = side*.24;
  addEllipsoid('leg', [side*.42,-1.75,0], [.22,1.35,.2], 0xf8fafc, .18);
}
const network = new THREE.Group(); body.add(network);
for (let i=0;i<34;i++) {
  const pts=[new THREE.Vector3(0,1,0), new THREE.Vector3((Math.random()-.5)*2.4, Math.random()*4-1.8, (Math.random()-.5)*.7)];
  const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: i%2?0x60a5fa:0xf97316, transparent:true, opacity:.46 }));
  network.add(line);
}

function animate(t) {
  requestAnimationFrame(animate);
  const time = t * 0.001;
  const phase = (time / 42) % 1;
  const stageIndex = Math.min(7, Math.floor(phase * 8));
  stageText.textContent = `${stages[stageIndex][0]}｜${stages[stageIndex][1]}`;
  progressBar.style.width = `${phase * 100}%`;

  const grow = Math.min(1, Math.max(0, (phase - 0.10) / 0.20));
  membrane.scale.setScalar(1 + grow * 1.2 + Math.sin(time*2)*0.02);
  nucleus.scale.setScalar(1 + grow * 0.7);
  particles.rotation.y = time * 0.18;
  particles.rotation.x = Math.sin(time*.4)*0.2;
  helix.rotation.y = time * 0.5;
  group.rotation.y = time * 0.18;
  group.position.x = -phase * 4.8;

  lineage.visible = phase > 0.23;
  lineage.rotation.y = time * 0.22;
  lineage.scale.setScalar(Math.min(2.4, Math.max(.1, (phase - .23) * 5.4)));
  lineage.children.forEach((s, i) => { s.position.y += Math.sin(time*1.8+i)*0.002; s.scale.setScalar(1 + Math.sin(time*3+i)*0.12); });

  body.visible = phase > 0.50;
  const bs = Math.min(1.75, Math.max(.01, (phase - .50)*4.2));
  body.scale.setScalar(bs);
  body.rotation.y = time * 0.16;
  body.position.x = 2.2;
  body.children.forEach((m, i) => { if (m.isMesh) m.material.emissiveIntensity = 0.12 + 0.08*Math.sin(time*2+i); });

  camera.position.z = 13 - phase * 4;
  camera.position.y = 0.7 + Math.sin(time*.2)*0.3;
  camera.lookAt(0, .45, 0);
  renderer.render(scene, camera);
}
requestAnimationFrame(animate);
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
