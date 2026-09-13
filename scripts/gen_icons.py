from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'icons')
os.makedirs(OUT, exist_ok=True)

BG = (10, 10, 10, 255)
GREEN = (0, 255, 136, 255)


def draw_mark(size, padding_ratio, corner_ratio, bg=BG):
    img = Image.new('RGBA', (size, size), bg)
    d = ImageDraw.Draw(img)

    pad = int(size * padding_ratio)
    frame_w = size - 2 * pad
    corner = int(frame_w * corner_ratio)
    thickness = max(2, int(frame_w * 0.09))

    x0, y0 = pad, pad
    x1, y1 = size - pad, size - pad

    def corner_lines(cx, cy, dx, dy):
        # dx/dy: +1 or -1 direction the arms extend
        d.line([(cx, cy), (cx + dx * corner, cy)], fill=GREEN, width=thickness)
        d.line([(cx, cy), (cx, cy + dy * corner)], fill=GREEN, width=thickness)

    corner_lines(x0, y0, 1, 1)
    corner_lines(x1, y0, -1, 1)
    corner_lines(x0, y1, 1, -1)
    corner_lines(x1, y1, -1, -1)

    # center square (scan target)
    cs = int(frame_w * 0.28)
    cx0 = size // 2 - cs // 2
    cy0 = size // 2 - cs // 2
    d.rounded_rectangle([cx0, cy0, cx0 + cs, cy0 + cs], radius=int(cs * 0.18), fill=GREEN)

    return img


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path, 'PNG')
    print('wrote', path)


# Standard + maskable icons
for size in (192, 512):
    icon = draw_mark(size, padding_ratio=0.12, corner_ratio=0.42)
    save(icon, f'icon-{size}.png')

    maskable = draw_mark(size, padding_ratio=0.22, corner_ratio=0.38)
    save(maskable, f'icon-maskable-{size}.png')

# Apple touch icon (opaque background required)
apple = draw_mark(180, padding_ratio=0.16, corner_ratio=0.4)
save(apple, 'apple-touch-icon.png')

# Favicon sizes
for size in (16, 32, 48):
    fav = draw_mark(size, padding_ratio=0.08, corner_ratio=0.42)
    save(fav, f'favicon-{size}.png')
