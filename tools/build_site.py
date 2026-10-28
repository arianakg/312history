#!/usr/bin/env python3
"""Build the 312 History static site from ../postNN folders.

Usage:  python3 build_site.py            (from site/)
New posts: add the post folder (caption.txt, sources.md, cover, reel), then add one
line to META below (topic, place, approximate lat/lng) and re-run. Media is copied
and compressed automatically if missing (needs ffmpeg).
"""
import html, json, os, re, subprocess, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root (features branch)
POSTS = "/workspace/chicago-story"  # post folders (read-only)
EXCLUDE = {"post40", "post02"}  # post40 = unpublished DuSable duplicate; post02 = intro reel, no caption
IG = "https://www.instagram.com/312history/"
SIGNUP_ACTION = "mailto:ariana.cholponkadyrova@gmail.com?subject=Subscribe%20to%20312%20History"  # PLACEHOLDER: replace with Buttondown/Mailchimp form action
SUPPORT = "https://ko-fi.com/312history"

# num: (topic, place, lat, lng, year_override)
# ALL COORDINATES ARE APPROXIMATE (street-corner or neighborhood level), for the draft map only.
# year_override: None = take first 4-digit year from the caption; "" = no single year (not on timeline).
META = {
 "03":("ORIGINS","Chicago River mouth",41.8886,-87.6240,1833),
 "04":("ORIGINS","Chicago River",41.8880,-87.6290,""),
 "05":("EVENTS","Whole city (began near DeKoven St)",41.8690,-87.6420,1871),
 "06":("ARCHITECTURE","Loop, LaSalle & Adams",41.8794,-87.6322,1872),
 "07":("LAKEFRONT","Chicago River",41.8869,-87.6170,1900),
 "08":("CULTURE","Bronzeville / South Side",41.8310,-87.6190,1922),
 "09":("ORIGINS","Chicago today",41.8789,-87.6359,2026),
 "10":("ARCHITECTURE","Loop, Lake St",41.8857,-87.6300,None),
 "11":("ARCHITECTURE","Michigan Ave",41.8972,-87.6244,1869),
 "12":("ARCHITECTURE","State St",41.8819,-87.6274,None),
 "13":("ARCHITECTURE","Oak Park / Hyde Park",41.7897,-87.5960,None),
 "14":("ARCHITECTURE","Under the Loop",41.8830,-87.6290,None),
 "15":("EVENTS","Jackson Park",41.7900,-87.5830,1893),
 "16":("EVENTS","Midway Plaisance",41.7870,-87.5960,1893),
 "17":("EVENTS","Chicago River at Clark St",41.8869,-87.6327,1915),
 "18":("EVENTS","Northerly Island",41.8630,-87.6080,1933),
 "19":("EVENTS","Whole city",41.8760,-87.6250,1967),
 "20":("PEOPLE","Near West Side",41.8716,-87.6475,None),
 "21":("PEOPLE","Bronzeville",41.8250,-87.6180,None),
 "22":("PEOPLE","Chicago",41.8530,-87.6240,1920),
 "23":("ARCHITECTURE","Whole city",41.8810,-87.6230,1909),
 "24":("PEOPLE","Chicago",41.8100,-87.6150,None),
 "25":("PEOPLE","Bronzeville",41.8180,-87.6170,None),
 "26":("PEOPLE","Pullman",41.6950,-87.6100,None),
 "27":("PEOPLE","Back of the Yards",41.8160,-87.6650,None),
 "28":("PEOPLE","Pilsen",41.8570,-87.6560,None),
 "29":("PEOPLE","Polish Downtown",41.9020,-87.6640,None),
 "30":("EVENTS","University of Chicago",41.7920,-87.6000,1942),
 "31":("FIRSTS","Chicago",41.8960,-87.6390,None),
 "32":("FIRSTS","Cook County Hospital",41.8695,-87.6740,None),
 "33":("FIRSTS","Chicago",41.8770,-87.6340,1893),
 "34":("FIRSTS","Chicago",41.8800,-87.6300,""),
 "35":("FOOD","Chicago",41.8640,-87.6480,""),
 "36":("FOOD","Chicago",41.8700,-87.6600,""),
 "37":("SPORTS","Wrigleyville",41.9484,-87.6553,1908),
 "38":("SPORTS","South Side",41.8310,-87.6350,1919),
 "39":("ORIGINS","Chicago",41.8830,-87.6320,""),
 "41":("ORIGINS","River mouth / Michigan Ave",41.8877,-87.6245,1803),
 "42":("ORIGINS","City Hall",41.8837,-87.6319,1917),
 "43":("FOOD","River North",41.8920,-87.6270,1943),
 "44":("CULTURE","West Loop",41.8790,-87.6430,None),
 "45":("CULTURE","State St",41.8855,-87.6274,1921),
 "46":("ARCHITECTURE","River at State St",41.8875,-87.6285,None),
 "47":("CULTURE","Old Town",41.9113,-87.6352,1959),
 "48":("TRAVEL","Adams St & Michigan Ave",41.8794,-87.6245,1926),
 "49":("LAKEFRONT","Grant Park",41.8758,-87.6189,1927),
 "50":("ARCHITECTURE","West Loop",41.8786,-87.6403,1925),
 "51":("ARCHITECTURE","Michigan Ave (Cultural Center)",41.8838,-87.6250,1897),
 "52":("LAKEFRONT","Lincoln Park",41.9211,-87.6340,1868),
 "53":("LAKEFRONT","Streeterville",41.8917,-87.6086,1916),
 "54":("LAKEFRONT","Museum Campus",41.8676,-87.6140,1930),
 "55":("ARCHITECTURE","Michigan Ave",41.8904,-87.6234,1925),
 "56":("ARCHITECTURE","LaSalle St",41.8789,-87.6321,1888),
 "57":("LAKEFRONT","Museum Campus",41.8623,-87.6167,1924),
 "58":("NATURE","East Garfield Park",41.8863,-87.7173,1908),
 "59":("ARCHITECTURE","LaSalle St",41.8780,-87.6323,1930),
 "60":("LOST CHICAGO","Belmont & Western",41.9400,-87.6880,1904),
 "61":("NATURE","Uptown",41.9580,-87.6600,1860),
 "62":("ARCHITECTURE","Prairie Ave",41.8572,-87.6213,1887),
 "63":("ARCHITECTURE","Jackson Blvd",41.8779,-87.6295,1891),
 "64":("LAKEFRONT","Harbor east of Navy Pier",41.8893,-87.5916,1893),
 "65":("TRAVEL","State St",41.8800,-87.6276,1882),
 "66":("EVENTS","Randolph St",41.8846,-87.6290,1903),
 "67":("ARCHITECTURE","Printers Row",41.8726,-87.6290,1885),
 "68":("CULTURE","Uptown, Argyle St",41.9730,-87.6640,1907),
 "69":("NATURE","Washington Square",41.8990,-87.6310,1842),
 "70":("LOST CHICAGO","State & Randolph",41.8848,-87.6276,1892),
 "71":("LOST CHICAGO","Loop, Dearborn St",41.8790,-87.6300,1905),
 "72":("CULTURE","Humboldt Park",41.9050,-87.7020,1900),
 "73":("PEOPLE","29th & Dearborn",41.8420,-87.6290,1891),
 "74":("PEOPLE","Chicago",41.8820,-87.6340,None),
 "75":("EVENTS","Haymarket Square, Randolph & Des Plaines",41.8847,-87.6443,1886),
 "76":("PEOPLE","Woodlawn, 60th St",41.7860,-87.5960,1887),
 "77":("CULTURE","Orchestra Hall, Michigan Ave",41.8792,-87.6250,1891),
 "78":("EVENTS","The Wigwam, Lake St & Wacker",41.8858,-87.6366,1860),
 "79":("SPORTS","Cubs Park (Wrigley Field)",41.9484,-87.6553,1920),
 "80":("FIRSTS","Indiana Dunes (outside Chicago)",None,None,1896),
 "81":("CULTURE","Chicago",None,None,1912),
 "82":("PEOPLE","Wabash Avenue YMCA, Bronzeville",41.8256,-87.6252,1895),
 "83":("SPORTS","Café de Champion, 41 W 31st St",41.8382,-87.6280,1912),
 "84":("PEOPLE","Armour Institute (IIT)",41.8349,-87.6270,1890),
 "85":("PEOPLE","Frances Willard House, Evanston",42.0483,-87.6792,1858),
 "86":("CULTURE","Art Institute of Chicago",41.8796,-87.6237,1870),
 "87":("CULTURE","Chicago",None,None,1927),
 "88":("CULTURE","Hull House",41.8717,-87.6477,1909),
 "89":("CULTURE","South Side",None,None,1919),
 "90":("PEOPLE","Hull House",41.8717,-87.6477,1891),
 "91":("CULTURE","Oriental Institute, Hyde Park",41.7892,-87.5975,None),
 "92":("SPORTS","Chicago",None,None,1906),
 "93":("LAKEFRONT","Lake Michigan",None,None,1864),
 "94":("EVENTS","Chicago Coliseum, Wabash Ave",41.8614,-87.6253,1912),
 "95":("TRAVEL","Grant Park lakefront",41.8758,-87.6189,1911),
 "96":("EVENTS","Michigan Ave to the Coliseum",41.8614,-87.6253,1916),
 "97":("CULTURE","Maxwell St & Halsted",41.8645,-87.6466,1912),
 "98":("LOST CHICAGO","White City, 63rd & South Park",41.7800,-87.6150,1905),
 "99":("LOST CHICAGO","Edgewater Beach Hotel, Sheridan Rd",41.9800,-87.6545,1916),
 "100":("CULTURE","Bronzeville to Washington Park",41.7930,-87.6170,1929),
 "101":("CULTURE","Aragon Ballroom, Uptown",41.9690,-87.6580,1926),
 "102":("FIRSTS","Chicago",None,None,1895),
 "103":("NATURE","Lincoln Park Conservatory, Lincoln Park",41.9254,-87.6359,1890),
 "104":("NATURE","Brookfield Zoo, Brookfield (west of Chicago)",41.8317,-87.8353,1937),
 "105":("CULTURE","Museum of Science and Industry, Hyde Park",41.7906,-87.5831,1954),
 "106":("NATURE","Osaka Garden, Wooded Island, Jackson Park",41.7915,-87.5805,1893),
 "107":("CULTURE","Art Institute of Chicago, Michigan Ave",41.8796,-87.6237,1894),
 "108":("ARCHITECTURE","Wrigley Building, 400-410 N Michigan Ave",41.8887,-87.6245,1921),
 "109":("LAKEFRONT","Michigan Avenue Bridge, Chicago River",41.8885,-87.6245,1920),
 "110":("LAKEFRONT","Montrose Point Bird Sanctuary, Lincoln Park",41.9636,-87.6339,""),
 "111":("NATURE","Lurie Garden, Millennium Park",41.8814,-87.6219,2004),
 "112":("ARCHITECTURE","Chinatown Gate, Wentworth Ave at Cermak Rd",41.8528,-87.6322,1975),
 "113":("LAKEFRONT","Promontory Point, Hyde Park",41.7945,-87.5795,1939),
 "114":("ARCHITECTURE","Carbide & Carbon Building, 230 N Michigan Ave",41.8866,-87.6249,1929),
}
TOPICS = {"ORIGINS":"Origins","ARCHITECTURE":"Architecture","LAKEFRONT":"Lake & River","NATURE":"Parks & Gardens",
 "EVENTS":"Big Events","PEOPLE":"People & Neighborhoods","CULTURE":"Culture","FOOD":"Food","FIRSTS":"Firsts",
 "SPORTS":"Sports","TRAVEL":"Getting Around","LOST CHICAGO":"Lost Chicago"}

WALKS = [
 ("The Loop Skyscraper Walk","About 2 hours. Iron, brick and Art Deco, block by block.",["56","59","63","71","70","45","46"]),
 ("Michigan Avenue to the Lake","2–3 hours. From the fort at the river mouth to the last lighthouse.",["51","55","41","11","53","64"]),
 ("South Loop & Museum Campus","2–3 hours. Old station, Route 66, the fountain and the lakefront.",["67","48","49","54","57","62"]),
]

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200d\u21A9]")
def clean(s): return EMOJI.sub("", s).replace("★","").strip()
def esc(s): return html.escape(s, quote=True)
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")[:48]

def linkify(s):
    s = esc(s)
    return re.sub(r"(https?://[^\s<]+)", lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)[:70]}{"…" if len(m.group(1))>70 else ""}</a>', s)

def parse(d):
    num = d[4:]
    txt = open(os.path.join(POSTS,d,"caption.txt"),encoding="utf-8").read().strip()
    paras = [p.strip() for p in re.split(r"\n\s*\n", txt) if p.strip()]
    title = clean(paras[0].splitlines()[0]).rstrip(".")
    lines = [l.strip() for l in txt.splitlines()]
    facts = [clean(l) for l in lines if l.startswith("★") or re.match(r"^[\U0001F300-\U0001FAFF]", l)]
    extra, images, sources_line = [], "", ""
    body = paras[1:]
    hook = ""
    for p in body:
        if p.startswith("#") or p.startswith("Follow 312"): continue
        for l in p.splitlines():
            if l.startswith("Images"):
                m = re.split(r"\s*Sources:\s*", l, maxsplit=1); images = m[0]; sources_line = m[1] if len(m)>1 else sources_line
            elif l.startswith("Sources:"): sources_line = l[8:].strip()
        if p.startswith(("Images","Sources","Script")): continue
        if p.startswith("★") or re.match(r"^[\U0001F300-\U0001FAFF]", p): continue
        if "👇" in p or p.startswith("Follow"): continue
        if not hook: hook = clean(p); continue
        extra.append(clean(p))
    if not facts:  # older paragraph-style captions: paragraphs are the facts
        facts, extra = extra, []
    allt = " ".join([title, hook] + facts)
    topic, place, lat, lng, yo = META[num]
    if yo is None:
        m = re.search(r"\b(1[6-9]\d\d|20[0-2]\d)\b", allt); year = int(m.group(1)) if m else ""
    else: year = yo
    src = []
    sp = os.path.join(POSTS,d,"sources.md")
    if os.path.exists(sp):
        for l in open(sp,encoding="utf-8"):
            l=l.strip()
            if re.match(r"^(-|\d+\.)\s", l): src.append(re.sub(r"^(-|\d+\.)\s+","",l))
    return dict(num=num, title=title, hook=hook, facts=facts, extra=extra, images=images,
                sources_line=sources_line, sources=src[:14], topic=topic, place=place,
                lat=lat, lng=lng, year=year, slug=f"{num}-{slug(title)}")

def ensure_media(d):
    num=d[4:]; jpg=os.path.join(ROOT,"media",f"{d}.jpg"); mp4=os.path.join(ROOT,"media",f"{d}.mp4")
    if not os.path.exists(jpg):
        c=(glob.glob(os.path.join(POSTS,d,f"{d}_cover.jpg"))+glob.glob(os.path.join(POSTS,d,f"{d}_cover_v5.jpg")))[0]
        subprocess.run(["ffmpeg","-v","error","-y","-i",c,"-vf","scale=720:-2","-q:v","5",jpg],check=True)
    if not os.path.exists(mp4):
        r=(glob.glob(os.path.join(POSTS,d,f"{d}_reel.mp4"))+glob.glob(os.path.join(POSTS,d,f"{d}_reel_30.mp4")))[0]
        subprocess.run(["ffmpeg","-v","error","-y","-i",r,"-vf","scale=360:-2","-c:v","libx264","-preset","veryfast","-crf","31","-c:a","aac","-b:a","64k","-movflags","+faststart",mp4],check=True)

SITE = "https://312history.com/"
DEFAULT_DESC = "Chicago history, one story at a time: fact-checked stories on a map, a timeline and walking routes. By 312 History."
# ANALYTICS (disabled). To switch on GoatCounter: create a free account at https://www.goatcounter.com,
# pick a site code (e.g. "312history"), put it here, rebuild and push. Empty string = no analytics script.
GOATCOUNTER = ""
PAGES_SEEN = []  # filled by head(); used for sitemap.xml

def short(t, n=155):
    t = re.sub(r"\s+"," ",clean(t)).strip()
    if len(t) <= n: return t
    return t[:n].rsplit(" ",1)[0].rstrip(",;:.") + "…"

def ld(obj): return '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False).replace("</","<\\/")+"</script>\n"

def head(title, depth, extra="", desc=None, img=None, path="", otype="website", jsonld=None):
    p = "../"*depth
    desc = short(desc or DEFAULT_DESC)
    img = SITE + (img or "img/og-default.jpg")
    url = SITE + path
    if path != "404.html": PAGES_SEEN.append(path)
    ga = (f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'
          if GOATCOUNTER else "<!-- Analytics hook: GoatCounter disabled (set GOATCOUNTER in tools/build_site.py) -->\n")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{otype}"><meta property="og:site_name" content="312 History">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{img}"><meta property="og:image:alt" content="{esc(title)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="en_US"><meta property="og:locale:alternate" content="ru_RU">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{img}">
<link rel="icon" href="{p}favicon.ico" sizes="any"><link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
{ga}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;800;900&display=swap" rel="stylesheet">
{ld(jsonld) if jsonld else ""}{extra}<link rel="stylesheet" href="{p}assets/style.css"></head><body>
<header class="nav"><a class="nav-logo" href="{p}index.html"><img src="{p}img/logo_white_transparent.png" alt="312 History"></a>
<nav><a href="{p}index.html#map" data-i18n="nav.map">Map</a><a href="{p}index.html#topics" data-i18n="nav.stories">Stories</a><a href="{p}routes.html" data-i18n="nav.routes">Walking routes</a><a href="{p}fire-1871.html" data-i18n="nav.fire">Great Fire</a><a href="{p}about.html" data-i18n="nav.about">About</a><a href="{p}press.html" data-i18n="nav.press">Press</a></nav>
<div class="lang" role="group" aria-label="Language"><button data-lang="en">EN</button><button data-lang="ru">RU</button></div>
<a class="btn btn-red nav-ig" href="{IG}" target="_blank" rel="noopener" aria-label="Instagram @312history">★ IG</a></header>"""

def foot(depth):
    p="../"*depth
    return f"""<footer class="foot"><div class="foot-row"><img src="{p}img/logo_white_transparent.png" alt="312 History"><div><p data-i18n="foot.tag">Chicago history, one story at a time. Every fact checked against sources.</p>
<a class="ig-link" href="{IG}" target="_blank" rel="noopener" data-i18n="foot.follow">Follow @312history on Instagram ★</a></div></div>
<div class="foot-btns"><a class="btn btn-line light" href="{IG}" target="_blank" rel="noopener" data-i18n="btn.ig">Instagram @312history</a><a class="btn btn-red" href="{SUPPORT}" target="_blank" rel="noopener" data-i18n="btn.support">Support the project ★</a></div>
<p class="draft" data-i18n="foot.credits">Images: Wikimedia Commons, Library of Congress and other public-domain / CC sources as credited on each story. Map pins are approximate.</p></footer>
<script src="{p}assets/i18n.js"></script><script src="{p}assets/site.js"></script></body></html>"""

def area(s):
    la,ln=s["lat"],s["lng"]
    if la is None: return "CITY"
    if ln<-87.66 and la>41.85: return "WEST"
    if la>41.9: return "NORTH"
    if la>=41.888: return "NEARNORTH"
    if la>=41.872 and ln>-87.645: return "LOOP"
    if la>=41.85: return "NEARSOUTHWEST" if ln<-87.64 else "SOUTHLOOP"
    return "SOUTH"
AREAS={"LOOP":"The Loop","NEARNORTH":"Near North & River","NORTH":"North Side","SOUTHLOOP":"South Loop & Museum Campus","NEARSOUTHWEST":"Near West & Pilsen","WEST":"West Side","SOUTH":"South Side","CITY":"Citywide / no pin"}
ERAS=[("PRE1871","Before 1871",0,1870),("1871","1871–1899",1871,1899),("1900","1900–1945",1900,1945),("1946","1946–today",1946,3000)]
def era(s):
    y=s["year"]
    if not isinstance(y,int): return "NONE"
    return next(k for k,_,a,b in ERAS if a<=y<=b)

def card(s, depth):
    p="../"*depth
    return f"""<a class="card" href="{p}stories/{s['slug']}.html" data-topic="{s['topic']}" data-area="{area(s)}" data-era="{era(s)}" data-q="{esc((s['title']+' '+s['place']+' '+s['hook']).lower())}"><div class="card-img"><img loading="lazy" src="{p}media/post{s['num']}.jpg" alt="{esc(s['title'])} cover"></div>
<div class="card-meta"><span class="kicker"><span data-i18n="topic.{s['topic']}">{esc(TOPICS[s['topic']])}</span> {(' · '+str(s['year'])) if s['year'] else ''}</span><h3>{esc(s['title'])}</h3></div></a>"""

def story_ld(s):
    url=SITE+f"stories/{s['slug']}.html"
    art={"@type":"Article","headline":s['title'][:110],"description":short(s['hook'] or (s['facts'][0] if s['facts'] else DEFAULT_DESC)),
         "image":SITE+f"media/post{s['num']}.jpg","url":url,"mainEntityOfPage":url,"inLanguage":"en",
         "author":{"@type":"Person","name":"Ariana Cholponkadyrova","url":SITE+"about.html"},
         "publisher":{"@type":"Organization","name":"312 History","url":SITE,"logo":{"@type":"ImageObject","url":SITE+"img/logo_white_transparent.png"}},
         "articleSection":TOPICS[s['topic']]}
    if s.get('place'):
        pl={"@type":"Place","name":s['place'],"address":{"@type":"PostalAddress","addressLocality":"Chicago","addressRegion":"IL","addressCountry":"US"}}
        if s.get('lat') is not None and s.get('lng') is not None: pl["geo"]={"@type":"GeoCoordinates","latitude":s['lat'],"longitude":s['lng']}
        art["contentLocation"]=pl
    crumbs={"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"312 History","item":SITE},{"@type":"ListItem","position":2,"name":s['title'],"item":url}]}
    return {"@context":"https://schema.org","@graph":[art,crumbs]}

def story_page(s, all_s):
    facts = "".join(f'<li class="fact reveal"><span class="star">★</span><p>{esc(f)}</p></li>' for f in s["facts"])
    extra = "".join(f'<p class="extra reveal">{esc(e)}</p>' for e in s["extra"])
    srcs = "".join(f"<li>{linkify(x)}</li>" for x in s["sources"])
    same = [x for x in all_s if x["topic"]==s["topic"] and x["num"]!=s["num"]][:3]
    i = [x["num"] for x in all_s].index(s["num"])
    prv, nxt = all_s[i-1], all_s[(i+1)%len(all_s)]
    return head(f"{s['title']} | 312 History", 1, desc=s['hook'] or (s['facts'][0] if s['facts'] else None), img=f"media/post{s['num']}.jpg", path=f"stories/{s['slug']}.html", otype="article", jsonld=story_ld(s)) + f"""
<main class="story">
<section class="story-hero"><div class="story-text"><span class="kicker red">{esc(TOPICS[s['topic']])} · Post #{s['num']}</span>
<div class="big-year">{s['year'] or ''}</div><h1>{esc(s['title']).upper()}</h1><p class="lead">{esc(s['hook'])}</p>
<p class="place">◉ {esc(s['place'])} <span>(map pin approximate)</span></p>
<a class="btn btn-red" href="{IG}" target="_blank" rel="noopener">Follow on Instagram ★</a></div>
<div class="reel"><video controls playsinline preload="none" poster="../media/post{s['num']}.jpg" src="../media/post{s['num']}.mp4"></video><span>Watch the reel</span></div></section>
<section class="facts"><h2 class="sec-title"><span>★</span> {len(s['facts'])} FACTS</h2><ol>{facts}</ol>{extra}</section>
<section class="sources"><h2 class="sec-title small">PRIMARY SOURCES & CREDITS</h2>
{f'<p><b>Sources:</b> {esc(s["sources_line"])}</p>' if s['sources_line'] else ''}{f'<p><b>Images:</b> {esc(s["images"])}</p>' if s['images'] else ''}
{f'<details><summary>Full source list</summary><ul>{srcs}</ul></details>' if srcs else ''}</section>
<section class="related"><h2 class="sec-title small">MORE {esc(TOPICS[s['topic']]).upper()}</h2><div class="grid">{''.join(card(x,1) for x in same)}</div>
<div class="pn"><a href="{prv['slug']}.html">← {esc(prv['title'])}</a><a href="{nxt['slug']}.html">{esc(nxt['title'])} →</a></div></section>
</main>""" + foot(1)

def index_page(S):
    years = [s for s in S if isinstance(s["year"], int)]
    chips = '<button class="chip on" data-f="ALL"><span data-i18n="chip.all">All</span> <i>%d</i></button>' % len(S) + "".join(
        f'<button class="chip" data-f="{k}"><span data-i18n="topic.{k}">{v}</span> <i>{sum(1 for s in S if s["topic"]==k)}</i></button>' for k,v in TOPICS.items() if any(s["topic"]==k for s in S))
    walks = ""
    for wi,(n,d,nums) in enumerate(WALKS):
        stops="".join(f'<li><a href="stories/{s["slug"]}.html"><img loading="lazy" decoding="async" width="720" height="1280" src="media/post{s["num"]}.jpg" alt="{esc(s["title"])}"><span><b>{esc(s["title"])}</b><em>{esc(s["place"])}</em></span></a></li>' for s in [next(x for x in S if x["num"]==k) for k in nums])
        walks+=f'<div class="walk reveal"><span class="walk-n">0{wi+1}</span><h3>{esc(n).upper()}</h3><p>{esc(d)}</p><ol>{stops}</ol><button class="btn btn-line" data-walk="{",".join(nums)}" data-i18n="r.show">Show on map ★</button></div>'
    marquee = " ★ ".join(esc(s["title"]).upper() for s in S)
    return head("312 History | Chicago history, one story at a time", 0, desc=f"{len(S)} fact-checked stories of Chicago history, from Fort Dearborn to today, on an interactive map, a timeline and walking routes.", path="", jsonld={"@context":"https://schema.org","@graph":[
      {"@type":"WebSite","name":"312 History","url":SITE,"inLanguage":["en","ru"],"description":DEFAULT_DESC},
      {"@type":"Organization","name":"312 History","url":SITE,"logo":SITE+"img/logo_white_transparent.png","sameAs":[IG],"founder":{"@type":"Person","name":"Ariana Cholponkadyrova"}}]}, extra=
      '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n') + f"""
<main>
<section class="hero"><div class="hero-inner">
<div class="hero-copy"><img class="hero-logo" src="img/logo_white_transparent.png" alt="312 History logo"><span class="kicker red" data-i18n="home.kicker">Chicago history · one story at a time</span>
<h1 class="mega" data-i18n="home.h1"><span class="line">THE CITY</span><span class="line">THAT BUILT</span><span class="line">ITSELF<b>★</b></span></h1>
<p class="lead" data-i18n="home.lead" data-n="{len(S)}">{len(S)} fact-checked stories from Fort Dearborn to today, on a map, a timeline and walks you can take this weekend.</p>
<div class="cta"><a class="btn btn-red" href="{IG}" target="_blank" rel="noopener" data-i18n="home.follow">Follow @312history ★</a><a class="btn btn-line light" href="#map" data-i18n="home.explore">Explore the map</a></div></div>
<div class="grow"><div class="grow-year"><span id="growYear">1803</span><small data-i18n="home.grows">CHICAGO GROWS</small></div><svg id="skyline" viewBox="0 0 800 520" preserveAspectRatio="xMidYMax meet"></svg></div>
</div><div class="marquee"><div>{marquee} ★ {marquee}</div></div></section>

<section id="map" class="map-sec"><div class="sec-head"><span class="kicker red" data-i18n="map.kicker">Signature feature</span><h2 class="sec-title" data-i18n="map.title">OLD MAPS <span class="outline">OVER</span> TODAY</h2>
<p data-i18n="map.text">Pick a year, slide the old map in and out, tap a red star to open its story.</p></div>
<div class="map-ui"><div class="years" id="years"></div><label class="op"><span data-i18n="map.old">Old map</span> <input id="opacity" type="range" min="0" max="100" value="70"> <b id="opv">70%</b></label></div>
<div class="map-wrap"><div id="leaf"></div><div class="map-note" id="mapNote"></div></div></section>

<section id="timeline" class="tl-sec"><div class="sec-head"><span class="kicker red" data-i18n="tl.kicker">1803 → today</span><h2 class="sec-title" data-i18n="tl.title">EVERY STORY <span class="outline">IN TIME</span></h2><p data-i18n="tl.text">Each star is a story. Hover or tap to preview.</p></div>
<div class="tl" id="tl"></div><div class="tl-card" id="tlCard"></div></section>

<section class="fire-teaser"><img loading="lazy" decoding="async" src="img/fire_flames.jpg" alt="Chicago in Flames, Currier &amp; Ives, 1871"><div><span class="kicker" data-i18n="fire.tkicker">Scroll story</span><h2 data-i18n="fire.ttitle">OCTOBER 8, 1871.<br>CHICAGO BURNS.</h2><a class="btn btn-red" href="fire-1871.html" data-i18n="fire.tbtn">Read the scroll story →</a></div></section>

<section id="topics" class="topics"><div class="sec-head"><span class="kicker red" data-i18n="topics.count" data-n="{len(S)}">{len(S)} stories</span><h2 class="sec-title" data-i18n="topics.title">PICK A <span class="outline">TOPIC</span></h2><p class="ru-note" data-i18n="ru.storynote"></p></div>
<div class="filters"><input id="q" type="search" placeholder="Search stories, places, years…" data-i18n-ph="f.search" aria-label="Search">
<select id="fArea" aria-label="Neighborhood"><option value="ALL" data-i18n="f.allareas">All neighborhoods</option>{''.join(f'<option value="{k}" data-i18n="area.{k}">{v}</option>' for k,v in AREAS.items())}</select>
<select id="fEra" aria-label="Era"><option value="ALL" data-i18n="f.alleras">All eras</option>{''.join(f'<option value="{k}" data-i18n="era.{k}">{n}</option>' for k,n,a,b in ERAS)}<option value="NONE" data-i18n="era.NONE">No single year</option></select>
<span class="count" id="fCount"></span></div><div class="chips">{chips}</div><p class="empty" id="fEmpty" data-i18n="f.empty" hidden>No stories match. Try another filter.</p><div class="grid" id="grid">{''.join(card(s,0) for s in S)}</div></section>

<section id="walks" class="walks"><div class="sec-head"><span class="kicker red" data-i18n="w.kicker">Walk it</span><h2 class="sec-title" data-i18n="w.title">WALKS FROM <span class="outline">THE POSTS</span></h2><p data-i18n="w.text">Routes built only from published stories. Times are rough guides.</p></div><div class="walk-row">{walks}</div></section>
</main>
<script>window.STORIES={json.dumps([dict(num=s['num'],title=s['title'],year=s['year'],topic=s['topic'],topicName=TOPICS[s['topic']],place=s['place'],lat=s['lat'],lng=s['lng'],slug=s['slug'],hook=s['hook']) for s in S])};</script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="assets/home.js"></script>""" + foot(0)

def fire_page(S):
    s = next(x for x in S if x["num"]=="05")
    sent = re.split(r"(?<=\.)\s+(?=When it was over)", s["hook"], maxsplit=1)
    texts = [sent[0], sent[1] if len(sent)>1 else ""] + s["facts"][:2]
    steps = [("img/fire_flames.jpg","Chicago in Flames, Currier & Ives lithograph, 1871 (public domain)"),
             ("img/map_watson_1874.jpg","Burnt district in red, Gaylord Watson map, 1874 (public domain)"),
             ("img/fire_ruins.jpg","Among the Ruins: Monroe and Dearborn, stereoview, 1871 (Newberry Library, public domain)"),
             ("img/fire_safes.jpg","Burnt safes on Dearborn St., C. R. Clark photo, 1871 (Newberry Library, public domain)")]
    blocks = ""
    for i in range(len(steps)):
        t = texts[i]
        blocks += f'<div class="step" data-i="{i}"><div class="step-box"><span class="kicker red">0{i+1}</span><p>{esc(t)}</p></div></div>'
    imgs = "".join(f'<figure class="fig{" on" if i==0 else ""}" data-i="{i}"><img src="{im}" alt="{esc(c)}"><figcaption>{esc(c)}</figcaption></figure>' for i,(im,c) in enumerate(steps))
    return head("The Great Chicago Fire, 1871 | 312 History scroll story",0, desc="Scroll through the Great Chicago Fire of October 8, 1871, step by step, with archival images and checked facts.", img="img/fire_flames.jpg", path="fire-1871.html") + f"""
<main class="scrolly"><section class="fire-hero"><span class="kicker red">Scroll story · from post #05</span><h1 class="mega"><span class="line">OCTOBER 8,</span><span class="line">1871.</span><span class="line">CHICAGO<b>★</b></span><span class="line">BURNS.</span></h1><p class="lead">Scroll down ↓</p></section>
<section class="scroll-wrap"><div class="sticky">{imgs}</div><div class="steps">{blocks}</div></section>
<section class="fire-end"><h2 class="sec-title">THE FULL STORY</h2><p>Watch the reel and see the sources.</p><a class="btn btn-red" href="stories/{s['slug']}.html">Open the story page →</a></section></main>
<script>
const figs=[...document.querySelectorAll('.fig')];
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{const i=e.target.dataset.i;figs.forEach(f=>f.classList.toggle('on',f.dataset.i===i));e.target.classList.add('in');}}}}),{{rootMargin:'-45% 0px -45% 0px'}});
document.querySelectorAll('.step').forEach(s=>io.observe(s));
</script>""" + foot(0)

def main():
    dirs = sorted((d for d in os.listdir(POSTS) if re.fullmatch(r"post\d{2,3}", d) and d not in EXCLUDE
                  and os.path.exists(os.path.join(POSTS,d,"caption.txt")) and d[4:] in META), key=lambda d:int(d[4:]))
    missing = [d for d in os.listdir(POSTS) if re.fullmatch(r"post\d{2,3}",d) and d not in EXCLUDE and os.path.exists(os.path.join(POSTS,d,"caption.txt")) and d[4:] not in META]
    if missing: print("WARNING: add META for", missing)
    os.makedirs(os.path.join(ROOT,"stories"),exist_ok=True); os.makedirs(os.path.join(ROOT,"media"),exist_ok=True)
    S=[]
    for d in dirs:
        ensure_media(d); S.append(parse(d))
    for s in S:
        open(os.path.join(ROOT,"stories",s["slug"]+".html"),"w",encoding="utf-8").write(story_page(s,S))
    open(os.path.join(ROOT,"index.html"),"w",encoding="utf-8").write(index_page(S))
    open(os.path.join(ROOT,"fire-1871.html"),"w",encoding="utf-8").write(fire_page(S))
    from pages import about_page, press_page, routes_page
    for fn,f in (("about.html",about_page),("press.html",press_page),("routes.html",routes_page)):
        open(os.path.join(ROOT,fn),"w",encoding="utf-8").write(f(S))
    json.dump(S, open(os.path.join(ROOT,"stories.json"),"w"), indent=1, ensure_ascii=False)
    nf = head("Page not found | 312 History", 0, '<base href="/">\n<meta name="robots" content="noindex">\n', desc="This page does not exist. Explore Chicago history stories on 312 History.", path="404.html") + """
<main class="page"><section class="page-hero"><span class="kicker red">Error 404</span>
<h1 class="mega small"><span class="line">LOST IN</span><span class="line">CHICAGO<b>★</b></span></h1>
<p class="lead dark">This page does not exist, but 99+ stories do.</p>
<div class="cta"><a class="btn btn-red" href="index.html">Back to the map ★</a><a class="btn btn-line" href="index.html#topics">All stories</a></div></section></main>""" + foot(0)
    open(os.path.join(ROOT,"404.html"),"w",encoding="utf-8").write(nf)
    import datetime; today=datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in dict.fromkeys(PAGES_SEEN))
    open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
    open(os.path.join(ROOT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    print(f"built {len(S)} stories")

if __name__=="__main__": main()
