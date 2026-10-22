(() => { const RG = {x0:-1.15,x1:2.32,z0:-8.75,z1:-4.68};
 const inR = (x,z) => x>=RG.x0 && x<=RG.x1 && z>=RG.z0 && z<=RG.z1;
 player.obj.visible = false; scene.updateMatrixWorld(true);
 const q = (a, d=1000) => Array.from(a, x => Math.round(x*d)/d);
 const texs = {}, mats = {}, meshes = [], sprites = [], lights = [];
 const tex = t => { if(!t) return null; if(!texs[t.uuid]) { const im = t.image; let url=null, w=0, h=0;
     try { let c = im; if (!(im instanceof HTMLCanvasElement)) { c = document.createElement('canvas'); c.width = im.width; c.height = im.height; c.getContext('2d').drawImage(im,0,0); }
       w=c.width; h=c.height; url = c.toDataURL('image/png'); } catch(e) { url = 'ERR '+e; }
     texs[t.uuid] = { url, w, h, wrapS:t.wrapS, wrapT:t.wrapT, repeat:t.repeat.toArray(), offset:t.offset.toArray(), rotation:t.rotation, center:t.center.toArray(), mag:t.magFilter, min:t.minFilter, enc:t.encoding, flipY:t.flipY, aniso:t.anisotropy, gen: t.generateMipmaps }; }
   return t.uuid; };
 const mat = m => { if(!mats[m.uuid]) { const o = { type:m.type, transparent:m.transparent, opacity:m.opacity, side:m.side, depthWrite:m.depthWrite, depthTest:m.depthTest, vertexColors:m.vertexColors, toneMapped:m.toneMapped, blending:m.blending, polygonOffset:m.polygonOffset, pof:m.polygonOffsetFactor, pou:m.polygonOffsetUnits, alphaTest:m.alphaTest, fog:m.fog, colorWrite:m.colorWrite };
     if (m.color) o.color = m.color.getHex(); if (m.emissive) { o.emissive = m.emissive.getHex(); o.emissiveIntensity = m.emissiveIntensity; }
     if (m.roughness !== undefined) { o.roughness = m.roughness; o.metalness = m.metalness; o.flatShading = m.flatShading; o.envMapIntensity = m.envMapIntensity; }
     if (m.map) o.map = tex(m.map); if (m.emissiveMap) o.emissiveMap = tex(m.emissiveMap); if (m.alphaMap) o.alphaMap = tex(m.alphaMap); if (m.roughnessMap) o.roughnessMap = tex(m.roughnessMap); if (m.normalMap) o.normalMap = tex(m.normalMap); if (m.bumpMap) o.bumpMap = tex(m.bumpMap);
     if (m.sizeAttenuation !== undefined) o.sizeAttenuation = m.sizeAttenuation; if (m.rotation !== undefined) o.rotation = m.rotation;
     o.obc = !!m.onBeforeCompile && m.onBeforeCompile.toString().length > 40; o.name = m.name;
     mats[m.uuid] = o; } return m.uuid; };
 const v = new THREE.Vector3(), n = new THREE.Vector3(), nm = new THREE.Matrix3(), M = new THREE.Matrix4(), IM = new THREE.Matrix4();
 let skipped = [];
 scene.traverse(o => {
   if (o.isLight) { const w = new THREE.Vector3(); o.getWorldPosition(w);
     if (o.isPointLight || o.isSpotLight) { if (!inR(w.x, w.z) && !(o.isPointLight && o.distance===0)) return; }
     const L = { type:o.type, color:o.color.getHex(), intensity:o.intensity, pos:w.toArray(), castShadow:o.castShadow, visible:o.visible };
     if (o.groundColor) L.ground = o.groundColor.getHex(); if (o.distance !== undefined) { L.distance=o.distance; L.decay=o.decay; }
     if (o.target) { const t=new THREE.Vector3(); o.target.getWorldPosition(t); L.target=t.toArray(); }
     if (o.shadow && o.castShadow) { const c=o.shadow.camera; L.shadow = { size:o.shadow.mapSize.toArray(), bias:o.shadow.bias, normalBias:o.shadow.normalBias, radius:o.shadow.radius, cam:[c.left,c.right,c.top,c.bottom,c.near,c.far] }; }
     lights.push(L); return; }
   let vis = true; for (let p=o;p;p=p.parent) if(!p.visible) vis=false; if(!vis) return;
   if (o.isSprite) { const w=new THREE.Vector3(); o.getWorldPosition(w); if(!inR(w.x,w.z)) return; const s=new THREE.Vector3(); o.getWorldScale(s);
     sprites.push({ pos:w.toArray(), scale:s.toArray(), mat:mat(o.material), ro:o.renderOrder }); return; }
   if (!o.isMesh) { if (o.isLine||o.isPoints) skipped.push(o.type); return; }
   const g = o.geometry; const P = g.attributes.position; if (!P) return;
   const ms = Array.isArray(o.material) ? o.material : [o.material];
   const groups = ms.length > 1 && g.groups.length ? g.groups : [{ start: 0, count: Infinity, materialIndex: 0 }];
   const N = g.attributes.normal, C = g.attributes.color, U = g.attributes.uv, idx = g.index;
   const insts = o.isInstancedMesh ? o.count : 1;
   for (const gr of groups) { const gm = ms[gr.materialIndex] || ms[0]; if (!gm.visible && gm.visible !== undefined) continue;
   const outP=[], outN=[], outC=[], outU=[];
   const t0 = Math.floor(gr.start/3), t1 = Math.min((idx ? idx.count : P.count)/3, gr.count === Infinity ? Infinity : Math.floor((gr.start+gr.count)/3));
   for (let k=0;k<insts;k++) {
     if (o.isInstancedMesh) { o.getMatrixAt(k, IM); M.multiplyMatrices(o.matrixWorld, IM); } else M.copy(o.matrixWorld);
     nm.getNormalMatrix(M);
     const tri = idx ? idx.count/3 : P.count/3;
     for (let t=t0;t<Math.min(tri,t1);t++) { const ii=[0,1,2].map(e => idx ? idx.getX(t*3+e) : t*3+e);
       let cx=0, cz=0; const ws = ii.map(i => { v.fromBufferAttribute(P,i).applyMatrix4(M); cx+=v.x; cz+=v.z; return v.toArray(); });
       if (!inR(cx/3, cz/3)) continue;
       ws.forEach((w,e)=>{ outP.push(...w); const i=ii[e];
         if (N) { n.fromBufferAttribute(N,i).applyMatrix3(nm).normalize(); outN.push(n.x,n.y,n.z); }
         if (C) outC.push(C.getX(i), C.getY(i), C.getZ(i)); if (U) outU.push(U.getX(i), U.getY(i)); });
     }
   }
   if (!outP.length) continue;
   meshes.push({ mat: mat(gm), p:outP, n: outN.length? outN:null, c: outC.length? outC:null, u: outU.length? outU:null, cast:o.castShadow, recv:o.receiveShadow, ro:o.renderOrder, inst:o.isInstancedMesh?o.count:0, src: o.uuid });
   }
 });
 // crop big clamped textures to the part this room uses, and remap its uvs
 for (const [id, T] of Object.entries(texs)) { if (T.w * T.h < 300000) continue;
   const users = meshes.filter(m => mats[m.mat].map === id && m.u); if (!users.length) continue;
   let u0=1,u1=0,v0=1,v1=0; for (const m of users) for (let i=0;i<m.u.length;i+=2) { u0=Math.min(u0,m.u[i]); u1=Math.max(u1,m.u[i]); v0=Math.min(v0,m.u[i+1]); v1=Math.max(v1,m.u[i+1]); }
   const px0 = Math.max(0, Math.floor(u0*T.w)-2), px1 = Math.min(T.w, Math.ceil(u1*T.w)+2);
   const py0 = Math.max(0, Math.floor((T.flipY ? 1-v1 : v0)*T.h)-2), py1 = Math.min(T.h, Math.ceil((T.flipY ? 1-v0 : v1)*T.h)+2);
   const img = new Image(); T.crop = [px0,py0,px1,py1,u0,u1,v0,v1];
   const src = document.createElement('canvas'); src.width=T.w; src.height=T.h;
   const tt = Object.values(scene.children).length; // noop
   const orig = (() => { let f=null; scene.traverse(o => { if (f||!o.material) return; for (const mm of [].concat(o.material)) for (const k of ['map']) if (mm[k] && mm[k].uuid===id) f = mm[k]; }); return f; })();
   src.getContext('2d').drawImage(orig.image, 0, 0);
   const c = document.createElement('canvas'); c.width = px1-px0; c.height = py1-py0; c.getContext('2d').drawImage(src, px0, py0, c.width, c.height, 0, 0, c.width, c.height);
   T.url = c.toDataURL('image/png');
   for (const m of users) for (let i=0;i<m.u.length;i+=2) { m.u[i] = (m.u[i]*T.w - px0)/(px1-px0); const py = T.flipY ? (1-m.u[i+1])*T.h : m.u[i+1]*T.h; m.u[i+1] = T.flipY ? 1-(py-py0)/(py1-py0) : (py-py0)/(py1-py0); }
   T.w = c.width; T.h = c.height; }
 const b64 = a => { const b = new Uint8Array(a.buffer); let s=''; for (let i=0;i<b.length;i+=0x8000) s += String.fromCharCode.apply(null, b.subarray(i,i+0x8000)); return btoa(s); };
 for (const m of meshes) { m.p = b64(new Float32Array(m.p)); if (m.n) m.n = b64(new Int8Array(m.n.map(x => Math.round(x*127)))); if (m.c) m.c = b64(new Uint16Array(m.c.map(x => Math.round(Math.min(1,Math.max(0,x))*65535)))); if (m.u) m.u = b64(new Float32Array(m.u)); }
 const r = renderer;
 return JSON.stringify({ region:RG, meshes, sprites, mats, texs, lights, skipped,
   renderer: { tm:r.toneMapping, exp:r.toneMappingExposure, enc:r.outputEncoding, pcl:r.physicallyCorrectLights, shadowType:r.shadowMap.type, shadows:r.shadowMap.enabled },
   bg: scene.background && scene.background.getHex ? scene.background.getHex() : null,
   cam: { az, el:.62, target:target.toArray(), zoom:camera.zoom, near:camera.near, far:camera.far },
   game: { calls: renderer.info.render.calls, tris: renderer.info.render.triangles } });
})()
