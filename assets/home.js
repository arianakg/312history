const S = window.STORIES;
const dated = S.filter(s => typeof s.year === 'number').sort((a,b)=>a.year-b.year);

/* ---------- 1. HERO: Chicago grows ---------- */
(function(){
  const svg = document.getElementById('skyline'), NS='http://www.w3.org/2000/svg';
  const W=800,H=520, n=dated.length, slot=W/n;
  let r=7; const rnd=()=>{r=(r*9301+49297)%233280;return r/233280};
  const els=[]; let tallest=null;
  dated.forEach((s,i)=>{
    const t=(s.year-1803)/(2026-1803);
    const h=50+t*360+rnd()*70, w=slot*(0.7+rnd()*0.9), x=i*slot-(w-slot)/2;
    const g=document.createElementNS(NS,'g'); g.setAttribute('class','bld');
    const rc=document.createElementNS(NS,'rect');
    rc.setAttribute('x',x);rc.setAttribute('y',H-h);rc.setAttribute('width',w);rc.setAttribute('height',h);
    rc.setAttribute('fill',i%5===0?'#1d1d1d':'#fff');rc.setAttribute('stroke','#fff');rc.setAttribute('stroke-width','1.5');
    g.appendChild(rc);
    if(w>9){for(let yy=H-h+10;yy<H-8;yy+=14){const win=document.createElementNS(NS,'rect');win.setAttribute('x',x+w*0.3);win.setAttribute('y',yy);win.setAttribute('width',Math.max(2,w*0.4));win.setAttribute('height',5);win.setAttribute('fill',i%5===0?'#555':'#111');g.appendChild(win);}}
    const tt=document.createElementNS(NS,'title');tt.textContent=s.year+' · '+s.title;g.appendChild(tt);
    g.style.cursor='pointer';g.addEventListener('click',()=>location.href='stories/'+s.slug+'.html');
    g.style.transformOrigin=`${x+w/2}px ${H}px`;
    svg.appendChild(g); els.push({g,s,x,w,h});
    if(!tallest||h>tallest.h) tallest={x,w,h};
  });
  const ground=document.createElementNS(NS,'rect');ground.setAttribute('x',0);ground.setAttribute('y',H-2);ground.setAttribute('width',W);ground.setAttribute('height',2);ground.setAttribute('fill','#E4002B');svg.appendChild(ground);
  const star=document.createElementNS(NS,'text');star.textContent='★';star.setAttribute('x',tallest.x+tallest.w/2);star.setAttribute('y',H-tallest.h-12);star.setAttribute('text-anchor','middle');star.setAttribute('font-size','34');star.setAttribute('fill','#E4002B');svg.appendChild(star);
  const yEl=document.getElementById('growYear');
  if(!window.gsap){return;}
  const D=6.5;
  gsap.set(els.map(e=>e.g),{scaleY:0}); gsap.set(star,{scale:0,transformOrigin:'center'});
  const tl=gsap.timeline({delay:.4});
  const o={y:1803}; tl.to(o,{y:2026,duration:D,ease:'power1.inOut',onUpdate:()=>yEl.textContent=Math.round(o.y)},0);
  // map ease: compute time for a given year by inverting approx power1.inOut via sampling
  const ease=gsap.parseEase('power1.inOut');
  const timeFor=yr=>{const p=(yr-1803)/223;let lo=0,hi=1;for(let k=0;k<20;k++){const m=(lo+hi)/2;ease(m)<p?lo=m:hi=m;}return lo*D;};
  els.forEach(e=>tl.to(e.g,{scaleY:1,duration:.6,ease:'back.out(1.6)'},timeFor(e.s.year)+.4));
  tl.to(star,{scale:1,rotation:360,duration:.8,ease:'back.out(2)'},D+.3);
  gsap.from('.mega .line',{yPercent:100,opacity:0,stagger:.12,duration:.9,ease:'power3.out'});
})();

/* ---------- 2. MAP: old maps over today ---------- */
const map=L.map('leaf',{scrollWheelZoom:false,zoomControl:true}).setView([41.885,-87.635],13);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,maxNativeZoom:16,attribution:'Basemap © Esri, HERE, Garmin, © OpenStreetMap contributors'}).addTo(map);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,maxNativeZoom:16,pane:'shadowPane'}).addTo(map);
const LAYERS={
 today:{label:'Today',year:2026,note:'<b>TODAY</b> · Modern map. Red stars = stories from the posts (pins are approximate).'},
 y1871:{label:'1871 · Burnt District',year:1871,center:[41.875,-87.64],zoom:13,
   layer:L.imageOverlay('img/map_watson_1874.jpg',[[41.815,-87.690],[41.930,-87.595]],{opacity:.7}), // DRAFT ALIGNMENT: corner bounds estimated by hand, map not rotated/warped
   note:'<b>1871 · BURNT DISTRICT</b> · Gaylord Watson map (1874), burnt area in red. Public domain, via Wikimedia Commons / David Rumsey. <u>Draft alignment</u>: placed by hand, streets will not line up exactly.'},
 y1895:{label:'1895 · Sanborn (Hyde Park)',year:1895,center:[41.795,-87.597],zoom:14,
   layer:L.tileLayer('https://ogy8wt89v1.execute-api.us-west-2.amazonaws.com//cog/tiles/WebMercatorQuad/{z}/{x}/{y}@2x.png?url=https%3A%2F%2Fs3.us-central-1.wasabisys.com%2Foldinsurancemaps%2Fuploaded%2Flayers%2Fchicago_ill_1895_vol_16_p0__WAIAbn_01.tif',
     {opacity:.7,tileSize:256,maxZoom:19,bounds:[[41.761,-87.633],[41.833,-87.563]],attribution:'Sanborn 1895 Vol. 16 key map, Library of Congress (public domain), georeferenced by OldInsuranceMaps.net'}),
   note:'<b>1895 · SANBORN FIRE-INSURANCE MAP</b> · Hyde Park / Woodlawn key sheet, truly georeferenced (OldInsuranceMaps.net, scan: Library of Congress, public domain). Near the 1893 fair and the Midway.'}
};
let active=null;
const yrs=document.getElementById('years'), note=document.getElementById('mapNote'), op=document.getElementById('opacity'), opv=document.getElementById('opv');
Object.entries(LAYERS).forEach(([k,v])=>{const b=document.createElement('button');b.textContent=v.label;b.dataset.k=k;b.onclick=()=>setLayer(k);yrs.appendChild(b);});
const markers=[];
S.forEach(s=>{
  const icon=L.divIcon({className:'',html:'<div class="star-pin">★</div>',iconSize:[26,26],iconAnchor:[13,13]});
  if(s.lat==null) return; const m=L.marker([s.lat,s.lng],{icon,title:s.title}).addTo(map); // approximate coordinates
  m.bindPopup(`<div class="pop"><img src="media/post${s.num}.jpg" alt=""><span class="kicker red">${s.topicName} · ${s.year||'—'}</span><h4>${s.title}</h4><p>${s.place}</p><a href="stories/${s.slug}.html">Read the story →</a></div>`);
  markers.push({m,s});
});
function setLayer(k){
  Object.values(LAYERS).forEach(v=>v.layer&&map.hasLayer(v.layer)&&map.removeLayer(v.layer));
  const v=LAYERS[k]; active=v;
  if(v.layer){v.layer.setOpacity(op.value/100);v.layer.addTo(map);map.flyTo(v.center,v.zoom,{duration:1});}
  note.innerHTML=v.note;
  [...yrs.children].forEach(b=>b.classList.toggle('on',b.dataset.k===k));
  markers.forEach(({m,s})=>{const el=m.getElement()&&m.getElement().firstChild;if(el)el.classList.toggle('dim',k!=='today'&&typeof s.year==='number'&&s.year>v.year);});
}
op.oninput=()=>{opv.textContent=op.value+'%';if(active&&active.layer)active.layer.setOpacity(op.value/100);};
setLayer('y1871');

/* walks -> map */
let walkLine=null;
document.querySelectorAll('[data-walk]').forEach(b=>b.addEventListener('click',()=>{
  const nums=b.dataset.walk.split(','); setLayer('today');
  const pts=nums.map(n=>S.find(s=>s.num===n)).map(s=>[s.lat,s.lng]);
  if(walkLine)map.removeLayer(walkLine);
  walkLine=L.polyline(pts,{color:'#E4002B',weight:4,dashArray:'8 8'}).addTo(map);
  markers.forEach(({m,s})=>{const el=m.getElement().firstChild;el.classList.toggle('hl',nums.includes(s.num));el.classList.toggle('dim',!nums.includes(s.num));});
  document.getElementById('map').scrollIntoView({behavior:'smooth'});
  setTimeout(()=>map.fitBounds(walkLine.getBounds(),{padding:[60,60]}),600);
}));

/* ---------- 3. TIMELINE (Histography-style) ---------- */
(function(){
  const tl=document.getElementById('tl'), card=document.getElementById('tlCard');
  const Y0=1795,Y1=2032, X=y=>((y-Y0)/(Y1-Y0))*100;
  [['Frontier town',1803,0],['Great Fire',1871,0],['World\'s Fair',1893,1],['Modern Chicago',1945,0]].forEach(([t,y,o])=>{const e=document.createElement('div');e.className='era';e.style.left=X(y)+'%';e.innerHTML='<span style="top:'+(o?18:0)+'px">'+t+'</span>';tl.appendChild(e);});
  for(let y=1800;y<=2025;y+=25){const t=document.createElement('div');t.className='tick';t.style.left=X(y)+'%';t.textContent=y;tl.appendChild(t);}
  const stack={};
  dated.forEach(s=>{
    const b=Math.round(X(s.year)/1.6); stack[b]=(stack[b]||0)+1;
    const d=document.createElement('a');d.className='dot';d.href='stories/'+s.slug+'.html';d.textContent='★';
    d.style.left=X(s.year)+'%';d.style.bottom=(stack[b]*22-6)+'px';d.title=s.year+' · '+s.title;
    const show=()=>{tl.querySelectorAll('.dot.on').forEach(x=>x.classList.remove('on'));d.classList.add('on');
      card.innerHTML=`<img src="media/post${s.num}.jpg" alt=""><div><div class="y">${s.year}</div><h3>${s.title}</h3><p>${s.hook}</p><a href="stories/${s.slug}.html">Read the story →</a></div>`;};
    d.addEventListener('mouseenter',show);d.addEventListener('focus',show);
    d.addEventListener('click',e=>{if(matchMedia('(hover:none)').matches&&!d.classList.contains('on')){e.preventDefault();show();}});
    tl.appendChild(d);
  });
  const first=tl.querySelector('.dot'); first&&first.dispatchEvent(new Event('mouseenter'));
  if(window.gsap){
    // play an animation once when the element scrolls into view (IntersectionObserver = robust to late layout changes)
    const once=(el,fn)=>{const o=new IntersectionObserver(es=>{if(es[0].isIntersecting){fn();o.disconnect();}},{threshold:.1});o.observe(el);};
    const dots=[...tl.querySelectorAll('.dot')]; gsap.set(dots,{y:-200,opacity:0});
    once(tl,()=>gsap.to(dots,{y:0,opacity:1,stagger:.01,duration:.6,ease:'bounce.out',clearProps:'transform'}));
    document.querySelectorAll('.sec-title').forEach(t=>{gsap.set(t,{y:60,opacity:0});once(t,()=>gsap.to(t,{y:0,opacity:1,duration:.9,ease:'power3.out'}));});
  }
})();

/* ---------- 4. TOPIC FILTERS ---------- */
document.querySelectorAll('.chip').forEach(c=>c.addEventListener('click',()=>{
  document.querySelectorAll('.chip').forEach(x=>x.classList.toggle('on',x===c));
  const f=c.dataset.f; document.querySelectorAll('#grid .card').forEach(k=>k.classList.toggle('hide',f!=='ALL'&&k.dataset.topic!==f));
}));
