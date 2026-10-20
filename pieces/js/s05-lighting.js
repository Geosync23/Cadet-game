// =====================================================================
// 5. LIGHTING
// The sun casts all shadows and follows the camera, snapped to shadow
// texels so edges don't shimmer. Lamps come up at night.
// =====================================================================
const hemi = new THREE.HemisphereLight(0xffffff, 0x000000, 1); scene.add(hemi);
const sun = new THREE.DirectionalLight(0xffffff, 1);
const SUN_OFF = new THREE.Vector3(-2.5, 9, 5.5);
sun.castShadow = true; scene.add(sun); scene.add(sun.target);
sun.shadow.mapSize.set(2048, 2048);
Object.assign(sun.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10, near: 1, far: 30 });
sun.shadow.bias = -.0004; sun.shadow.normalBias = .03;
const sunDir = SUN_OFF.clone().normalize();
const sunR = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), sunDir).normalize();
const sunU = new THREE.Vector3().crossVectors(sunDir, sunR);
let SHADOW_K = 1;
function placeSun(p) {
  // 0.27.18: zoomed out, the shadowed square grows with the view (k), so shadows never stop short on screen; the
  // texels per screen pixel stay about the same. At the usual zooms k is 1 and nothing changes.
  const hd = Math.hypot((camera.right - camera.left) / 2, (camera.top - camera.bottom) / 2 / Math.sin(.62)) / camera.zoom, k = Math.max(1, hd / 9.5);
  if (k !== SHADOW_K) {
    SHADOW_K = k; Object.assign(sun.shadow.camera, { left: -10 * k, right: 10 * k, top: 10 * k, bottom: -10 * k, far: 30 * k });
    sun.shadow.camera.updateProjectionMatrix(); sun.shadow.normalBias = .03 * k;
  }
  const ts = 20 * k / sun.shadow.mapSize.x, v = new THREE.Vector3(p.x, 0, p.z), a = v.dot(sunR), b = v.dot(sunU);
  v.addScaledVector(sunR, Math.round(a / ts) * ts - a).addScaledVector(sunU, Math.round(b / ts) * ts - b);
  sun.target.position.copy(v); sun.position.copy(v).addScaledVector(SUN_OFF, k);
}

const DAY = { sky: col('#e3ebf1'), gnd: col('#5b4d41'), hemi: .85, sun: col('#fff2e0'), sunI: 1.6, exp: 1.05, bg: new THREE.Color('#151d2c') };
const NIGHT = { sky: col('#7886ad'), gnd: col('#30241c'), hemi: .42, sun: col('#ffb371'), sunI: .62, exp: 1.03, bg: new THREE.Color('#0a0e17') };   // 0.47.5 (playtest: "a little brighter"): hemi .32, sunI .5, exp 1.0, sky #6d7ca3, ground #2a1f18 before; the dimming still starts at 20:30 (nightAt)
let nightT = 0;                                          // 0 day ... 1 night; follows the clock (section 13)
function applyLight(k) {
  const lerp = THREE.MathUtils.lerp;
  hemi.color.copy(DAY.sky).lerp(NIGHT.sky, k); hemi.groundColor.copy(DAY.gnd).lerp(NIGHT.gnd, k);
  hemi.intensity = lerp(DAY.hemi, NIGHT.hemi, k);
  sun.color.copy(DAY.sun).lerp(NIGHT.sun, k); sun.intensity = lerp(DAY.sunI, NIGHT.sunI, k);
  const ml = deckDef && deckDef.light;                   // a deck's own mood (Deck 6 runs warm and dim)
  if (ml) { hemi.color.multiply(ml.sky); hemi.intensity *= ml.hemi; sun.color.multiply(ml.sun); sun.intensity *= ml.sunI; }
  if (REC_SHOW.dim) { const q = 1 - REC_SHOW.dim; hemi.intensity *= q; sun.intensity *= q; }   // 0.84.8: the auditorium's house lights down for a show (8c)
  for (const L of LAMPS) L.l.intensity = lerp(L.day, L.night, k);
  renderer.toneMappingExposure = lerp(DAY.exp, NIGHT.exp, k);
  scene.background.copy(DAY.bg).lerp(NIGHT.bg, k);
  SKY.mat.uniforms.uK.value = lerp(.8, 1.15, k);
}

