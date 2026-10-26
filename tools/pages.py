"""Extra pages for the features branch: About, Press & Awards, Walking routes."""
import json, math
from __main__ import head, foot, esc, TOPICS, WALKS, IG

def about_page(S):
    return head("About — 312 History", 0) + f"""
<main class="page"><section class="page-hero"><span class="kicker red" data-i18n="about.kicker">About the project</span>
<h1 class="mega small"><span class="line" data-i18n="about.h1">CHICAGO HISTORY</span><span class="line" data-i18n="about.h2">THROUGH AN</span><span class="line" data-i18n="about.h3">IMMIGRANT'S EYES<b>★</b></span></h1></section>
<section class="about-grid"><figure class="portrait"><img src="img/ariana-portrait.jpg" alt="Ariana Cholponkadyrova, creator of 312 History" width="576" height="1024"></figure>
<div class="about-text">
<h2 class="sec-title small" data-i18n="about.who">WHO IS BEHIND 312 HISTORY</h2>
<p data-i18n="about.p1">Hi, I'm Ariana Cholponkadyrova, the creator of 312 History. I'm from Kyrgyzstan, and Chicago is now my home.</p>
<p data-i18n="about.p2">Back in Kyrgyzstan I worked on vocational and technical education projects. In agriculture I helped advance the green economy: we built greenhouses and ran green-economy courses. I was the coordinator and organizer of Karagat Fest, the annual berry and fruit festival of the Issyk-Kul region, and worked as a PR specialist on many projects. My background is in event management and a major PR agency.</p>
<p data-i18n="about.p2b">In Chicago I'm a content creator and a mom of two: my daughter is 5 and my son is 9. I also run a small business printing designs on T-shirts and tote bags, a craft I love. I enjoy photography and making beautiful videos, and right now I'm studying AI neuro-content and AI agents.</p>
<h2 class="sec-title small" data-i18n="about.mission">MISSION</h2>
<p data-i18n="about.p3">Chicago was built by immigrants. 312 History tells the city's stories through an immigrant's eyes, in short videos and on an interactive map, so anyone can discover what happened right on their block.</p>
<ul class="about-list"><li data-i18n="about.l1">Short videos on Instagram</li><li data-i18n="about.l2">An interactive map of every story</li><li data-i18n="about.l3">Every fact checked against sources</li></ul>
<div class="cta"><a class="btn btn-red" href="{IG}" target="_blank" rel="noopener" data-i18n="btn.ig">Instagram @312history</a><a class="btn btn-line" href="index.html#map" data-i18n="about.map">Explore the map</a></div>
</div></section></main>""" + foot(0)

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
