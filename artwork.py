#!/usr/bin/env python3
"""Draw the front page of 20 November 2026 as a 1024x1024 PNG.

Everything is drawn with Pillow primitives: no downloaded images, no
network, fully deterministic. Run: python3 artwork.py -> entry.png
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (198, 148, 40)
GREY = (90, 86, 76)
LIGHT = (238, 231, 214)
SKY = (214, 230, 240)
SEA = (46, 110, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill=INK, max_w=None, leading=1.25,
               align="left"):
    """Draw wrapped text; return y just below the last line."""
    lines = wrap(draw, text, fnt, max_w) if max_w else [text]
    lh = int(fnt.size * leading)
    for line in lines:
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=fnt)) // 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += lh
    return y


def panel(draw, box, fill=(255, 255, 255), outline=INK, width=2):
    draw.rectangle(box, fill=fill, outline=outline, width=width)


def flag_us(draw, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        c = (178, 34, 34) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                       fill=c)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(28, 48, 96))
    for r in range(4):
        for c_ in range(5):
            px = x + 8 + c_ * (cw - 14) / 4
            py = y + 6 + r * (ch - 12) / 3
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.28
    draw_star(draw, cx, cy, h * 0.16, (255, 222, 0))
    for sx, sy in [(0.42, 0.14), (0.52, 0.28), (0.52, 0.48), (0.42, 0.62)]:
        draw_star(draw, x + w * sx, y + h * sy, h * 0.06, (255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)


def draw_star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=INK,
                 width=3)
    for k in range(-2, 3):
        off = k * r / 3
        draw.arc([cx - r, cy - r, cx + r, cy + r], -60, 60,
                 fill=SEA, width=2)
        draw.ellipse([cx - abs(off) * 0.55, cy - r, cx + abs(off) * 0.55,
                      cy + r], outline=SEA, width=2)
    draw.line([cx - r, cy - r * 0.25, cx + r, cy - r * 0.25], fill=SEA, width=2)
    draw.line([cx - r, cy + r * 0.35, cx + r, cy + r * 0.35], fill=SEA, width=2)
    # land blobs
    draw.ellipse([cx - r * 0.7, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
                 fill=(96, 160, 90))
    draw.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.65, cy + r * 0.6],
                 fill=(96, 160, 90))


def draw_cyclone(draw, cx, cy, r):
    import math
    for turn in range(3):
        pts = []
        for a in range(0, 300):
            ang = math.radians(a + turn * 90)
            rr = r * (0.15 + 0.85 * a / 300)
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.line(pts, fill=SEA, width=5)
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 255),
                 outline=INK, width=2)
    # rain
    for i, dx in enumerate([-r * 0.9, -r * 0.5, 0, r * 0.5, r * 0.9]):
        draw.line([cx + dx, cy + r * 0.75, cx + dx - 6, cy + r * 1.05],
                  fill=SEA, width=3)


def draw_scales(draw, cx, cy, s):
    # post
    draw.line([cx, cy - s, cx, cy + s], fill=INK, width=4)
    draw.line([cx - s * 0.9, cy - s * 0.7, cx + s * 0.9, cy - s * 0.7],
              fill=INK, width=4)
    draw.ellipse([cx - 6, cy - s - 8, cx + 6, cy - s + 8], fill=GOLD,
                 outline=INK, width=2)
    for side in (-1, 1):
        px = cx + side * s * 0.9
        draw.line([px, cy - s * 0.7, px, cy - s * 0.1], fill=INK, width=3)
        draw.polygon([(px - s * 0.45, cy - s * 0.1), (px + s * 0.45, cy - s * 0.1),
                      (px, cy + s * 0.35)], fill=GOLD, outline=INK)
    draw.line([cx - s * 0.55, cy + s, cx + s * 0.55, cy + s], fill=INK, width=5)


def draw_embassy(draw, x, y, w, h):
    # building with columns
    draw.rectangle([x, y, x + w, y + h], fill=(232, 222, 196), outline=INK,
                   width=2)
    draw.polygon([(x - 4, y), (x + w / 2, y - h * 0.22), (x + w + 4, y)],
                 fill=RED, outline=INK)
    for i in range(4):
        cx = x + w * (0.18 + i * 0.21)
        draw.rectangle([cx - 5, y + h * 0.18, cx + 5, y + h * 0.8], fill=INK)
    draw.rectangle([x, y + h * 0.82, x + w, y + h], fill=INK)
    # blast starburst
    import math
    bx, by, br = x + w * 0.85, y + h * 0.1, h * 0.35
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = br if i % 2 == 0 else br * 0.45
        pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    draw.polygon(pts, fill=(255, 196, 0), outline=RED)


def draw_bat_ball(draw, cx, cy, r):
    # cricket bat
    draw.rounded_rectangle([cx - r * 0.55, cy - r * 0.35, cx + r * 0.15,
                            cy + r * 0.9], radius=8, fill=(210, 180, 130),
                           outline=INK, width=2)
    draw.rectangle([cx - r * 0.18, cy - r * 0.9, cx - r * 0.02, cy - r * 0.3],
                   fill=(120, 80, 40))
    # ball
    draw.ellipse([cx + r * 0.35, cy - r * 0.75, cx + r * 0.95, cy - r * 0.15],
                 fill=RED, outline=INK, width=2)
    draw.arc([cx + r * 0.35, cy - r * 0.75, cx + r * 0.95, cy - r * 0.15],
             200, 340, fill=(255, 255, 255), width=2)


def draw_chip(draw, cx, cy, s):
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=INK)
    draw.rectangle([cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6],
                   fill=(60, 200, 160), outline=(255, 255, 255), width=2)
    for i in range(5):
        off = -s + i * (2 * s / 4)
        draw.line([cx + off, cy - s - 12, cx + off, cy - s], fill=INK, width=3)
        draw.line([cx + off, cy + s, cx + off, cy + s + 12], fill=INK, width=3)
        draw.line([cx - s - 12, cy + off, cx - s, cy + off], fill=INK, width=3)
        draw.line([cx + s, cy + off, cx + s + 12, cy + off], fill=INK, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=4)
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)

    # ---------- masthead ----------
    y = 30
    text_block(d, 0, y, "THE WORLD TODAY", SERIF_B(66), INK,
               max_w=W, align="center")
    y = 108
    d.line([40, y, W - 40, y], fill=INK, width=3)
    y = 118
    text_block(d, 0, y, "FRIDAY  •  20 NOVEMBER 2026", SANS_B(34), RED,
               max_w=W, align="center")
    y = 158
    d.line([40, y, W - 40, y], fill=INK, width=2)
    text_block(d, 0, 166, "ONE DAY, ONE PAGE — THE WORLD'S NEWS, AS REPORTED TODAY",
               SANS_B(17), GREY, max_w=W, align="center")

    # ---------- lead story ----------
    panel(d, [28, 196, 996, 470], fill=(255, 255, 255))
    text_block(d, 48, 210, "THE THREE-POWER SUMMIT", SANS_B(20), RED, max_w=640)
    text_block(d, 48, 236,
               "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
               SERIF_B(40), INK, max_w=660, leading=1.1)
    text_block(d, 48, 330,
               "First-ever three-way talks in China end with a joint peace "
               "declaration: nuclear arms control, energy security and the "
               "war in Ukraine on the table at the APEC summit.",
               SANS(21), INK, max_w=620, leading=1.3)
    # flags + globe on the right
    flag_us(d, 700, 218, 120, 64)
    flag_cn(d, 836, 218, 120, 64)
    flag_ru(d, 700, 296, 120, 64)
    d.text((700, 372), "APEC  •  SHENZHEN, CHINA", font=SANS_B(15),
           fill=GREY)
    draw_globe(d, 880, 432, 34)

    # ---------- middle row: cyclone + ICJ ----------
    # cyclone
    panel(d, [28, 484, 500, 700], fill=(255, 255, 255))
    text_block(d, 48, 498, "CYCLONE AKVAN", SANS_B(22), BLUE, max_w=300)
    text_block(d, 48, 526,
               "Storm makes landfall on India's east coast",
               SERIF_B(24), INK, max_w=300, leading=1.15)
    text_block(d, 48, 596,
               "80,000 people evacuated in Odisha; schools shut, trains "
               "cancelled as heavy rain begins.",
               SANS(18), INK, max_w=290, leading=1.3)
    draw_cyclone(d, 410, 585, 62)
    # ICJ
    panel(d, [516, 484, 996, 700], fill=(255, 255, 255))
    text_block(d, 536, 498, "WORLD COURT  •  THE HAGUE", SANS_B(22), BLUE,
               max_w=440)
    text_block(d, 536, 526,
               "MYANMAR GUILTY OF GENOCIDE",
               SERIF_B(26), INK, max_w=440, leading=1.15)
    text_block(d, 536, 590,
               "The ICJ rules Myanmar committed genocide against the "
               "Rohingya in 2017 — a first for the court.",
               SANS(18), INK, max_w=300, leading=1.3)
    draw_scales(d, 905, 600, 55)

    # ---------- bottom row: Kyiv, cricket, AI ----------
    # Kyiv
    panel(d, [28, 714, 344, 940], fill=(255, 255, 255))
    text_block(d, 44, 726, "KYIV UNDER FIRE", SANS_B(19), RED, max_w=290)
    text_block(d, 44, 750,
               "Russian drones hit two embassies",
               SERIF_B(22), INK, max_w=288, leading=1.15)
    draw_embassy(d, 70, 812, 200, 50)
    text_block(d, 44, 872,
               "One killed; two embassies damaged, cathedral windows "
               "shattered.",
               SANS(16), INK, max_w=288, leading=1.25)
    # cricket
    panel(d, [360, 714, 664, 940], fill=(255, 255, 255))
    text_block(d, 376, 726, "CRICKET  •  WELLINGTON", SANS_B(19), RED, max_w=272)
    text_block(d, 376, 750,
               "NICHOLLS 113* LIFTS NZ",
               SERIF_B(22), INK, max_w=272, leading=1.15)
    draw_bat_ball(d, 480, 832, 42)
    text_block(d, 376, 872,
               "New Zealand 243/5 at stumps on day one of the first Test.",
               SANS(16), INK, max_w=272, leading=1.25)
    # AI / business
    panel(d, [680, 714, 996, 940], fill=(255, 255, 255))
    text_block(d, 696, 726, "TECH  •  BUSINESS", SANS_B(19), RED, max_w=284)
    text_block(d, 696, 750,
               "ANTHROPIC 'WORTH $1.5 TRILLION'",
               SERIF_B(22), INK, max_w=284, leading=1.15)
    draw_chip(d, 838, 826, 30)
    text_block(d, 696, 872,
               "AI firm said to hit a $1.5 trillion valuation as the AI boom "
               "climbs.",
               SANS(16), INK, max_w=284, leading=1.25)

    # ---------- footer ----------
    d.line([40, 956, W - 40, 956], fill=INK, width=2)
    text_block(d, 0, 966,
               "ALSO TODAY: World Children's Day  •  APEC leaders meet in Shenzhen  •  "
               "Fiji declares a disaster over drought",
               SANS_B(15), GREY, max_w=W, align="center")
    text_block(d, 0, 990,
               "Drawn from the news reported on Friday 20 November 2026.",
               SANS(13), GREY, max_w=W, align="center")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
