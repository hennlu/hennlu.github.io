#!/usr/bin/env python3
"""Generate an A5 concert cover from the public event poster. Requires Pillow."""
from pathlib import Path
from urllib.request import urlretrieve
from PIL import Image, ImageDraw, ImageFont

poster_url = "https://orchestre-universitaire-picardie.fr/wp-content/uploads/2026/10/bach_saint_acheul_22_novembre_16h.png"
poster_file = Path("affiche_originale.png")
if not poster_file.exists():
    urlretrieve(poster_url, poster_file)
im = Image.open(poster_file).convert("RGB")
w,h = im.size
H = int(w * 595.276 / 419.528)  # A5 portrait
im = im.crop((0,0,w,min(h,H)))
if im.height != H:
    im = im.resize((w,H))

draw=ImageDraw.Draw(im)
def font(size, italic=False):
    import os
    candidates=([
       "/usr/share/fonts/truetype/ebgaramond/EBGaramond08-Italic.ttf" if italic else "/usr/share/fonts/truetype/ebgaramond/EBGaramond08-Regular.ttf",
       "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ])
    for f in candidates:
        if os.path.isfile(f):
            return ImageFont.truetype(f,size)
    return ImageFont.load_default()
def centered(text,y,size,italic=False,color=(35,32,30)):
    f=font(size,italic)
    bb=draw.textbbox((0,0),text,font=f)
    draw.text(((w-(bb[2]-bb[0]))/2,y),text,font=f,fill=color)
# Reorder the three suites on the illustration.
draw.rectangle((int(w*.29),int(H*.265),int(w*.73),int(H*.432)),fill="white")
for i,(title,bwv) in enumerate([("Suite n° 3 en ut majeur","BWV 1009"),("Suite n° 2 en ré mineur","BWV 1008"),("Suite n° 1 en sol majeur","BWV 1007")]):
    centered(title,int(H*.273)+i*49,26)
    centered(bwv,int(H*.296)+i*49,20,italic=True)
# Remove lower booking details; replace with a minimal concert footer.
draw.rectangle((0,int(H*.835),int(w*.53),H),fill="white")
draw.text((int(w*.05),int(H*.852)),"LUCIEN HENNECART",font=font(27),fill=(44,34,30))
draw.text((int(w*.07),int(H*.887)),"violoncelle",font=font(25,italic=True),fill=(124,39,30))
draw.text((int(w*.035),int(H*.927)),"ÉGLISE SAINT-ACHEUL",font=font(29),fill=(146,32,26))
draw.text((int(w*.14),int(H*.960)),"AMIENS · 22 NOVEMBRE · 16 H",font=font(19),fill=(44,34,30))
# Output the exact A5 ratio for the pdfpages wrapper.
im.save("couverture_ordree.pdf", "PDF", resolution=72*w/419.528)
print("Couverture créée :", Path("couverture_ordree.pdf").resolve())
