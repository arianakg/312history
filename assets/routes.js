(function(){const map=L.map('rmap',{scrollWheelZoom:false}).setView([41.88,-87.627],14);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,maxNativeZoom:16,attribution:'Basemap © Esri, HERE, Garmin, © OpenStreetMap contributors'}).addTo(map);L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}',{maxZoom:19,maxNativeZoom:16,pane:'shadowPane'}).addTo(map);
let grp=null;function show(i){const r=ROUTES[i];if(grp)map.removeLayer(grp);grp=L.featureGroup();
const pts=r.stops.map(s=>[s.lat,s.lng]);L.polyline(pts,{color:'#E4002B',weight:4,dashArray:'8 8'}).addTo(grp);
r.stops.forEach((s,k)=>L.marker([s.lat,s.lng],{icon:L.divIcon({className:'rpin',html:`<span>${k+1}</span>`,iconSize:[28,28]})}).bindPopup(`<b>${k+1}. ${s.title}</b><br><a href="stories/${s.slug}.html">Read →</a>`).addTo(grp));
grp.addTo(map);map.fitBounds(grp.getBounds(),{padding:[40,40]});
document.querySelectorAll('[data-route]').forEach(b=>b.classList.toggle('btn-line',+b.dataset.route!==i));}
document.querySelectorAll('[data-route]').forEach(b=>b.addEventListener('click',()=>{show(+b.dataset.route);if(innerWidth<900)document.getElementById('rmap').scrollIntoView({behavior:'smooth'});}));
show(0);})();
