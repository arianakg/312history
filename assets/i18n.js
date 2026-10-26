/* EN/RU switch. UI strings + About are translated; story texts stay in English (no Russian versions yet). */
const RU={
"nav.map":"Карта","nav.stories":"Истории","nav.routes":"Маршруты","nav.fire":"Пожар 1871","nav.about":"О проекте","nav.press":"Пресса",
"signup.kicker":"Рассылка","signup.title":"НОВЫЕ ИСТОРИИ НА ПОЧТУ","signup.text":"Одно короткое письмо, когда выходят новые истории о Чикаго. Без спама.","signup.btn":"Подписаться",
"signup.note":"Временно: подписка открывает почтовое приложение, пока не подключён сервис рассылки.",
"btn.ig":"Instagram @312history","btn.support":"Поддержать проект ★",
"f.search":"Поиск по историям, местам, годам…","f.allareas":"Все районы","f.alleras":"Все эпохи","f.empty":"Ничего не найдено. Попробуйте другой фильтр.",
"ru.storynote":"Тексты историй пока только на английском. Русские версии появятся позже.",
"about.kicker":"О проекте","about.h1":"ИСТОРИЯ ЧИКАГО","about.h2":"ГЛАЗАМИ","about.h3":"ИММИГРАНТКИ<b>★</b>","about.photo":"Здесь будет фото Арианы",
"about.who":"КТО СТОИТ ЗА 312 HISTORY","about.p1":"Привет! Я Ариана Чолпонкадырова, автор 312 History. Я иммигрантка из Кыргызстана, и теперь мой дом — Чикаго.",
"about.p2":"В Кыргызстане я занималась организацией мероприятий и работала в крупном PR-агентстве. В Чикаго я начала всё заново, и изучение прошлого нового города стало моим способом почувствовать себя здесь дома.",
"about.mission":"МИССИЯ","about.p3":"Чикаго построили иммигранты. 312 History рассказывает истории города глазами иммигрантки — в коротких видео и на интерактивной карте, чтобы каждый мог узнать, что происходило прямо на его улице.",
"about.l1":"Короткие видео в Instagram","about.l2":"Интерактивная карта всех историй","about.l3":"Каждый факт проверен по источникам","about.map":"Открыть карту",
"press.kicker":"Пресса и награды","press.h1":"О НАС","press.h2":"ПИШУТ<b>★</b>","press.lead":"Здесь будут статьи, интервью и награды 312 History.",
"press.media":"ПУБЛИКАЦИИ","press.awards":"НАГРАДЫ","press.talks":"ВЫСТУПЛЕНИЯ И СОБЫТИЯ","press.ph":"Пока пусто.","press.kit":"ДЛЯ ПРЕССЫ","press.kittext":"Журналистам: напишите нам за фото, логотипами и интервью.","press.contact":"Связаться (временный email)",
"r.kicker":"Пешком","r.h1":"ПЕШЕХОДНЫЕ","r.h2":"МАРШРУТЫ<b>★</b>","r.lead":"Маршруты только из опубликованных историй с точкой на карте, по порядку. Время примерное, точки на карте приблизительные. Тексты историй на английском.",
"r.stops":"остановок","r.straight":"по прямой","r.show":"Показать на карте ★"};
(function(){const els=[...document.querySelectorAll('[data-i18n]')],phs=[...document.querySelectorAll('[data-i18n-ph]')];
els.forEach(e=>e.dataset.en=e.innerHTML);phs.forEach(e=>e.dataset.en=e.placeholder);
function set(l){document.documentElement.lang=l;els.forEach(e=>{const k=e.dataset.i18n;e.innerHTML=l==='ru'&&RU[k]?RU[k]:e.dataset.en;});
phs.forEach(e=>{e.placeholder=l==='ru'?RU[e.dataset.i18nPh]:e.dataset.en});
document.querySelectorAll('[data-lang]').forEach(b=>b.classList.toggle('on',b.dataset.lang===l));try{localStorage.lang=l}catch(_){}}
document.querySelectorAll('[data-lang]').forEach(b=>b.addEventListener('click',()=>set(b.dataset.lang)));
let l='en';try{l=localStorage.lang||'en'}catch(_){}set(l);})();
