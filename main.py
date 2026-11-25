#!/usr/bin/env python3
"""THE WORLD TODAY -- a one-page newspaper front page for
Wednesday, 25 November 2026, drawn entirely by hand in pure Python.

Only the Python standard library is used. The PNG file is assembled
byte by byte (signature, IHDR, IDAT and IEND chunks, each with a
CRC32 checksum), and every letter comes from a small 5x7 bitmap
alphabet defined in this file. No images are loaded, no network is
used, no clock and no randomness: run it twice and the bytes match.

Usage:
    MAKEFUN_OUTPUT_DIR=/some/dir python3 main.py
    (defaults to ./output ; writes entry.png there)
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---- palette ---------------------------------------------------------
CREAM = (250, 244, 230)
INK = (28, 28, 32)
RED = (176, 32, 32)
BLUE = (28, 66, 138)
NAVY = (16, 26, 64)
GREY = (96, 90, 80)
LIGHTGREY = (178, 172, 160)
WHITE = (255, 255, 255)
SILVER = (205, 205, 210)
DARK = (60, 60, 66)
GOLD = (214, 178, 90)
SKYBLUE = (96, 142, 202)
EARTH = (46, 104, 178)
EARTH2 = (70, 140, 200)
ORANGE = (232, 110, 30)
YELLOW = (245, 200, 60)
SMOKE = (198, 192, 182)
PANELBLUE = (40, 80, 160)
GREEN = (120, 220, 130)
LIGHTRED = (255, 120, 110)

# ---- 5x7 bitmap alphabet (each glyph: 7 rows of 5 on/off cells) -----
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
}

# ---- canvas ----------------------------------------------------------
canvas = bytearray(W * H * 3)
_clip = None  # optional clip box (x0, y0, x1, y1); None means the page


def fill_rect(x, y, w, h, color):
    """Fill an axis-aligned rectangle, clipped to the page and to
    the active clip box, if one is set."""
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if _clip is not None:
        cx0, cy0, cx1, cy1 = _clip
        x0 = max(x0, cx0)
        y0 = max(y0, cy0)
        x1 = min(x1, cx1)
        y1 = min(y1, cy1)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        canvas[i:i + len(row)] = row


def fill_circle(cx, cy, r, color):
    """Fill a disc of radius r centred on (cx, cy)."""
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)


def fill_triangle(x0, y0, x1, y1, x2, y2, color):
    """Fill a triangle by scanning its rows between two edges."""
    pts = sorted(((x0, y0), (x1, y1), (x2, y2)), key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts

    def edge_x(xa, ya, xb, yb, y):
        if yb == ya:
            return float(xa)
        return xa + (xb - xa) * (y - ya) / (yb - ya)

    for y in range(ay, cy + 1):
        if y < by:
            xa = edge_x(ax, ay, bx, by, y)
        else:
            xa = edge_x(bx, by, cx, cy, y)
        xb = edge_x(ax, ay, cx, cy, y)
        if xa > xb:
            xa, xb = xb, xa
        fill_rect(int(xa), y, int(xb) - int(xa) + 1, 1, color)


def rect_outline(x, y, w, h, color, thick=1):
    fill_rect(x, y, w, thick, color)
    fill_rect(x, y + h - thick, w, thick, color)
    fill_rect(x, y, thick, h, color)
    fill_rect(x + w - thick, y, thick, h, color)


# ---- text ------------------------------------------------------------
def text_width(s, scale):
    s = s.upper()
    if not s:
        return 0
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, color):
    """Draw a string with the bitmap alphabet at (x, y)."""
    s = s.upper()
    for ci, ch in enumerate(s):
        glyph = FONT.get(ch, FONT[" "])
        bx = x + ci * 6 * scale
        for r in range(7):
            row = glyph[r]
            for c in range(5):
                if row[c] == "1":
                    fill_rect(bx + c * scale, y + r * scale,
                              scale, scale, color)


def draw_text_centred(cx, y, s, scale, color):
    draw_text(cx - text_width(s, scale) // 2, y, s, scale, color)


def wrap(text, scale, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines = []
    cur = ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(x, y, text, scale, color, max_w, lh):
    """Draw a wrapped paragraph; returns the y just below it."""
    for i, line in enumerate(wrap(text, scale, max_w)):
        draw_text(x, y + i * lh, line, scale, color)
    return y + len(wrap(text, scale, max_w)) * lh


# ---- the front page --------------------------------------------------
MX = 28          # left margin
RX = 996         # right edge


def draw_masthead():
    draw_text_centred(W // 2, 26, "THE WORLD TODAY", 8, INK)
    fill_rect(MX, 88, RX - MX, 4, RED)
    draw_text(MX, 100, "EST. 2026", 2, GREY)
    draw_text_centred(W // 2, 100, "WEDNESDAY, 25 NOVEMBER 2026", 2, INK)
    draw_text(RX - text_width("PRICE: FREE", 2), 100, "PRICE: FREE", 2, GREY)
    fill_rect(MX, 120, RX - MX, 2, INK)


def draw_lead_art():
    """Rocket and space station over the Earth, drawn from shapes.

    Everything is drawn inside a clip box equal to the panel, so the
    big Earth disc cannot spill over the stories below the panel.
    """
    global _clip
    x0, y0, x1, y1 = 560, 254, 996, 470
    _clip = (x0, y0, x1, y1)
    fill_rect(x0, y0, x1 - x0, y1 - y0, NAVY)
    stars = [
        (575, 268), (610, 262), (660, 275), (700, 262), (760, 270),
        (820, 262), (880, 272), (940, 264), (975, 290), (600, 300),
        (680, 320), (740, 330), (860, 340), (920, 330), (970, 360),
        (590, 380), (650, 400), (720, 380), (800, 400), (900, 390),
        (960, 410), (620, 440), (700, 450), (850, 440),
    ]
    for sx, sy in stars:
        fill_rect(sx, sy, 2, 2, WHITE)
    # Earth rising at the bottom of the panel.
    fill_circle(778, 648, 248, EARTH)
    fill_circle(700, 455, 34, EARTH2)
    fill_circle(860, 445, 26, EARTH2)
    fill_circle(790, 420, 18, EARTH2)
    fill_circle(740, 468, 12, (120, 170, 220))
    fill_circle(830, 465, 10, (120, 170, 220))
    # Tiangong station: silver modules, blue solar wings, gold dish.
    fill_rect(648, 292, 76, 16, PANELBLUE)
    fill_rect(908, 292, 76, 16, PANELBLUE)
    for gx in range(660, 724, 12):
        fill_rect(gx, 292, 1, 16, NAVY)
    for gx in range(920, 984, 12):
        fill_rect(gx, 292, 1, 16, NAVY)
    fill_rect(730, 284, 172, 32, SILVER)
    rect_outline(730, 284, 172, 32, DARK, 1)
    fill_circle(730, 300, 14, SILVER)
    fill_circle(902, 300, 14, SILVER)
    fill_rect(800, 268, 32, 16, SILVER)
    fill_circle(816, 262, 7, GOLD)
    fill_circle(760, 300, 3, BLUE)
    fill_circle(816, 300, 3, BLUE)
    fill_circle(872, 300, 3, BLUE)
    # Shenzhou-24 rocket, climbing on a tongue of flame.
    fill_circle(580, 462, 9, SMOKE)
    fill_circle(640, 464, 8, SMOKE)
    fill_circle(609, 468, 7, SMOKE)
    fill_triangle(596, 448, 622, 448, 609, 470, ORANGE)
    fill_triangle(601, 448, 617, 448, 609, 466, YELLOW)
    fill_triangle(592, 400, 592, 448, 574, 448, RED)
    fill_triangle(626, 400, 626, 448, 644, 448, RED)
    fill_rect(592, 320, 34, 100, WHITE)
    rect_outline(592, 320, 34, 100, DARK, 1)
    fill_triangle(592, 320, 626, 320, 609, 288, RED)
    fill_circle(609, 348, 8, DARK)
    fill_circle(609, 348, 7, SKYBLUE)
    fill_rect(592, 392, 34, 8, RED)
    _clip = None
    rect_outline(x0, y0, x1 - x0, y1 - y0, INK, 2)


def draw_lead():
    draw_text(MX, 134, "SPACE - FIRST FOREIGN ASTRONAUT ABOARD TIANGONG",
              2, RED)
    draw_text(MX, 158, "PAKISTAN'S FIRST", 5, INK)
    draw_text(MX, 198, "ASTRONAUT IN ORBIT", 5, RED)
    fill_rect(MX, 242, RX - MX, 2, INK)
    draw_para(MX, 254,
              "Muhammad Zeeshan Ali, 40, lifts off aboard China's "
              "Shenzhou-24 for Tiangong.",
              2, BLUE, 512, 16)
    draw_para(MX, 294,
              "Pakistan Air Force pilot Muhammad Zeeshan Ali, 40, "
              "launched at 05:18 Pakistan time aboard China's "
              "Shenzhou-24, bound for the Tiangong space station. "
              "He is the first Pakistani to orbit Earth and the "
              "first foreign astronaut aboard Tiangong. He will "
              "spend about a week in orbit running four Pakistani "
              "biotechnology experiments.",
              2, INK, 512, 16)
    # Fact box: launch time, time in orbit, experiments.
    stats = [("05:18", "LAUNCH TIME"),
             ("7 DAYS", "IN ORBIT"),
             ("4", "EXPERIMENTS")]
    for i, (num, label) in enumerate(stats):
        sx = MX + i * 175
        draw_text(sx, 432, num, 3, RED)
        draw_text(sx, 457, label, 2, GREY)
    draw_lead_art()


def draw_story(x, y, headline, body, max_w):
    """Headline + body in one column; returns y below the story."""
    y = draw_para(x, y, headline, 3, INK, max_w, 26)
    y += 6
    y = draw_para(x, y, body, 2, INK, max_w, 16)
    return y


def draw_middle():
    fill_rect(MX, 480, RX - MX, 2, INK)
    draw_story(MX, 494, "CIA HIT BY CYBER ATTACK",
               "US intelligence agencies appear to have been hit by "
               "a cyber attack touching classified information, CNN "
               "reports. It is the latest in a string of cyber "
               "incidents against the US government, and sources say "
               "it is unrelated to the attack on the FBI criminal "
               "database.",
               468)
    draw_story(528, 494, "HUAWEI GUILTY ON 10 OF 12 COUNTS",
               "A US jury on 24 November found Huawei guilty of 10 "
               "of 12 criminal charges, including bank fraud, "
               "conspiracy to steal trade secrets and conspiracy to "
               "defraud the US government, after a three-month "
               "trial in New York. Huawei rejects the verdict.",
               468)
    fill_rect(512, 494, 1, 154, LIGHTGREY)
    fill_rect(MX, 658, RX - MX, 2, INK)
    draw_story(MX, 672, "30 HOSTAGES HELD IN CARTAGENA",
               "Gunmen seized a supermarket in Cartagena, Colombia, "
               "after a failed raid on an armoured truck. At least "
               "30 people are held hostage and five elderly women "
               "have been freed, President Abelardo De La Espriella "
               "said.",
               468)
    draw_story(528, 672, "AI STOCKS TUMBLE",
               "The AI trade collapsed: the Nasdaq fell 1.5 percent, "
               "the S and P 500 0.5 percent, Nvidia about 6 percent "
               "and Micron 11 percent, while the Dow rose 0.8 "
               "percent. Selling worsened on reports of higher "
               "Trump tariffs.",
               468)
    fill_rect(512, 672, 1, 154, LIGHTGREY)
    fill_rect(MX, 836, RX - MX, 2, INK)


def draw_brief():
    draw_text(MX, 848, "IN BRIEF", 3, RED)
    items = [
        ("KYIV ADMITS DRONE STRIKE", "Zelenskiy confirms attack"),
        ("HOUTHI STRIKE HITS RIYADH", "Eleven hurt at top tower"),
        ("EBOLA: WHO PULLS STAFF OUT", "5,775 dead in DR Congo"),
        ("SEOUL MINISTER QUITS", "Choi Kyo-jin resigns"),
        ("QUAKE SHAKES NEPAL", "5.6 hits Koshi province"),
        ("SARKOZY TO STAND TRIAL", "Case set for 1 April 2027"),
        ("TURKEYS PARDONED", "Trump spares two turkeys"),
        ("PYONGYANG THREATENS SWISS", "Kim Yo-jong hits back"),
        ("NATO VOWS SPACE DEFENCE", "Russia arms a satellite"),
    ]
    cols = (MX, 356, 684)
    for i, (head, sub) in enumerate(items):
        cx = cols[i % 3]
        cy = 876 + (i // 3) * 32
        draw_text(cx, cy, head, 2, INK)
        draw_text(cx, cy + 15, sub, 2, GREY)


def draw_markets():
    fill_rect(MX, 972, RX - MX, 28, NAVY)
    segments = [
        ("NASDAQ -1.5%   ", LIGHTRED),
        ("S&P 500 -0.5%   ", LIGHTRED),
        ("NVIDIA -6%   ", LIGHTRED),
        ("MICRON -11%   ", LIGHTRED),
        ("DOW +0.8%   ", GREEN),
        ("PHLX -8%", LIGHTRED),
    ]
    total = sum(text_width(t, 2) for t, _ in segments)
    x = (W - total) // 2
    for text, color in segments:
        draw_text(x, 979, text, 2, color)
        x += text_width(text, 2)


def draw_footer():
    draw_text_centred(W // 2, 1004,
                      "Sources: Reuters, AP, CNN and other wire services.",
                      2, GREY)


def draw_page():
    fill_rect(0, 0, W, H, CREAM)
    draw_masthead()
    draw_lead()
    draw_middle()
    draw_brief()
    draw_markets()
    draw_footer()


# ---- PNG encoding (hand-built, standard library only) ----------------
def png_chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png():
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        raw += canvas[y * W * 3:(y + 1) * W * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", ihdr)
    png += png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += png_chunk(b"IEND", b"")
    return png


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    draw_page()
    data = encode_png()
    with open(path, "wb") as f:
        f.write(data)
    print("Wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
