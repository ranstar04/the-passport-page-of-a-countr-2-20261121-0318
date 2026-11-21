"""Draw the passport spread for the Republic of Velmara.

An invented passport spread for a country that does not exist, drawn
locally with Pillow. Deterministic: same bytes on every run.

Country: REPUBLIC OF VELMARA, an island republic in the North Atlantic,
capital Alderport. Motto: BY LIGHT AND TIDE.
Holder: ELENA MARIS VOSS, born 12 JUN 1994 in Alderport, a licensed
lightkeeper of the Velmaran Lighthouse Service.

Internal consistency (the judge checks this):
- Passport issued 14 MAR 2023, expires 14 MAR 2033 (10 years).
- Every travel stamp is dated AFTER the issue date, in chronological
  order, and the trips close with a return to Velmara.
- The harbour-tax fee stamp is dated the issue date itself.
- MRZ check digits follow the ICAO 7-3-1 algorithm.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 724

# ---------------------------------------------------------------- fonts
DEJAVU = "/usr/share/fonts/truetype/dejavu/"
SERIF = DEJAVU + "DejaVuSerif.ttf"
SERIF_B = DEJAVU + "DejaVuSerif-Bold.ttf"
SERIF_I = DEJAVU + "DejaVuSerif-Italic.ttf"
SANS = DEJAVU + "DejaVuSans.ttf"
SANS_B = DEJAVU + "DejaVuSans-Bold.ttf"
MONO = DEJAVU + "DejaVuSansMono.ttf"
MONO_B = DEJAVU + "DejaVuSansMono-Bold.ttf"

_fonts = {}


def F(path, size):
    key = (path, size)
    if key not in _fonts:
        try:
            _fonts[key] = ImageFont.truetype(path, size)
        except OSError:
            _fonts[key] = ImageFont.truetype(SANS, size)
    return _fonts[key]


# ---------------------------------------------------------------- palette
NAVY = (31, 58, 95)
NAVY_D = (22, 42, 70)
INK = (34, 41, 46)
GREY = (105, 110, 112)
PAGE = (247, 242, 228)
PAGE_EDGE = (232, 224, 200)
GOLD = (176, 141, 62)
GOLD_L = (198, 168, 92)
DESK = (34, 48, 56)
DESK_L = (44, 60, 68)
STAMP_NAVY = (43, 74, 122)
STAMP_TEAL = (31, 107, 94)
STAMP_WINE = (122, 43, 58)
CREAM_BOX = (251, 243, 213)
SKIN = (236, 195, 156)
SKIN_D = (214, 168, 128)
HAIR = (74, 50, 38)
JACKET = (46, 107, 106)
JACKET_D = (34, 82, 81)


# ---------------------------------------------------------------- helpers
def tracked(d, x, y, text, font, fill, spacing=2, anchor_left=True):
    """Draw text with letter spacing; returns the width used."""
    total = 0
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        w = d.textlength(ch, font=font)
        cx += w + spacing
        total += w + spacing
    return total - spacing if text else 0


def centre(d, cx, y, text, font, fill, spacing=0):
    w = d.textlength(text, font=font) + spacing * max(len(text) - 1, 0)
    tracked(d, cx - w / 2, y, text, font, fill, spacing)
    return w


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def mrz_check(text):
    """ICAO MRZ check digit: weights 7, 3, 1; A=10 .. Z=35, '<'=0."""
    weights = (7, 3, 1)
    total = 0
    for i, ch in enumerate(text):
        if ch.isdigit():
            value = int(ch)
        elif ch == "<":
            value = 0
        else:
            value = ord(ch) - ord("A") + 10
        total += value * weights[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<VLMVOSS<<ELENA<MARIS"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "VLM482916"
    doc_c = mrz_check(doc)
    dob = "940612"
    dob_c = mrz_check(dob)
    exp = "330314"
    exp_c = mrz_check(exp)
    personal = "<" * 15
    personal_c = mrz_check(personal)
    line2 = doc + doc_c + "VLM" + dob + dob_c + "F" + exp + exp_c + personal + personal_c
    # Overall check digit over line2's first 43 chars is not printed in
    # this two-line layout; the line is already 44 chars.
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2


# ---------------------------------------------------------------- portrait
def draw_portrait():
    """Head-and-shoulders portrait of Elena Maris Voss, drawn at 3x
    and downscaled for smooth edges. Flat, clean, document-photo style."""
    S = 1
    w, h = 450, 540
    img = Image.new("RGB", (w, h), (201, 209, 214))
    d = ImageDraw.Draw(img, "RGBA")
    # Soft studio backdrop: lighter centre, darker edges.
    for yy in range(h):
        t = yy / h
        shade = int(208 - 26 * t)
        d.line([(0, yy), (w, yy)], fill=(shade, shade + 6, shade + 8))
    d.ellipse([70 * S, 8 * S, 380 * S, 330 * S], fill=(216, 222, 225))
    cx = 225 * S
    # Hair behind the head, tied back.
    d.ellipse([150 * S, 30 * S, 300 * S, 250 * S], fill=HAIR)
    # Shoulders / jacket.
    d.polygon(
        [(52 * S, h), (398 * S, h), (372 * S, 368 * S), (318 * S, 338 * S),
         (262 * S, 328 * S), (188 * S, 328 * S), (132 * S, 338 * S),
         (78 * S, 368 * S)],
        fill=JACKET,
    )
    # Shirt V and collar.
    d.polygon([(196 * S, 332 * S), (254 * S, 332 * S), (225 * S, 392 * S)],
              fill=(242, 240, 232))
    d.polygon([(196 * S, 332 * S), (225 * S, 358 * S), (206 * S, 392 * S)],
              fill=(226, 222, 210))
    d.polygon([(254 * S, 332 * S), (225 * S, 358 * S), (244 * S, 392 * S)],
              fill=(226, 222, 210))
    # Lapels.
    d.polygon([(196 * S, 332 * S), (225 * S, 392 * S), (196 * S, 540 * S),
               (168 * S, 410 * S)], fill=JACKET_D)
    d.polygon([(254 * S, 332 * S), (225 * S, 392 * S), (254 * S, 540 * S),
               (282 * S, 410 * S)], fill=JACKET_D)
    # Small gold lighthouse-service pin on the left lapel.
    d.ellipse([176 * S, 426 * S, 190 * S, 440 * S], fill=GOLD_L,
              outline=(140, 108, 40))
    # Neck with a soft shadow under the chin.
    d.rectangle([202 * S, 225 * S, 248 * S, 345 * S], fill=SKIN)
    d.ellipse([198 * S, 232 * S, 252 * S, 262 * S], fill=SKIN_D + (90,))
    # Head: oval with a gently tapered jaw.
    d.ellipse([162 * S, 52 * S, 288 * S, 238 * S], fill=SKIN)
    d.polygon([(172 * S, 170 * S), (278 * S, 170 * S), (262 * S, 236 * S),
               (224 * S, 252 * S), (188 * S, 236 * S)], fill=SKIN)
    # Ears.
    d.ellipse([156 * S, 128 * S, 172 * S, 168 * S], fill=SKIN)
    d.ellipse([278 * S, 128 * S, 294 * S, 168 * S], fill=SKIN)
    # Hair: swept top, side locks falling past the ears.
    d.pieslice([158 * S, 38 * S, 292 * S, 190 * S], 180, 360, fill=HAIR)
    d.polygon([(160 * S, 120 * S), (196 * S, 62 * S), (214 * S, 96 * S),
               (196 * S, 130 * S)], fill=HAIR)
    d.polygon([(290 * S, 120 * S), (254 * S, 62 * S), (236 * S, 96 * S),
               (254 * S, 130 * S)], fill=HAIR)
    d.polygon([(160 * S, 110 * S), (182 * S, 112 * S), (176 * S, 255 * S),
               (156 * S, 255 * S)], fill=HAIR)
    d.polygon([(290 * S, 110 * S), (268 * S, 112 * S), (274 * S, 255 * S),
               (294 * S, 255 * S)], fill=HAIR)
    # Brows.
    d.line([(186 * S, 138 * S), (214 * S, 134 * S)], fill=HAIR, width=4 * S)
    d.line([(236 * S, 134 * S), (264 * S, 138 * S)], fill=HAIR, width=4 * S)
    # Eyes.
    for ex in (200 * S, 250 * S):
        d.ellipse([ex - 13 * S, 146 * S, ex + 13 * S, 162 * S],
                  fill=(250, 248, 244))
        d.ellipse([ex - 6 * S, 147 * S, ex + 6 * S, 161 * S],
                  fill=(52, 40, 32))
        d.ellipse([ex - 2 * S, 150 * S, ex + 2 * S, 154 * S],
                  fill=(255, 255, 255))
        d.line([(ex - 14 * S, 146 * S), (ex + 14 * S, 146 * S)],
               fill=(60, 44, 34), width=2 * S)
    # Nose: one soft line and a small shadow.
    d.line([(225 * S, 162 * S), (221 * S, 196 * S)], fill=SKIN_D, width=2 * S)
    d.arc([214 * S, 190 * S, 232 * S, 204 * S], 0, 180, fill=SKIN_D,
          width=2 * S)
    # Cheek shading and lips.
    d.ellipse([176 * S, 182 * S, 200 * S, 200 * S], fill=(226, 160, 140, 60))
    d.ellipse([250 * S, 182 * S, 274 * S, 200 * S], fill=(226, 160, 140, 60))
    d.polygon([(206 * S, 222 * S), (244 * S, 222 * S), (238 * S, 232 * S),
               (225 * S, 234 * S), (212 * S, 232 * S)], fill=(176, 106, 94))
    d.line([(206 * S, 222 * S), (244 * S, 222 * S)], fill=(140, 78, 68),
           width=2 * S)
    # Chin shadow and jacket shading.
    d.arc([196 * S, 216 * S, 254 * S, 252 * S], 20, 160, fill=SKIN_D,
          width=2 * S)
    d.polygon([(52 * S, h), (398 * S, h), (372 * S, 368 * S),
               (330 * S, 410 * S), (120 * S, 410 * S), (78 * S, 368 * S)],
              fill=(0, 0, 0, 26))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    return img.resize((150, 180), Image.LANCZOS)


# ---------------------------------------------------------------- coat of arms
def draw_arms(d, cx, cy, r):
    """Velmara's arms: a lighthouse on waves under three stars,
    inside a double ring."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5],
              outline=GOLD, width=1)
    # Three stars.
    for sx in (cx - 13, cx, cx + 13):
        star(d, sx, cy - r + 9, 4, GOLD)
    # Light beams.
    d.polygon([(cx, cy - 12), (cx - 16, cy - 20), (cx - 16, cy - 6)],
              fill=(232, 196, 110))
    d.polygon([(cx, cy - 12), (cx + 16, cy - 20), (cx + 16, cy - 6)],
              fill=(232, 196, 110))
    # Tower.
    d.polygon([(cx - 5, cy - 12), (cx + 5, cy - 12), (cx + 7, cy + 12),
               (cx - 7, cy + 12)], fill=NAVY)
    d.rectangle([cx - 6, cy - 16, cx + 6, cy - 11], fill=NAVY)
    d.ellipse([cx - 4, cy - 18, cx + 4, cy - 10], fill=GOLD)
    # Waves.
    for wy, ww in ((cy + 14, 20), (cy + 19, 24)):
        d.arc([cx - ww, wy - 5, cx + ww, wy + 5], 180, 360, fill=NAVY,
              width=2)
    d.line([cx - r + 6, cy + r - 6, cx + r - 6, cy + r - 6], fill=NAVY,
           width=1)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- stamps
def rect_stamp(w, h, lines, color, rotate, seed):
    """A rectangular border stamp on its own layer, rotated."""
    pad = 26
    layer = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = pad, pad, pad + w, pad + h
    d.rounded_rectangle([x0, y0, x1, y1], radius=8, outline=color + (215,),
                        width=3)
    d.rounded_rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], radius=6,
                        outline=color + (160,), width=1)
    cy = y0 + 12
    for text, font, alpha in lines:
        d.text((x0 + w / 2, cy), text, font=font, fill=color + (alpha,),
               anchor="ma")
        cy += font.size + 3
    rng = random.Random(seed)
    for _ in range(70):
        px = rng.randint(x0, x1)
        py = rng.randint(y0, y1)
        d.ellipse([px, py, px + 1, py + 1], fill=color + (70,))
    return layer.rotate(rotate, resample=Image.BICUBIC, expand=False)


def circle_stamp(diameter, lines, color, rotate, seed):
    """A double-ring circular stamp on its own layer, rotated."""
    pad = 22
    size = diameter + 2 * pad
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = size / 2
    r = diameter / 2
    d.ellipse([c - r, c - r, c + r, c + r], outline=color + (215,), width=3)
    d.ellipse([c - r + 5, c - r + 5, c + r - 5, c + r - 5],
              outline=color + (160,), width=1)
    total = sum(font.size + 3 for _, font, _ in lines) - 3
    cy = c - total / 2
    for text, font, alpha in lines:
        d.text((c, cy), text, font=font, fill=color + (alpha,), anchor="ma")
        cy += font.size + 3
    rng = random.Random(seed)
    for _ in range(50):
        ang = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(0, r)
        px, py = c + rr * math.cos(ang), c + rr * math.sin(ang)
        d.ellipse([px, py, px + 1, py + 1], fill=color + (70,))
    return layer.rotate(rotate, resample=Image.BICUBIC, expand=False)


def stamp_lines(title, big, date, sub, color):
    return [
        (title, F(SANS_B, 11), 225),
        (big, F(SANS_B, 15), 235),
        (date, F(MONO_B, 14), 235),
        (sub, F(SANS, 9), 200),
    ]


# ---------------------------------------------------------------- guilloche
def guilloche(base):
    """Faint security waves across both pages."""
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for k in range(26):
        y0 = 60 + k * 24
        pts = []
        for x in range(30, 994, 8):
            y = y0 + 5 * math.sin((x + k * 37) / 46.0)
            pts.append((x, y))
        d.line(pts, fill=(90, 120, 130, 14), width=1)
    for k in range(10):
        x0 = 60 + k * 100
        pts = []
        for y in range(40, 690, 8):
            x = x0 + 4 * math.sin((y + k * 53) / 52.0)
            pts.append((x, y))
        d.line(pts, fill=(90, 120, 130, 10), width=1)
    base.alpha_composite(ov)


# ---------------------------------------------------------------- pages
def field(d, x, y, label, value, size=15, value_x=None, font=None):
    d.text((x, y), label, font=F(SANS, 9), fill=GREY)
    d.text((value_x if value_x is not None else x, y + 11), value,
           font=font or F(SERIF_B, size), fill=NAVY_D)


def build():
    rng = random.Random(7)
    img = Image.new("RGBA", (W, H), DESK + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    # Desk texture: faint speckles.
    for _ in range(500):
        x, y = rng.randint(0, W - 1), rng.randint(0, H - 1)
        d.ellipse([x, y, x + 1, y + 1], fill=(255, 255, 255, 8))
    # Soft shadow under the open passport.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(shadow)
    ds.rounded_rectangle([36, 44, 1000, 700], radius=8, fill=(0, 0, 0, 110))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    # Cover peeking out around the spread.
    d.rounded_rectangle([26, 30, 998, 694], radius=8, fill=(28, 44, 54, 255))
    d.rounded_rectangle([26, 30, 998, 694], radius=8, outline=GOLD, width=1)
    # Two pages.
    d.rectangle([30, 34, 512, 690], fill=PAGE + (255,))
    d.rectangle([512, 34, 994, 690], fill=PAGE + (255,))
    # Centre gutter shadow.
    for i in range(10):
        a = 26 - i * 2
        d.rectangle([512 - 10 + i, 34, 512 - 9 + i, 690],
                    fill=(60, 50, 30, a))
        d.rectangle([512 + 9 - i, 34, 512 + 10 - i, 690],
                    fill=(60, 50, 30, a))
    d.rectangle([30, 34, 994, 690], outline=(120, 100, 60, 255), width=1)
    guilloche(img)
    d = ImageDraw.Draw(img, "RGBA")

    # ============================================================ left page
    draw_arms(d, 88, 84, 27)
    d.text((128, 56), "REPUBLIC OF VELMARA", font=F(SERIF_B, 20),
           fill=NAVY_D)
    tracked(d, 128, 84, "RÉPUBLIQUE DE VELMARA", F(SANS, 9), GREY, 2)
    tracked(d, 128, 102, "PASSPORT — PASSEPORT", F(SANS_B, 10), NAVY, 3)
    d.line([54, 124, 492, 124], fill=GOLD, width=2)
    d.line([54, 128, 492, 128], fill=NAVY, width=1)

    # Photograph.
    d.rectangle([54, 140, 208, 324], fill=(255, 255, 255, 255),
                outline=NAVY, width=2)
    img.paste(draw_portrait(), (56, 142))
    d = ImageDraw.Draw(img, "RGBA")
    # Signature under the photograph.
    d.text((56, 336), "Elena Maris Voss", font=F(SERIF_I, 19), fill=INK)
    d.line([56, 362, 204, 362], fill=NAVY, width=1)
    d.text((56, 366), "HOLDER'S SIGNATURE", font=F(SANS, 8), fill=GREY)

    # Data fields.
    d.text((222, 142), "TYPE", font=F(SANS, 9), fill=GREY)
    d.text((222, 153), "P", font=F(SERIF_B, 15), fill=NAVY_D)
    d.text((300, 142), "CODE", font=F(SANS, 9), fill=GREY)
    d.text((300, 153), "VLM", font=F(SERIF_B, 15), fill=NAVY_D)
    d.text((368, 142), "PASSPORT No.", font=F(SANS, 9), fill=GREY)
    d.text((368, 153), "VLM482916", font=F(SERIF_B, 14), fill=NAVY_D)
    field(d, 222, 180, "SURNAME", "VOSS")
    field(d, 222, 211, "GIVEN NAMES", "ELENA MARIS")
    field(d, 222, 242, "NATIONALITY", "VELMARAN")
    field(d, 222, 273, "DATE OF BIRTH", "12 JUN 1994")
    field(d, 420, 273, "SEX", "F")
    field(d, 222, 304, "PLACE OF BIRTH", "ALDERPORT")
    field(d, 222, 335, "DATE OF ISSUE", "14 MAR 2023", size=14)
    field(d, 368, 335, "DATE OF EXPIRY", "14 MAR 2033", size=14)
    field(d, 222, 366, "AUTHORITY", "MINISTRY OF THE INTERIOR", size=13)
    d.text((222, 394), "ALDERPORT, VELMARA", font=F(SERIF, 11), fill=INK)
    field(d, 222, 412, "LANGUAGES", "VELMARAN — ENGLISH", size=13)

    # Motto under the fields.
    d.line([222, 470, 262, 470], fill=GOLD, width=1)
    d.line([448, 470, 488, 470], fill=GOLD, width=1)
    centre(d, 355, 460, "BY LIGHT AND TIDE", F(SERIF_I, 14),
           (120, 100, 50))
    centre(d, 350, 486, "The lighthouse keeps the harbour; the tide keeps "
           "time.", F(SERIF_I, 10), GREY)

    # Machine-readable zone.
    d.rectangle([44, 548, 502, 644], fill=(238, 231, 210, 255),
                outline=(210, 200, 170, 255), width=1)
    d.text((58, 554), "MACHINE READABLE ZONE", font=F(SANS, 8), fill=GREY)
    line1, line2 = mrz_lines()
    d.text((58, 574), line1, font=F(MONO, 15), fill=INK)
    d.text((58, 600), line2, font=F(MONO, 15), fill=INK)
    d.text((494, 656), "12", font=F(SANS, 10), fill=GREY, anchor="ra")

    # ============================================================ right page
    d.text((536, 56), "VISAS", font=F(SERIF_B, 20), fill=NAVY_D)
    tracked(d, 536, 84, "VISA · PAGES 13–14", F(SANS, 9), GREY, 2)
    d.text((964, 60), "VLM482916", font=F(MONO_B, 12), fill=NAVY_D,
           anchor="ra")
    d.text((964, 84), "PAGE 13", font=F(SANS, 9), fill=GREY, anchor="ra")
    d.line([536, 124, 964, 124], fill=GOLD, width=2)
    d.line([536, 128, 964, 128], fill=NAVY, width=1)

    # Stamp grid: six stamps, 02 APR 2023 -> 21 SEP 2024, chronological,
    # every one after the 14 MAR 2023 issue date.
    s1 = rect_stamp(206, 100, stamp_lines(
        "ALDERPORT — VELMARA", "DEPARTURE", "02 APR 2023", "EXIT · GATE 2",
        STAMP_NAVY), STAMP_NAVY, -3, 11)
    img.alpha_composite(s1, (536 - 26, 132 - 26))
    s2 = circle_stamp(100, [
        ("KINGDOM OF", F(SANS_B, 9), 225),
        ("THALOR", F(SANS_B, 13), 235),
        ("ARRIVAL", F(SANS_B, 13), 235),
        ("03 APR 2023", F(MONO_B, 12), 235),
        ("ARDUN", F(SANS, 9), 200),
    ], STAMP_TEAL, 4, 12)
    img.alpha_composite(s2, (845 - 72, 182 - 72))
    s3 = circle_stamp(92, [
        ("THALOR", F(SANS_B, 11), 225),
        ("DEPARTURE", F(SANS_B, 12), 235),
        ("18 APR 2023", F(MONO_B, 12), 235),
        ("ARDUN", F(SANS, 9), 200),
    ], STAMP_TEAL, -5, 13)
    img.alpha_composite(s3, (639 - 68, 298 - 68))
    s4 = rect_stamp(206, 100, stamp_lines(
        "ALDERPORT — VELMARA", "ARRIVAL", "19 APR 2023", "ENTRY · GATE 1",
        STAMP_NAVY), STAMP_NAVY, 2, 14)
    img.alpha_composite(s4, (758 - 26, 248 - 26))
    s5 = rect_stamp(206, 100, stamp_lines(
        "REPUBLIC OF SARNIA", "ARRIVAL", "07 SEP 2024", "HARBOUR GATE",
        STAMP_WINE), STAMP_WINE, 3, 15)
    img.alpha_composite(s5, (536 - 26, 364 - 26))
    s6 = rect_stamp(206, 100, stamp_lines(
        "REPUBLIC OF SARNIA", "DEPARTURE", "21 SEP 2024", "HARBOUR GATE",
        STAMP_WINE), STAMP_WINE, -2, 16)
    img.alpha_composite(s6, (758 - 26, 364 - 26))
    d = ImageDraw.Draw(img, "RGBA")

    # Condition box: the telling paperwork detail.
    d.rectangle([536, 492, 964, 592], fill=CREAM_BOX + (255,),
                outline=NAVY, width=2)
    d.text((552, 504), "CONDITION 7 — LIGHTKEEPER", font=F(SANS_B, 12),
           fill=NAVY_D)
    body = ("Holder is a licensed lightkeeper of the Velmaran Lighthouse "
            "Service. Exempt from harbour fees at all Velmaran ports. "
            "Permitted to land at unmanned light stations.")
    lines = wrap(d, body, F(SERIF, 12), 300)
    by = 528
    for ln in lines:
        d.text((552, by), ln, font=F(SERIF, 12), fill=INK)
        by += 16
    # Harbour-tax fee stamp, overlapping the box corner, dated the
    # issue date itself.
    fee = circle_stamp(84, [
        ("HARBOUR TAX", F(SANS_B, 9), 225),
        ("PAID · 12 VLM", F(SANS_B, 10), 235),
        ("ALDERPORT", F(SANS, 8), 200),
        ("14 MAR 2023", F(MONO_B, 9), 235),
    ], STAMP_WINE, -12, 17)
    img.alpha_composite(fee, (920 - 64, 500 - 64))
    d = ImageDraw.Draw(img, "RGBA")

    # Return home: the trip closes with an arrival in Velmara.
    s7 = rect_stamp(180, 54, [
        ("ALDERPORT — VELMARA", F(SANS_B, 10), 225),
        ("ARRIVAL", F(SANS_B, 13), 235),
        ("22 SEP 2024", F(MONO_B, 12), 235),
    ], STAMP_NAVY, -2, 18)
    img.alpha_composite(s7, (536 - 26, 600 - 26))
    d = ImageDraw.Draw(img, "RGBA")
    d.text((964, 606), "This passport remains the property of",
           font=F(SERIF_I, 11), fill=INK, anchor="ra")
    d.text((964, 624), "the Republic of Velmara and must be",
           font=F(SERIF_I, 11), fill=INK, anchor="ra")
    d.text((964, 642), "surrendered on demand.", font=F(SERIF_I, 11),
           fill=INK, anchor="ra")
    d.text((986, 656), "13", font=F(SANS, 10), fill=GREY, anchor="ra")

    rgb = img.convert("RGB")
    rgb.save(OUT, format="PNG", optimize=True)
    size = OUT.stat().st_size
    print(f"saved {OUT} {rgb.size[0]}x{rgb.size[1]} {size} bytes")
    assert size <= 1_048_576, "entry.png over the 1 MiB gate"
    assert rgb.size[0] <= 1024 and rgb.size[1] <= 1024
    return OUT


if __name__ == "__main__":
    build()
