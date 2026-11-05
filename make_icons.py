"""Генерирует иконки приложения (icon-180/192/512.png): листок календаря + палец с накрашенным ногтем."""
from PIL import Image, ImageDraw, ImageFilter
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = 1024


def grad(size, a, b, diag=True):
    g = Image.new('RGB', (2, 2))
    g.putpixel((0, 0), a); g.putpixel((1, 1), b)
    g.putpixel((1, 0), tuple((x + y) // 2 for x, y in zip(a, b))); g.putpixel((0, 1), g.getpixel((1, 0)))
    return g.resize(size, Image.BILINEAR)


# фон
img = grad((S, S), (250, 214, 214), (241, 160, 170)).convert('RGBA')

# тень листка
sh = Image.new('L', (S, S), 0)
ImageDraw.Draw(sh).rounded_rectangle((190, 250, 834, 890), 110, fill=90)
img.paste((150, 60, 80, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(28)))

# листок календаря
card = (180, 230, 844, 870)
mask = Image.new('L', (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle(card, 110, fill=255)
layer = Image.new('RGBA', (S, S), (255, 255, 255, 255))
d = ImageDraw.Draw(layer)
# шапка
d.rectangle((0, 0, S, 395), fill=(217, 96, 122))
# точки-дни
for row in range(2):
    for col in range(5):
        x, y = 262 + col * 125, 465 + row * 95
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(246, 220, 224))
# палец
skin = (247, 206, 186)
d.rounded_rectangle((372, 560, 652, 1000), 140, fill=skin)
d.rounded_rectangle((372, 560, 652, 1000), 140, outline=(232, 180, 160), width=6)
# ноготь
nail = Image.new('RGBA', (S, S), (0, 0, 0, 0))
nm = Image.new('L', (S, S), 0)
ImageDraw.Draw(nm).rounded_rectangle((418, 600, 606, 840), 94, fill=255)
ng = grad((S, S), (240, 110, 140), (196, 50, 92))
nail.paste(ng, (0, 0), nm)
nd = ImageDraw.Draw(nail)
# блик
hl = Image.new('L', (S, S), 0)
ImageDraw.Draw(hl).rounded_rectangle((452, 632, 488, 760), 18, fill=200)
nail.paste((255, 255, 255, 255), (0, 0), hl.filter(ImageFilter.GaussianBlur(3)))
layer.alpha_composite(nail)
img.paste(layer, (0, 0), mask)

# кольца календаря
d = ImageDraw.Draw(img)
for x in (360, 664):
    d.rounded_rectangle((x - 26, 175, x + 26, 300), 26, fill=(255, 255, 255))
    d.rounded_rectangle((x - 26, 175, x + 26, 300), 26, outline=(200, 80, 105), width=8)

# блёстка
def star(cx, cy, r):
    d.polygon([(cx, cy - r), (cx + r * .22, cy - r * .22), (cx + r, cy), (cx + r * .22, cy + r * .22),
               (cx, cy + r), (cx - r * .22, cy + r * .22), (cx - r, cy), (cx - r * .22, cy - r * .22)], fill=(255, 255, 255))
star(735, 330, 46)
star(800, 255, 22)

img = img.convert('RGB')
for n in (180, 192, 512):
    img.resize((n, n), Image.LANCZOS).save(os.path.join(HERE, f'icon-{n}.png'), optimize=True)
print('ok')
