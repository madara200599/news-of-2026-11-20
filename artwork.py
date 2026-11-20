#!/usr/bin/env python3
"""Draw the front page of 20 November 2026 as a 1024x1024 PNG.

Standard library only: the page is rasterised into an in-memory RGB
buffer with a small hand-drawn 5x7 bitmap font, then encoded as a PNG
with zlib/struct. No Pillow, no font files, no network; the output is
fully deterministic. Run: python3 artwork.py -> entry.png
"""

import math
import struct
import zlib

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (198, 148, 40)
GREY = (90, 86, 76)
SKY = (214, 230, 240)
SEA = (46, 110, 160)
WHITE = (255, 255, 255)
GREEN = (96, 160, 90)
CREAM = (232, 222, 196)
TAN = (210, 180, 130)
BROWN = (120, 80, 40)
YELLOW = (255, 196, 0)

# ---------------------------------------------------------------------------
# 5x7 bitmap font. Each glyph is 7 rows of 5 pixels, '#' = ink.
# ---------------------------------------------------------------------------

FONT = {
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#.#.#", "#..##", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "a": (".....", ".....", ".####", "....#", ".####", "#...#", ".####"),
    "b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    "c": (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
    "d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    "e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".####"),
    "f": ("..##.", ".#...", ".#...", "####.", ".#...", ".#...", ".#..."),
    "g": (".....", ".....", ".####", "#...#", ".####", "....#", ".###."),
    "h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    "j": ("...#.", ".....", "..##.", "...#.", "...#.", "#..#.", ".##.."),
    "k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    "l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    "n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    "p": (".....", ".....", "####.", "#...#", "#...#", "####.", "#...."),
    "q": (".....", ".....", ".####", "#...#", "#...#", ".####", "...##"),
    "r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    "s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    "t": (".#...", ".#...", "####.", ".#...", ".#...", ".#..#", "..##."),
    "u": (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
    "v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "w": (".....", ".....", "#...#", "#...#", "#.#.#", "#.#.#", ".#.#."),
    "x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    "y": (".....", ".....", "#...#", "#...#", ".####", "....#", ".###."),
    "z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", ".####", ".....", ".....", "....."),
    "(": ("...#.", "..#..", "..#..", "..#..", "..#..", "..#..", "...#."),
    ")": (".#...", "..#..", "..#..", "..#..", "..#..", "..#..", ".#..."),
    "/": ("....#", "....#", "...#.", "..#..", "..#..", ".#...", ".#..."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "*": (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "+": (".....", "..#..", "..#..", ".####", "..#..", "..#..", "....."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "<": ("....#", "...#.", "..#..", ".#...", "..#..", "...#.", "....#"),
    ">": ("#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."),
    "[": ("..###", "..#..", "..#..", "..#..", "..#..", "..#..", "..###"),
    "]": ("###..", "..#..", "..#..", "..#..", "..#..", "..#..", "###.."),
    "|": ("..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    "@": (".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".####"),
    "^": ("..#..", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "~": (".....", ".....", ".#..#", "#.#.#", ".....", ".....", "....."),
    "`": ("..#..", "..#..", "...#.", ".....", ".....", ".....", "....."),
    "\\": ("#....", "#....", ".#...", "..#..", "..#..", "...#.", "....#"),
    "{": ("...##", "...#.", "...#.", ".##..", "...#.", "...#.", "...##"),
    "}": ("##...", ".#...", ".#...", "..##.", ".#...", ".#...", "##..."),
    "•": (".....", ".....", ".###.", ".###.", ".###.", ".....", "....."),
    "—": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
}

_FALLBACK = {"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "·": "•"}


def _glyph(ch):
    if ch in FONT:
        return FONT[ch]
    return FONT[_FALLBACK.get(ch, "?")]


# ---------------------------------------------------------------------------
# Canvas: an RGB pixel buffer with the drawing primitives the page needs.
# ---------------------------------------------------------------------------

class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(bytes(bg) * (w * h))

    def fill_rect(self, x0, y0, x1, y1, color):
        """Fill the inclusive rectangle (x0, y0)-(x1, y1), clipped."""
        x0 = max(0, int(x0))
        y0 = max(0, int(y0))
        x1 = min(self.w - 1, int(x1))
        y1 = min(self.h - 1, int(y1))
        if x1 < x0 or y1 < y0:
            return
        row = bytes(color) * (x1 - x0 + 1)
        n = len(row)
        for yy in range(y0, y1 + 1):
            i = (yy * self.w + x0) * 3
            self.buf[i:i + n] = row

    def rect(self, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = (int(v) for v in box)
        if fill is not None:
            self.fill_rect(x0, y0, x1, y1, fill)
        if outline is not None:
            self.fill_rect(x0, y0, x1, y0 + width - 1, outline)
            self.fill_rect(x0, y1 - width + 1, x1, y1, outline)
            self.fill_rect(x0, y0, x0 + width - 1, y1, outline)
            self.fill_rect(x1 - width + 1, y0, x1, y1, outline)

    def line(self, x0, y0, x1, y1, color, width=1):
        """Bresenham line with a square brush of the given width."""
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        r = width // 2
        while True:
            self.fill_rect(x0 - r, y0 - r, x0 - r + width - 1,
                           y0 - r + width - 1, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def ellipse(self, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = (float(v) for v in box)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        if rx <= 0 or ry <= 0:
            return
        if fill is not None:
            top = int(math.floor(cy - ry))
            bot = int(math.ceil(cy + ry))
            for yy in range(top, bot + 1):
                t = (yy - cy) / ry
                if abs(t) > 1:
                    continue
                dx = rx * math.sqrt(1 - t * t)
                self.fill_rect(cx - dx, yy, cx + dx, yy, fill)
        if outline is not None:
            steps = max(24, int(2 * math.pi * max(rx, ry)) + 1)
            prev = None
            for i in range(steps + 1):
                a = 2 * math.pi * i / steps
                p = (cx + rx * math.cos(a), cy + ry * math.sin(a))
                if prev is not None:
                    self.line(prev[0], prev[1], p[0], p[1], outline, width)
                prev = p

    def arc(self, box, start, end, color, width=1):
        """Arc in degrees, PIL-style: 0 at 3 o'clock, growing clockwise."""
        x0, y0, x1, y1 = (float(v) for v in box)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        steps = max(8, int(abs(end - start) * max(rx, ry) / 2) + 1)
        prev = None
        for i in range(steps + 1):
            a = math.radians(start + (end - start) * i / steps)
            p = (cx + rx * math.cos(a), cy + ry * math.sin(a))
            if prev is not None:
                self.line(prev[0], prev[1], p[0], p[1], color, width)
            prev = p

    def polygon(self, pts, fill=None, outline=None, width=1):
        if fill is not None:
            ys = [p[1] for p in pts]
            n = len(pts)
            for yy in range(int(math.floor(min(ys))),
                            int(math.ceil(max(ys))) + 1):
                yc = yy + 0.5
                xs = []
                for i in range(n):
                    ax, ay = pts[i]
                    bx, by = pts[(i + 1) % n]
                    if (ay <= yc < by) or (by <= yc < ay):
                        xs.append(ax + (yc - ay) * (bx - ax) / (by - ay))
                xs.sort()
                for i in range(0, len(xs) - 1, 2):
                    self.fill_rect(xs[i], yy, xs[i + 1], yy, fill)
        if outline is not None:
            n = len(pts)
            for i in range(n):
                ax, ay = pts[i]
                bx, by = pts[(i + 1) % n]
                self.line(ax, ay, bx, by, outline, width)

    def rounded_rect(self, box, radius, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = (int(v) for v in box)
        r = int(radius)
        if fill is not None:
            self.fill_rect(x0 + r, y0, x1 - r, y1, fill)
            self.fill_rect(x0, y0 + r, x0 + r - 1, y1 - r, fill)
            self.fill_rect(x1 - r + 1, y0 + r, x1, y1 - r, fill)
            for ccx, ccy in ((x0 + r, y0 + r), (x1 - r, y0 + r),
                             (x0 + r, y1 - r), (x1 - r, y1 - r)):
                self.ellipse([ccx - r, ccy - r, ccx + r, ccy + r], fill=fill)
        if outline is not None:
            self.line(x0 + r, y0, x1 - r, y0, outline, width)
            self.line(x0 + r, y1, x1 - r, y1, outline, width)
            self.line(x0, y0 + r, x0, y1 - r, outline, width)
            self.line(x1, y0 + r, x1, y1 - r, outline, width)
            self.arc([x0, y0, x0 + 2 * r, y0 + 2 * r], 180, 270,
                     outline, width)
            self.arc([x1 - 2 * r, y0, x1, y0 + 2 * r], 270, 360,
                     outline, width)
            self.arc([x1 - 2 * r, y1 - 2 * r, x1, y1], 0, 90,
                     outline, width)
            self.arc([x0, y1 - 2 * r, x0 + 2 * r, y1], 90, 180,
                     outline, width)


def png_bytes(cv):
    """Encode a Canvas as PNG bytes (filter 0 rows, zlib level 9)."""
    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    stride = cv.w * 3
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.buf[yy * stride:(yy + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))


# ---------------------------------------------------------------------------
# Text: the 5x7 font at integer scales. A nominal size N maps to a scale
# of about N/10, so glyphs stand about 0.7*N px tall, like a text font.
# ---------------------------------------------------------------------------

def scale_for(size):
    return max(1, int(size / 10 + 0.5))


def text_size(text, size, bold=False):
    s = scale_for(size)
    if not text:
        return 0
    w = (len(text) * 6 - 1) * s
    if bold:
        w += max(1, s // 2)
    return w


def draw_text(cv, x, y, text, size, color, bold=False):
    s = scale_for(size)
    extra = max(1, s // 2) if bold else 0
    cx = int(x)
    top = int(y)
    for ch in text:
        glyph = _glyph(ch)
        for r, row in enumerate(glyph):
            for c, bit in enumerate(row):
                if bit == "#":
                    gx = cx + c * s
                    gy = top + r * s
                    cv.fill_rect(gx, gy, gx + s - 1, gy + s - 1, color)
                    if extra:
                        cv.fill_rect(gx + extra, gy, gx + extra + s - 1,
                                     gy + s - 1, color)
        cx += 6 * s
    return cx


def wrap(text, size, bold, max_w):
    """Greedy word wrap into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_size(trial, size, bold) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(cv, x, y, text, size, color, bold=False, max_w=None,
               leading=1.25, align="left"):
    """Draw wrapped text; return y just below the last line."""
    lines = wrap(text, size, bold, max_w) if max_w else [text]
    lh = int(size * leading)
    for line in lines:
        if align == "center":
            lx = x + (max_w - text_size(line, size, bold)) // 2
        else:
            lx = x
        draw_text(cv, lx, y, line, size, color, bold)
        y += lh
    return y


# ---------------------------------------------------------------------------
# Pictures
# ---------------------------------------------------------------------------

def panel(cv, box, fill=WHITE):
    cv.rect(box, fill=fill, outline=INK, width=2)


def draw_star(cv, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    cv.polygon(pts, fill=fill)


def flag_us(cv, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        c = RED if i % 2 == 0 else WHITE
        cv.fill_rect(x, y + i * stripe, x + w, y + (i + 1) * stripe - 1, c)
    cw, ch = w * 0.4, stripe * 7
    cv.fill_rect(x, y, x + cw, y + ch, (28, 48, 96))
    for r in range(4):
        for c_ in range(5):
            px = x + 8 + c_ * (cw - 14) / 4
            py = y + 6 + r * (ch - 12) / 3
            cv.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)


def flag_cn(cv, x, y, w, h):
    cv.fill_rect(x, y, x + w, y + h, (222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.28
    draw_star(cv, cx, cy, h * 0.16, (255, 222, 0))
    for sx, sy in [(0.42, 0.14), (0.52, 0.28), (0.52, 0.48), (0.42, 0.62)]:
        draw_star(cv, x + w * sx, y + h * sy, h * 0.06, (255, 222, 0))


def flag_ru(cv, x, y, w, h):
    for i, c in enumerate([WHITE, (0, 57, 166), (213, 0, 50)]):
        cv.fill_rect(x, y + i * h / 3, x + w, y + (i + 1) * h / 3 - 1, c)


def draw_globe(cv, cx, cy, r):
    cv.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=INK,
               width=3)
    for k in (-2, -1, 1, 2):
        off = k * r / 3
        hw = abs(off) * 0.55
        cv.ellipse([cx - hw, cy - r, cx + hw, cy + r], outline=SEA, width=2)
    cv.line(cx - r, cy - r * 0.25, cx + r, cy - r * 0.25, SEA, 2)
    cv.line(cx - r, cy + r * 0.35, cx + r, cy + r * 0.35, SEA, 2)
    cv.ellipse([cx - r * 0.7, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
               fill=GREEN)
    cv.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.65, cy + r * 0.6],
               fill=GREEN)


def draw_cyclone(cv, cx, cy, r):
    for turn in range(3):
        prev = None
        for a in range(0, 300):
            ang = math.radians(a + turn * 90)
            rr = r * (0.15 + 0.85 * a / 300)
            p = (cx + rr * math.cos(ang), cy + rr * math.sin(ang))
            if prev is not None:
                cv.line(prev[0], prev[1], p[0], p[1], SEA, 5)
            prev = p
    cv.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=WHITE, outline=INK,
               width=2)
    for dx in (-r * 0.9, -r * 0.5, 0, r * 0.5, r * 0.9):
        cv.line(cx + dx, cy + r * 0.75, cx + dx - 6, cy + r * 1.05, SEA, 3)


def draw_scales(cv, cx, cy, s):
    cv.line(cx, cy - s, cx, cy + s, INK, 4)
    cv.line(cx - s * 0.9, cy - s * 0.7, cx + s * 0.9, cy - s * 0.7, INK, 4)
    cv.ellipse([cx - 6, cy - s - 8, cx + 6, cy - s + 8], fill=GOLD,
               outline=INK, width=2)
    for side in (-1, 1):
        px = cx + side * s * 0.9
        cv.line(px, cy - s * 0.7, px, cy - s * 0.1, INK, 3)
        cv.polygon([(px - s * 0.45, cy - s * 0.1),
                    (px + s * 0.45, cy - s * 0.1),
                    (px, cy + s * 0.35)], fill=GOLD, outline=INK)
    cv.line(cx - s * 0.55, cy + s, cx + s * 0.55, cy + s, INK, 5)


def draw_embassy(cv, x, y, w, h):
    cv.rect([x, y, x + w, y + h], fill=CREAM, outline=INK, width=2)
    cv.polygon([(x - 4, y), (x + w / 2, y - h * 0.22), (x + w + 4, y)],
               fill=RED, outline=INK)
    for i in range(4):
        ccx = x + w * (0.18 + i * 0.21)
        cv.fill_rect(ccx - 5, y + h * 0.18, ccx + 5, y + h * 0.8, INK)
    cv.fill_rect(x, y + h * 0.82, x + w, y + h, INK)
    bx, by, br = x + w * 0.85, y + h * 0.1, h * 0.35
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = br if i % 2 == 0 else br * 0.45
        pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    cv.polygon(pts, fill=YELLOW, outline=RED)


def draw_bat_ball(cv, cx, cy, r):
    cv.rounded_rect([cx - r * 0.55, cy - r * 0.35, cx + r * 0.15,
                     cy + r * 0.9], 8, fill=TAN, outline=INK, width=2)
    cv.fill_rect(cx - r * 0.18, cy - r * 0.9, cx - r * 0.02, cy - r * 0.3,
                 BROWN)
    cv.ellipse([cx + r * 0.35, cy - r * 0.75, cx + r * 0.95, cy - r * 0.15],
               fill=RED, outline=INK, width=2)
    cv.arc([cx + r * 0.35, cy - r * 0.75, cx + r * 0.95, cy - r * 0.15],
           200, 340, WHITE, 2)


def draw_chip(cv, cx, cy, s):
    cv.fill_rect(cx - s, cy - s, cx + s, cy + s, INK)
    cv.rect([cx - s * 0.6, cy - s * 0.6, cx + s * 0.6, cy + s * 0.6],
            fill=(60, 200, 160), outline=WHITE, width=2)
    for i in range(5):
        off = -s + i * (2 * s / 4)
        cv.line(cx + off, cy - s - 12, cx + off, cy - s, INK, 3)
        cv.line(cx + off, cy + s, cx + off, cy + s + 12, INK, 3)
        cv.line(cx - s - 12, cy + off, cx - s, cy + off, INK, 3)
        cv.line(cx + s, cy + off, cx + s + 12, cy + off, INK, 3)


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------

def draw_page():
    cv = Canvas(W, H, PAPER)

    # outer frame
    cv.rect([6, 6, W - 7, H - 7], outline=INK, width=4)
    cv.rect([14, 14, W - 15, H - 15], outline=INK, width=1)

    # ---------- masthead ----------
    text_block(cv, 0, 30, "THE WORLD TODAY", 66, INK, bold=True,
               max_w=W, align="center")
    cv.line(40, 108, W - 40, 108, INK, 3)
    text_block(cv, 0, 118, "FRIDAY  •  20 NOVEMBER 2026", 34, RED,
               bold=True, max_w=W, align="center")
    cv.line(40, 158, W - 40, 158, INK, 2)
    text_block(cv, 0, 166,
               "ONE DAY, ONE PAGE — THE WORLD'S NEWS, AS REPORTED TODAY",
               17, GREY, bold=True, max_w=W, align="center")

    # ---------- lead story ----------
    panel(cv, [28, 196, 996, 470])
    text_block(cv, 48, 210, "THE THREE-POWER SUMMIT", 20, RED, bold=True,
               max_w=640)
    text_block(cv, 48, 236, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
               40, INK, bold=True, max_w=660, leading=1.1)
    text_block(cv, 48, 330,
               "First-ever three-way talks in China end with a joint peace "
               "declaration: nuclear arms control, energy security and the "
               "war in Ukraine on the table at the APEC summit.",
               21, INK, max_w=620, leading=1.3)
    flag_us(cv, 700, 218, 120, 64)
    flag_cn(cv, 836, 218, 120, 64)
    flag_ru(cv, 700, 296, 120, 64)
    draw_text(cv, 700, 372, "APEC  •  SHENZHEN, CHINA", 15, GREY, bold=True)
    draw_globe(cv, 880, 432, 34)

    # ---------- middle row: cyclone + ICJ ----------
    panel(cv, [28, 484, 500, 700])
    text_block(cv, 48, 498, "CYCLONE AKVAN", 22, BLUE, bold=True, max_w=300)
    text_block(cv, 48, 526, "Storm makes landfall on India's east coast",
               24, INK, bold=True, max_w=300, leading=1.15)
    text_block(cv, 48, 596,
               "80,000 people evacuated in Odisha; schools shut, trains "
               "cancelled as heavy rain begins.",
               18, INK, max_w=290, leading=1.3)
    draw_cyclone(cv, 410, 585, 62)

    panel(cv, [516, 484, 996, 700])
    text_block(cv, 536, 498, "WORLD COURT  •  THE HAGUE", 22, BLUE,
               bold=True, max_w=440)
    text_block(cv, 536, 526, "MYANMAR GUILTY OF GENOCIDE",
               26, INK, bold=True, max_w=440, leading=1.15)
    text_block(cv, 536, 590,
               "The ICJ rules Myanmar committed genocide against the "
               "Rohingya in 2017 — a first for the court.",
               18, INK, max_w=300, leading=1.3)
    draw_scales(cv, 905, 600, 55)

    # ---------- bottom row: Kyiv, cricket, AI ----------
    panel(cv, [28, 714, 344, 940])
    text_block(cv, 44, 726, "KYIV UNDER FIRE", 19, RED, bold=True, max_w=290)
    text_block(cv, 44, 750, "Russian drones hit two embassies",
               22, INK, bold=True, max_w=288, leading=1.15)
    draw_embassy(cv, 70, 812, 200, 50)
    text_block(cv, 44, 872,
               "One killed; two embassies damaged, cathedral windows "
               "shattered.",
               16, INK, max_w=288, leading=1.25)

    panel(cv, [360, 714, 664, 940])
    text_block(cv, 376, 726, "CRICKET  •  WELLINGTON", 19, RED, bold=True,
               max_w=272)
    text_block(cv, 376, 750, "NICHOLLS 113* LIFTS NZ",
               22, INK, bold=True, max_w=272, leading=1.15)
    draw_bat_ball(cv, 480, 832, 42)
    text_block(cv, 376, 872,
               "New Zealand 243/5 at stumps on day one of the first Test.",
               16, INK, max_w=272, leading=1.25)

    panel(cv, [680, 714, 996, 940])
    text_block(cv, 696, 726, "TECH  •  BUSINESS", 19, RED, bold=True,
               max_w=284)
    text_block(cv, 696, 750, "ANTHROPIC 'WORTH $1.5 TRILLION'",
               22, INK, bold=True, max_w=284, leading=1.15)
    draw_chip(cv, 838, 826, 30)
    text_block(cv, 696, 872,
               "AI firm said to hit a $1.5 trillion valuation as the AI "
               "boom climbs.",
               16, INK, max_w=284, leading=1.25)

    # ---------- footer ----------
    cv.line(40, 956, W - 40, 956, INK, 2)
    text_block(cv, 0, 968,
               "ALSO TODAY: World Children's Day  •  APEC leaders meet in "
               "Shenzhen  •  Fiji declares a disaster over drought",
               13, GREY, bold=True, max_w=W, align="center")
    text_block(cv, 0, 988,
               "Drawn from the news reported on Friday 20 November 2026.",
               12, GREY, max_w=W, align="center")

    return cv


def render_png():
    return png_bytes(draw_page())


def main():
    with open(OUT, "wb") as fh:
        fh.write(render_png())
    print("wrote", OUT)


if __name__ == "__main__":
    main()
