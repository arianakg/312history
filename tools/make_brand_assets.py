"""One-off: generates img/og-default.jpg (1200x630), favicon.ico, apple-touch-icon.png from the brand logos."""
from PIL import Image, ImageDraw, ImageFont
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ink=(17,17,17);cream=(245,241,234);red=(228,0,43);blue=(179,221,242)
W=Image.open(f'{R}/img/logo_white_transparent.png').convert('RGBA'); B=Image.open(f'{R}/img/logo_black_transparent.png').convert('RGBA')
F='/usr/share/fonts/truetype/sand-box/google/Montserrat/Montserrat-VariableFont_wght.ttf'
def font(sz):
    f=ImageFont.truetype(F,sz)
    try: f.set_variation_by_name('Black')
    except Exception: pass
    return f
og=Image.new('RGB',(1200,630),ink); lg=W.copy(); lg.thumbnail((380,380)); og.paste(lg,(90,(630-lg.size[1])//2),lg)
d=ImageDraw.Draw(og); d.rectangle([0,600,1200,630],fill=red)
for i,t in enumerate(["CHICAGO HISTORY","ONE STORY","AT A TIME"]): d.text((540,200+70*i),t,font=font(56),fill=(255,255,255))
d.text((540,440),"312history.com",font=font(30),fill=blue)
og.save(f'{R}/img/og-default.jpg',quality=90)
def sq(n,pad):
    im=Image.new('RGBA',(n,n),cream+(255,)); l=B.copy(); l.thumbnail((n-2*pad,n-2*pad),Image.LANCZOS); im.paste(l,((n-l.size[0])//2,(n-l.size[1])//2),l); return im
sq(180,18).convert('RGB').save(f'{R}/apple-touch-icon.png')
sq(256,20).save(f'{R}/favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
