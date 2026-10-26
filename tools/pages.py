"""Extra pages for the features branch: About, Press & Awards, Walking routes."""
import json, math
from __main__ import head, foot, esc, TOPICS, WALKS, IG

def about_page(S):
    return head("About | 312 History", 0) + f"""
<main class="page"><section class="page-hero"><span class="kicker red" data-i18n="about.kicker">About the project</span>
<h1 class="mega small"><span class="line" data-i18n="about.h1">CHICAGO HISTORY</span><span class="line" data-i18n="about.h2">THROUGH AN</span><span class="line" data-i18n="about.h3">IMMIGRANT'S EYES<b>★</b></span></h1></section>
<section class="mission-band"><span class="kicker" data-i18n="about.mission">MISSION</span><p class="mission-quote" data-i18n="about.missiontext">To tell the history of Chicago through an immigrant's eyes, so that everyone who comes here can feel that this city is their own.</p></section>
<section class="about-grid"><figure class="portrait"><img src="img/ariana-portrait.jpg" alt="Ariana Cholponkadyrova, creator of 312 History" width="720" height="1280"></figure>
<div class="about-text"><h2 class="sec-title small" data-i18n="about.who">HI, I'M ARIANA</h2><p data-i18n="about.p1">I'm Ariana Cholponkadyrova, the creator of 312 History. I came to Chicago from Kyrgyzstan, and exploring the history of my new city became my way of making it home.</p><p data-i18n="about.p2">Back home I worked at a public foundation that ran several large projects: in agriculture, in promoting the green economy (we built greenhouses and ran training courses) and in vocational and technical education. I was the coordinator and organizer of Karagat Fest, the annual berry and fruit festival of the Issyk-Kul region, and handled PR for many of the projects. That work taught me how to bring people together around a good story.</p><p data-i18n="about.p3">In Chicago I'm a content creator and a mom of two: my daughter is 5 and my son is 9. I run a small business printing designs on T-shirts and tote bags, a craft I truly love. I love photography and making beautiful videos, and right now I'm studying AI neuro-content and AI agents.</p>
<h2 class="sec-title small" data-i18n="about.vision">VISION</h2><p data-i18n="about.visiontext">312 History becomes the leading bilingual guide to Chicago's history: videos, the map at 312history.com, tours and a book that connect the city's past with the people who live here today.</p><p data-i18n="about.how">Today that means short videos on Instagram and an interactive map where every story is a point you can visit.</p>
<div class="cta"><a class="btn btn-red" href="{IG}" target="_blank" rel="noopener" data-i18n="btn.ig">Instagram @312history</a><a class="btn btn-line" href="index.html#map" data-i18n="about.map">Explore the map</a></div></div></section>
<section class="about-cols"><div><h2 class="sec-title small" data-i18n="about.values">VALUES</h2><ul class="about-list"><li data-i18n="about.v1"><b>Truth.</b> Only checked facts, with a source in every post.</li><li data-i18n="about.v2"><b>People.</b> History told through human lives, not dry dates.</li><li data-i18n="about.v3"><b>Openness.</b> Chicago for everyone who came here, in Russian and English.</li><li data-i18n="about.v4"><b>Curiosity.</b> We look for secrets and forgotten stories close to home.</li><li data-i18n="about.v5"><b>Respect.</b> We speak with care about tragedies and different cultures.</li></ul></div>
<div><h2 class="sec-title small" data-i18n="about.angle">WHAT MAKES US DIFFERENT</h2><ol class="angle-list"><li data-i18n="about.a1">The view of an immigrant from Kyrgyzstan: fresh and personal.</li><li data-i18n="about.a2">Two languages, Russian and English, for an audience almost no one serves.</li><li data-i18n="about.a3">An interactive map on the site: every story is a point on the map.</li><li data-i18n="about.a4">Experience in PR and events: we know how to create events, partnerships and press.</li></ol></div></section></main>""" + foot(0)

def press_page(S):
    def block(key, title, ph):
        return f'''<section class="press-block"><h2 class="sec-title small" data-i18n="press.{key}">{title}</h2>
<ul class="press-list"><li class="ph"><span class="kicker">Placeholder</span><p data-i18n="press.ph">{ph}</p></li></ul></section>'''
    return head("Press & Awards — 312 History", 0) + f"""
<main class="page"><section class="page-hero"><span class="kicker red" data-i18n="press.kicker">Press & Awards</span>
<h1 class="mega small"><span class="line" data-i18n="press.h1">IN THE</span><span class="line" data-i18n="press.h2">NEWS<b>★</b></span></h1>
<p class="lead dark" data-i18n="press.lead">Articles, interviews and awards about 312 History will be listed here.</p></section>
<div class="press-wrap">
{block("media","PRESS COVERAGE","No coverage yet. Format: outlet, headline, date, link.")}
{block("awards","AWARDS & RECOGNITION","No awards yet. Format: award, organization, year.")}
{block("talks","TALKS & EVENTS","No events yet. Format: event, venue, date.")}
<section class="press-block"><h2 class="sec-title small" data-i18n="press.kit">PRESS KIT & CONTACT</h2><p data-i18n="press.kittext">Journalists: write to us for photos, logos and interviews.</p>
<a class="btn btn-line" href="mailto:hello@312history.com" data-i18n="press.contact">Contact (placeholder email)</a></section>
</div></main>""" + foot(0)

def order(stops):
    """Nearest-neighbour walk starting from the northernmost stop."""
    rest=stops[:]; cur=max(rest,key=lambda s:s["lat"]); out=[cur]; rest.remove(cur)
    while rest:
        cur=min(rest,key=lambda s:math.hypot(s["lat"]-cur["lat"],(s["lng"]-cur["lng"])*0.75)); out.append(cur); rest.remove(cur)
    return out

def routes_page(S):
    by={s["num"]:s for s in S}; routes=[]; html=""
    for wi,(n,d,nums) in enumerate(WALKS):
        st=order([by[k] for k in nums if k in by and by[k]["lat"] is not None])
        km=sum(math.hypot((a["lat"]-b["lat"])*111,(a["lng"]-b["lng"])*83) for a,b in zip(st,st[1:]))
        routes.append(dict(name=n,stops=[dict(num=s["num"],title=s["title"],lat=s["lat"],lng=s["lng"],slug=s["slug"]) for s in st]))
        li="".join(f'<li><a href="stories/{s["slug"]}.html"><img src="media/post{s["num"]}.jpg" alt=""><span><b>{esc(s["title"])}</b><em>{esc(s["place"])}</em></span></a></li>' for s in st)
        html+=f'''<div class="walk"><span class="walk-n">0{wi+1}</span><h3>{esc(n).upper()}</h3><p>{esc(d)}</p>
<p class="kicker">{len(st)} <span data-i18n="r.stops">stops</span> · ≈{km:.1f} km <span data-i18n="r.straight">straight-line</span></p><ol>{li}</ol>
<button class="btn btn-red" data-route="{wi}" data-i18n="r.show">Show on map ★</button></div>'''
    return head("Walking routes — 312 History",0,'<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n') + f"""
<main class="page"><section class="page-hero"><span class="kicker red" data-i18n="r.kicker">Walk it</span>
<h1 class="mega small"><span class="line" data-i18n="r.h1">WALKING</span><span class="line" data-i18n="r.h2">ROUTES<b>★</b></span></h1>
<p class="lead dark" data-i18n="r.lead">Routes built only from published stories with map pins, ordered stop by stop. Times are rough guides; pins are approximate.</p></section>
<section class="routes"><div class="routes-map"><div id="rmap"></div></div><div class="walk-col">{html}</div></section></main>
<script>window.ROUTES={json.dumps(routes)};</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script src="assets/routes.js"></script>""" + foot(0)
