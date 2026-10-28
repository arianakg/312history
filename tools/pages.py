"""Extra pages for the features branch: About, Press & Awards, Walking routes."""
import json, math
from __main__ import head, foot, esc, TOPICS, WALKS, IG

def about_page(S):
    return head("About | 312 History", 0, desc="Meet Ariana Cholponkadyrova, creator of 312 History: uncovering Chicago's history with the fresh eyes of someone who chose this city as home.", path="about.html") + f"""
<main class="page"><section class="page-hero"><span class="kicker red" data-i18n="about.kicker">About the project</span>
<h1 class="mega small"><span class="line" data-i18n="about.h1">CHICAGO HISTORY</span><span class="line" data-i18n="about.h2">WITH FRESH</span><span class="line" data-i18n="about.h3">EYES<b>★</b></span></h1></section>
<section class="mission-band"><span class="kicker" data-i18n="about.mission">MISSION</span><p class="mission-quote" data-i18n="about.missiontext">Uncovering Chicago's history with the fresh eyes of someone who chose this city as home.</p></section>
<section class="about-grid"><figure class="portrait"><img src="img/ariana-portrait.jpg" alt="Ariana Cholponkadyrova, creator of 312 History" width="720" height="1280"></figure>
<div class="about-text"><p data-i18n="about.s1">When I moved to Chicago, I didn't know its streets, its neighborhoods, or its past. But every building I passed seemed to hold a secret. Who lived here a hundred years ago? Who built this city?</p><p data-i18n="about.s2">I'm Ariana Cholponkadyrova. Back home in Kyrgyzstan, I worked as a PR manager at a public foundation that ran large projects in agriculture, the green economy and vocational and technical education, and I coordinated Karagat Fest, the annual berry and fruit festival of the Issyk-Kul region. I moved to Chicago four years ago and started over as a mom of two and a content creator. I love making beautiful photos and videos, I create AI content and study AI, and I'm still improving my English. Most of all, I love building brands from scratch. Exploring my new city became my way of making it home.</p><p data-i18n="about.s3">That's how 312history was born.</p><h2 class="sec-title small" data-i18n="about.h_what">WHAT IS 312HISTORY?</h2><p data-i18n="about.what">312history tells the story of Chicago through short videos and an interactive map. Every story is a point on the map, so you can discover what happened right on your block. Explore it at 312history.com and follow along on Instagram.</p><h2 class="sec-title small" data-i18n="about.h_why">WHY FRESH EYES?</h2><p data-i18n="about.why">Chicago was built by people who came from far away: Polish, German, Irish, Mexican, Ukrainian and many more. As someone who chose this city as home, I see their stories in a personal way. Their story is my story too.</p><h2 class="sec-title small" data-i18n="about.h_next">WHAT'S NEXT?</h2><p data-i18n="about.next">More neighborhoods, more forgotten heroes, and every story in both English and Russian. My dream is that one day anyone walking down a Chicago street can open the map and hear the voice of the past.</p><p data-i18n="about.join">If you love Chicago, or have ever built a new home far from where you started, join me. Let's discover this city together.</p>
<div class="cta"><a class="btn btn-red" href="{IG}" target="_blank" rel="noopener" data-i18n="btn.ig">Instagram @312history</a><a class="btn btn-line" href="index.html#map" data-i18n="about.map">Explore the map</a></div></div></section>
<section class="about-cols"><div><h2 class="sec-title small" data-i18n="about.values">VALUES</h2><ul class="about-list"><li data-i18n="about.v1"><b>Truth.</b> Only checked facts, with a source in every post.</li><li data-i18n="about.v2"><b>People.</b> History told through human lives, not dry dates.</li><li data-i18n="about.v3"><b>Openness.</b> Chicago for everyone who came here, in Russian and English.</li><li data-i18n="about.v4"><b>Curiosity.</b> We look for secrets and forgotten stories close to home.</li><li data-i18n="about.v5"><b>Respect.</b> We speak with care about tragedies and different cultures.</li></ul></div>
<div><h2 class="sec-title small" data-i18n="about.angle">WHAT MAKES US DIFFERENT</h2><ol class="angle-list"><li data-i18n="about.a1">A fresh, personal view from someone who chose Chicago as home, coming from Kyrgyzstan.</li><li data-i18n="about.a2">Two languages, Russian and English, for an audience almost no one serves.</li><li data-i18n="about.a3">An interactive map on the site: every story is a point on the map.</li><li data-i18n="about.a4">Experience in PR and events: we know how to create events, partnerships and press.</li></ol></div></section></main>""" + foot(0)

def press_page(S):
    # Add real items here as (text, url); a section is shown only when it has items.
    PRESS = {"media": [], "awards": [], "talks": []}
    def block(key, title, ph):
        items = PRESS[key]
        if not items: return ""
        li = "".join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t,u in items)
        return f'''<section class="press-block"><h2 class="sec-title small" data-i18n="press.{key}">{title}</h2><ul class="press-list">{li}</ul></section>'''
    return head("Press & Awards | 312 History", 0, desc="Press kit and contact for 312 History, a bilingual Chicago history project by Ariana Cholponkadyrova.", path="press.html") + f"""
<main class="page"><section class="page-hero"><span class="kicker red" data-i18n="press.kicker">Press & Awards</span>
<h1 class="mega small"><span class="line" data-i18n="press.h1">IN THE</span><span class="line" data-i18n="press.h2">NEWS<b>★</b></span></h1>
<p class="lead dark" data-i18n="press.lead">Articles, interviews and awards about 312 History will be listed here.</p></section>
<div class="press-wrap">
{block("media","PRESS COVERAGE","No coverage yet. Format: outlet, headline, date, link.")}
{block("awards","AWARDS & RECOGNITION","No awards yet. Format: award, organization, year.")}
{block("talks","TALKS & EVENTS","No events yet. Format: event, venue, date.")}
<section class="press-block"><h2 class="sec-title small" data-i18n="press.kit">PRESS KIT & CONTACT</h2><p data-i18n="press.kittext">Journalists: write to us for photos, logos and interviews.</p><p><span data-i18n="press.inq">Press inquiries:</span> <a href="mailto:ariana.cholponkadyrova@gmail.com">ariana.cholponkadyrova@gmail.com</a></p>
<a class="btn btn-line" href="mailto:ariana.cholponkadyrova@gmail.com" data-i18n="press.contact">Contact</a></section>
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
        li="".join(f'<li><a href="stories/{s["slug"]}.html"><img loading="lazy" decoding="async" width="720" height="1280" src="media/post{s["num"]}.jpg" alt="{esc(s["title"])}"><span><b>{esc(s["title"])}</b><em>{esc(s["place"])}</em></span></a></li>' for s in st)
        html+=f'''<div class="walk"><span class="walk-n">0{wi+1}</span><h3 data-i18n="walk{wi}.n">{esc(n).upper()}</h3><p data-i18n="walk{wi}.d">{esc(d)}</p>
<p class="kicker">{len(st)} <span data-i18n="r.stops">stops</span> · ≈{km:.1f} km <span data-i18n="r.straight">straight-line</span></p><ol>{li}</ol>
<button class="btn btn-red" data-route="{wi}" data-i18n="r.show">Show on map ★</button></div>'''
    return head("Walking routes | 312 History",0, desc="Self-guided Chicago history walks built from 312 History stories: the Loop, Michigan Avenue to the lake, and the South Loop.", path="routes.html", extra='<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n') + f"""
<main class="page"><section class="page-hero"><span class="kicker red" data-i18n="r.kicker">Walk it</span>
<h1 class="mega small"><span class="line" data-i18n="r.h1">WALKING</span><span class="line" data-i18n="r.h2">ROUTES<b>★</b></span></h1>
<p class="lead dark" data-i18n="r.lead">Routes built only from published stories with map pins, ordered stop by stop. Times are rough guides; pins are approximate.</p></section>
<section class="routes"><div class="routes-map"><div id="rmap"></div></div><div class="walk-col">{html}</div></section></main>
<script>window.ROUTES={json.dumps(routes)};</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script src="assets/routes.js"></script>""" + foot(0)
