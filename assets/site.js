// reveal-on-scroll for any .reveal element
const ro=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}}),{threshold:.15});
document.querySelectorAll('.reveal').forEach(el=>ro.observe(el));
