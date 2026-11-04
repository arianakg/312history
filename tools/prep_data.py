# Builds data/datamaps.json + compressed media from /workspace/chicago-story/*_map (run locally; not needed at build time)
import os,re,json,glob,subprocess
from PIL import Image
R='/workspace/312history-deploy/repo'; C='/workspace/chicago-story'
PREF={'births_map':'births_map_reel_oldstyle_remux.mp4','foodtruck_map':'foodtruck_map_reel_classic.mp4','towed_map':'buildings_map_reel.mp4'}
EXCLUDE={'shootings_map','bikeracks_map'}
ORDER=['rats','L','divvy','dognames','foodtruck','film','beach','trees','towed','traffic']
out=[];miss=[]
for d in sorted(glob.glob(C+'/*_map')):
    k=os.path.basename(d); key=k[:-4]
    if k in EXCLUDE: continue
    v=os.path.join(d,PREF.get(k,k+'_reel.mp4'))
    cov=[p for p in glob.glob(d+'/*cover_v5.jpg') if 'flat_old' not in p]
    if not (os.path.exists(v) and cov and os.path.exists(d+'/caption.txt')): miss.append(k); continue
    if subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v],capture_output=True,text=True).returncode: miss.append(k); continue
    L=[l.strip() for l in open(d+'/caption.txt',encoding='utf-8') if l.strip()]
    first=L[0].split('★')[0].strip(); rest=L[0].split('★',1)[1].strip() if '★' in L[0] and L[0].split('★',1)[1].strip() else ''
    title=first.title().replace("'S","'s").replace("’S","’s") if first.isupper() else first
    hook=rest or L[1]
    hook=re.sub(r'[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]','',hook).strip()
    src=next((l for l in L if re.match(r'(Data|Source)',l,re.I)),'')
    src=re.sub(r'^(Data/Sources|Data and sources|Data & sources|Sources?|Data)\s*:\s*','',src,flags=re.I)
    src=src.split(';')[0].strip()
    if len(hook)>170: hook=hook[:hook.rfind(' ',0,165)]+'…'
    im=Image.open(cov[0]).convert('RGB').resize((432,768),Image.LANCZOS); im.save(f'{R}/img/data/{key}.jpg',quality=80,optimize=True)
    mp=f'{R}/media/data/{key}.mp4'
    if not os.path.exists(mp):
        subprocess.run(['ffmpeg','-v','error','-y','-i',v,'-vf','scale=360:640','-c:v','libx264','-crf','32','-preset','slow','-profile:v','main','-pix_fmt','yuv420p','-c:a','aac','-b:a','64k','-movflags','+faststart',mp],check=True)
    out.append(dict(key=key,title=title,hook=hook,source=src))
out.sort(key=lambda d:(ORDER.index(d['key']) if d['key'] in ORDER else len(ORDER),d['key']))
json.dump(out,open(f'{R}/data/datamaps.json','w'),indent=1,ensure_ascii=False)
print(len(out),'included; missing:',miss)
