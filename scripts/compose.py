"""Cover image, phone/browser frames and web-sized screenshots for docs/ from docs/raw/."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pathlib
R = pathlib.Path(__file__).resolve().parent.parent / 'docs'
raw = R / 'raw'; (R / 'screens').mkdir(exist_ok=True)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def grad(w, h):
    im = Image.new('RGB', (w, h)); px = im.load()
    for y in range(h):
        for x in range(w):
            t = (x / w * .6 + y / h * .4)
            a = (11, 31, 58); b = (23, 70, 160); c = (14, 165, 183)
            col = [int(a[i] + (b[i] - a[i]) * min(1, t * 1.6)) for i in range(3)]
            if t > .62: col = [int(col[i] + (c[i] - col[i]) * (t - .62) / .38 * .7) for i in range(3)]
            px[x, y] = tuple(col)
    return im
def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, *im.size], r, fill=255)
    o = Image.new('RGBA', im.size); o.paste(im, (0, 0), m); return o
def shadow(canvas, box, r, blur=30, off=18, alpha=110):
    s = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    x0, y0, x1, y1 = box; d.rounded_rectangle([x0, y0 + off, x1, y1 + off], r, fill=(0, 10, 30, alpha))
    canvas.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))
def browser(shot, w):
    im = Image.open(shot).convert('RGB'); h = int(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
    bar = 34; fr = Image.new('RGB', (w, h + bar), (236, 241, 248)); d = ImageDraw.Draw(fr)
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]): d.ellipse([14 + i * 18, 12, 24 + i * 18, 22], fill=c)
    d.rounded_rectangle([w // 2 - 160, 8, w // 2 + 160, 26], 9, fill=(255, 255, 255))
    fr.paste(im, (0, bar)); return rounded(fr, 14)
def phone(shot, w):
    im = Image.open(shot).convert('RGB'); sh = int(w * 844 / 390); im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS).crop((0, 0, w, sh))
    b = 12; fr = Image.new('RGBA', (w + 2 * b, sh + 2 * b), (0, 0, 0, 0)); d = ImageDraw.Draw(fr)
    d.rounded_rectangle([0, 0, w + 2 * b, sh + 2 * b], 46, fill=(12, 16, 26, 255))
    fr.alpha_composite(rounded(im, 36), (b, b)); d.rounded_rectangle([w // 2 + b - 46, b + 10, w // 2 + b + 46, b + 34], 12, fill=(12, 16, 26, 255))
    return fr
def place(canvas, img, xy, r=14):
    shadow(canvas, (xy[0], xy[1], xy[0] + img.width, xy[1] + img.height), r); canvas.alpha_composite(img, xy)
# cover 1600x900
W, H = 1600, 900; cv = grad(W, H).convert('RGBA')
place(cv, browser(raw / 'labs-desktop.png', 900), (620, 70))
place(cv, browser(raw / 'fuel-desktop.png', 900), (90, 300))
ph = phone(raw / 'labs-mobile.png', 250); place(cv, ph, (1290, 330), 46)
cv.convert('RGB').save(R / 'cover.jpg', quality=86, optimize=True, progressive=True)
# square social 1080
S = grad(1080, 1080).convert('RGBA'); d = ImageDraw.Draw(S)
d.text((70, 80), 'FUEL & LABS', font=ImageFont.truetype(F, 30), fill=(200, 230, 255))
d.text((70, 125), 'Two apps for a\nmarathon build', font=ImageFont.truetype(F, 74), fill='white', spacing=6)
place(S, phone(raw / 'fuel-mobile.png', 300), (110, 370), 46); place(S, phone(raw / 'labs-mobile.png', 300), (560, 420), 46)
S.convert('RGB').save(R / 'social.jpg', quality=86)
# screens
for n in ['fuel-desktop', 'fuel-meals', 'fuel-build', 'fuel-juices', 'fuel-shop', 'fuel-dark', 'labs-desktop', 'labs-heatmap', 'labs-systems', 'labs-explore', 'labs-dark', 'launcher']:
    im = Image.open(raw / f'{n}.png').convert('RGB'); im.thumbnail((1440, 1440)); im.save(R / 'screens' / f'{n}.jpg', quality=82, optimize=True, progressive=True)
for n in ['fuel-mobile', 'fuel-mobile-meals', 'labs-mobile']:
    p = phone(raw / f'{n}.png', 360); bg = Image.new('RGB', p.size, (243, 246, 251)); bg.paste(p, (0, 0), p); bg.save(R / 'screens' / f'{n}.jpg', quality=84)
    p.save(R / 'screens' / f'{n}-frame.png')
im = Image.open(R / 'cover.jpg'); im.thumbnail((800, 800)); im.save(R / 'thumb.webp', quality=80)
print('ok')
