"""Draw 25 November 2026 on one page: 33 dated stories over 8 regions.

The page is built in four ranks, top to bottom: a masthead that names the day, a strip of
five figures that carry the day in numbers, three lead stories each with a drawn scene, and
a grid of thirty briefs that each keep a place, a UTC minute, a headline and a pictogram.
Everything is drawn from primitives here -- no photographs, no network, no randomness -- so
two runs write the same bytes.

Run:  node /opt/data/runpy.js /opt/data/manim-venv/bin/python render.py entry.png
"""

import sys

from PIL import Image, ImageDraw, ImageFont

import stories

W = H = 1024
SS = 2                                   # supersample, then LANCZOS down
M = 26                                   # outer margin (gate wants 12 px clear)
PAPER = (252, 250, 245)
INK = (22, 23, 26)
SOFT = (96, 100, 108)
HAIR = (188, 184, 176)
SIGNAL = (170, 38, 32)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

REGION_INK = {
    "MIDDLE EAST": (166, 52, 40),
    "EUROPE": (40, 66, 132),
    "AFRICA": (150, 92, 20),
    "EAST ASIA": (120, 44, 108),
    "SOUTH ASIA": (30, 104, 78),
    "SE ASIA": (178, 96, 16),
    "OCEANIA": (26, 92, 126),
    "AMERICAS": (92, 60, 132),
}

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size * SS)
    return _cache[key]


def text_w(dr, s, f):
    return dr.textlength(s, font=f)


def wrap(dr, s, f, width):
    """Greedy wrap that never splits a word, returns the lines."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(dr, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(dr, s, path, size, width, max_lines):
    """Largest size <= size whose wrap fits in max_lines."""
    while size > 8:
        f = font(path, size)
        lines = wrap(dr, s, f, width)
        if len(lines) <= max_lines:
            return f, lines, size
        size -= 1
    return font(path, 8), wrap(dr, s, font(path, 8), width), 8


# ---------------------------------------------------------------- pictograms
def icon(dr, kind, x, y, s, ink):
    """Draw `kind` inside the s x s box at (x, y) on the supersampled canvas."""
    def p(u, v):
        return x + u * s, y + v * s

    lw = max(2, int(s * 0.055))
    if kind == "drone":
        dr.line([p(.12, .34), p(.88, .34)], fill=ink, width=lw)
        for u in (.24, .5, .76):
            dr.line([p(u, .18), p(u, .34)], fill=ink, width=lw)
            dr.line([p(u - .1, .18), p(u + .1, .18)], fill=ink, width=lw)
        dr.rectangle([*p(.34, .36), *p(.66, .58)], fill=ink)
        dr.line([p(.5, .58), p(.5, .72)], fill=ink, width=lw)
        dr.ellipse([*p(.4, .72), *p(.6, .86)], outline=ink, width=lw)
    elif kind == "flame":
        dr.polygon([p(.5, .08), p(.72, .40), p(.66, .58), p(.80, .58), p(.62, .92),
                    p(.34, .92), p(.20, .66), p(.30, .46), p(.38, .60), p(.34, .34)], fill=ink)
        dr.ellipse([*p(.44, .62), *p(.58, .84)], fill=PAPER)
    elif kind == "chart":
        dr.line([p(.14, .14), p(.14, .86), p(.88, .86)], fill=ink, width=lw)
        for i, h in enumerate((.34, .52, .44, .72)):
            xx = .24 + i * .16
            dr.rectangle([*p(xx, .86 - h), *p(xx + .10, .84)], fill=ink)
        dr.line([p(.2, .44), p(.44, .56), p(.62, .40), p(.82, .22)], fill=SIGNAL, width=lw)
    elif kind == "blast":
        dr.polygon([p(.5, .06), p(.60, .32), p(.84, .20), p(.70, .44), p(.94, .52),
                    p(.66, .60), p(.80, .84), p(.56, .70), p(.50, .94), p(.42, .70),
                    p(.18, .84), p(.32, .60), p(.06, .52), p(.30, .44), p(.16, .20),
                    p(.40, .32)], fill=ink)
    elif kind == "flag":
        dr.line([p(.24, .10), p(.24, .92)], fill=ink, width=lw)
        dr.polygon([p(.26, .12), p(.82, .26), p(.26, .44)], fill=ink)
    elif kind == "gavel":
        dr.line([p(.20, .80), p(.62, .34)], fill=ink, width=int(lw * 2))
        dr.rectangle([*p(.54, .14), *p(.86, .34)], fill=ink)
        dr.line([p(.16, .90), p(.52, .90)], fill=ink, width=lw)
    elif kind == "power":
        dr.polygon([p(.52, .08), p(.24, .54), p(.46, .54), p(.38, .92), p(.70, .42),
                    p(.48, .42)], fill=ink)
    elif kind == "chip":
        dr.rectangle([*p(.24, .24), *p(.76, .76)], outline=ink, width=lw)
        dr.rectangle([*p(.38, .38), *p(.62, .62)], fill=ink)
        for u in (.34, .5, .66):
            dr.line([p(u, .10), p(u, .24)], fill=ink, width=lw)
            dr.line([p(u, .76), p(u, .90)], fill=ink, width=lw)
            dr.line([p(.10, u), p(.24, u)], fill=ink, width=lw)
            dr.line([p(.76, u), p(.90, u)], fill=ink, width=lw)
    elif kind == "train":
        dr.rounded_rectangle([*p(.18, .26), *p(.82, .74)], radius=int(s * .1), fill=ink)
        dr.rectangle([*p(.28, .34), *p(.72, .52)], fill=PAPER)
        dr.line([p(.24, .80), p(.16, .92)], fill=ink, width=lw)
        dr.line([p(.76, .80), p(.84, .92)], fill=ink, width=lw)
    elif kind == "person":
        dr.ellipse([*p(.38, .10), *p(.62, .34)], fill=ink)
        dr.polygon([p(.24, .92), p(.30, .52), p(.50, .40), p(.70, .52), p(.76, .92)], fill=ink)
    elif kind == "ship":
        dr.polygon([p(.10, .66), p(.90, .66), p(.76, .90), p(.24, .90)], fill=ink)
        dr.rectangle([*p(.26, .42), *p(.50, .64)], fill=ink)
        dr.rectangle([*p(.56, .30), *p(.74, .64)], fill=ink)
        dr.line([p(.14, .26), p(.14, .60)], fill=ink, width=lw)
    elif kind == "mine":
        dr.polygon([p(.10, .88), p(.40, .34), p(.60, .34), p(.90, .88)], fill=ink)
        dr.ellipse([*p(.44, .52), *p(.56, .64)], fill=PAPER)
        dr.line([p(.5, .20), p(.5, .34)], fill=ink, width=lw)
    elif kind == "trophy":
        dr.polygon([p(.34, .16), p(.66, .16), p(.62, .52), p(.38, .52)], fill=ink)
        dr.arc([*p(.14, .16), *p(.40, .46)], 90, 270, fill=ink, width=lw)
        dr.arc([*p(.60, .16), *p(.86, .46)], 270, 90, fill=ink, width=lw)
        dr.rectangle([*p(.46, .52), *p(.54, .74)], fill=ink)
        dr.rectangle([*p(.30, .74), *p(.70, .86)], fill=ink)
    elif kind == "star":
        dr.polygon([p(.5, .08), p(.60, .38), p(.92, .38), p(.66, .58), p(.76, .90),
                    p(.50, .70), p(.24, .90), p(.34, .58), p(.08, .38), p(.40, .38)], fill=ink)
    elif kind == "rocket":
        dr.polygon([p(.5, .06), p(.66, .40), p(.66, .70), p(.34, .70), p(.34, .40)], fill=ink)
        dr.polygon([p(.34, .70), p(.24, .92), p(.46, .80)], fill=SIGNAL)
        dr.polygon([p(.66, .70), p(.76, .92), p(.54, .80)], fill=SIGNAL)
    elif kind == "shirt":
        dr.polygon([p(.28, .16), p(.40, .10), p(.60, .10), p(.72, .16), p(.88, .38),
                    p(.72, .50), p(.72, .90), p(.28, .90), p(.28, .50), p(.12, .38)], fill=ink)
    elif kind == "bank":
        dr.polygon([p(.5, .08), p(.92, .32), p(.08, .32)], fill=ink)
        for u in (.18, .38, .58, .78):
            dr.rectangle([*p(u, .38), *p(u + .08, .78)], fill=ink)
        dr.rectangle([*p(.06, .80), *p(.94, .92)], fill=ink)
    elif kind == "plane":
        dr.polygon([p(.5, .06), p(.62, .44), p(.94, .62), p(.94, .72), p(.60, .64),
                    p(.58, .84), p(.72, .92), p(.72, .96), p(.5, .90), p(.28, .96),
                    p(.28, .92), p(.42, .84), p(.40, .64), p(.06, .72), p(.06, .62),
                    p(.38, .44)], fill=ink)
    elif kind == "cross":
        dr.rectangle([*p(.42, .10), *p(.58, .90)], fill=ink)
        dr.rectangle([*p(.18, .32), *p(.82, .48)], fill=ink)
    else:                                     # a bare dot, never reached
        dr.ellipse([*p(.3, .3), *p(.7, .7)], fill=ink)


def tile(dr, x, y, w, h, kind, region, seed):
    """A card's picture: paper ground, a wash of the region's colour, its pictogram."""
    dr.rectangle([x, y, x + w, y + h], fill=(250, 248, 242))
    wash = REGION_INK.get(region, INK)
    pale = tuple(int(c + (250 - c) * 0.55) for c in wash)
    dr.rectangle([x, y, x + w, y + h], fill=pale)
    dr.line([x, y + h, x + w, y + h], fill=HAIR, width=SS)
    icon(dr, kind, x + w * .22, y + h * .10, min(w, h) * .8, wash)


# ---------------------------------------------------------------- the page
def measure(img):
    px = img.convert("RGB").load()
    w, h = img.size
    light = colour = total = 0
    for yy in range(0, h, 3):
        for xx in range(0, w, 3):
            r, g, b = px[xx, yy]
            mx, mn = max(r, g, b), min(r, g, b)
            total += 1
            if mx > 225 and mx - mn < 22:
                light += 1
            elif mx - mn > 30:
                colour += 1
    return round(100 * light / total, 1), round(100 * colour / total, 1)


def build():
    im = Image.new("RGB", (W * SS, H * SS), PAPER)
    dr = ImageDraw.Draw(im)

    def S(v):
        return v * SS

    # --- masthead -----------------------------------------------------
    dr.rectangle([S(M), S(M), S(W - M), S(M + 2)], fill=INK)
    dr.text((S(M), S(M + 8)), "THE WORLD TODAY", font=font(SANS_B, 15), fill=SIGNAL)
    date_f = font(SERIF_B, 42)
    dr.text((S(M), S(M + 24)), stories.DAY, font=date_f, fill=INK)
    n_all = len(stories.LEADS) + len(stories.BRIEFS)
    sub = "%d dated stories \u00b7 %d regions \u00b7 every one first reported today \u00b7 %s" % (
        n_all, len(stories.REGIONS), stories.STAMP)
    dr.text((S(M), S(M + 76)), sub, font=font(SANS_B, 13), fill=SOFT)
    dr.rectangle([S(M), S(M + 96), S(W - M), S(M + 97)], fill=HAIR)

    # --- the day in numbers -------------------------------------------
    y0 = M + 104
    cw = (W - 2 * M) / 5
    for i, (val, lab1, lab2) in enumerate(stories.NUMBERS):
        cx = M + i * cw
        dr.text((S(cx + 4), S(y0)), val, font=font(SERIF_B, 30), fill=SIGNAL)
        dr.text((S(cx + 4), S(y0 + 38)), lab1, font=font(SANS, 10), fill=SOFT)
        dr.text((S(cx + 4), S(y0 + 50)), lab2, font=font(SANS, 10), fill=SOFT)
        if i:
            dr.rectangle([S(cx - 6), S(y0), S(cx - 5), S(y0 + 62)], fill=HAIR)
    dr.rectangle([S(M), S(y0 + 68), S(W - M), S(y0 + 69)], fill=HAIR)

    # --- three lead stories -------------------------------------------
    ly = y0 + 78
    lh = 250
    lw = (W - 2 * M - 2 * 10) / 3
    for i, (region, place, hhmm, head, kind, detail) in enumerate(stories.LEADS):
        x = M + i * (lw + 10)
        dr.rectangle([S(x), S(ly), S(x + lw), S(ly + lh)], outline=HAIR, width=SS)
        tile(dr, S(x + 1), S(ly + 1), S(lw - 2), S(96), kind, region, i)
        dr.rectangle([S(x + 6), S(ly + 6), S(x + 6 + 10 * len(region) * 0.62), S(ly + 21)],
                     fill=REGION_INK[region])
        dr.text((S(x + 9), S(ly + 9)), region, font=font(SANS_B, 9), fill=PAPER)
        dr.text((S(x + lw - 46), S(ly + 9)), place, font=font(SANS_B, 8), fill=PAPER)
        f, lines, size = fit_lines(dr, head, SERIF_B, 24, S(lw - 12), 4)
        yy = ly + 102
        for ln in lines:
            dr.text((S(x + 6), S(yy)), ln, font=f, fill=INK)
            yy += size + 4
        assert yy < ly + lh - 8, "lead %d overflows: %s" % (i, head)
        fd = font(SANS, 8.5)
        dl = wrap(dr, detail, fd, S(lw - 12))[:2]
        yy += 2
        for ln in dl:
            dr.text((S(x + 6), S(yy)), ln, font=fd, fill=SOFT)
            yy += 10
        assert yy <= ly + lh - 2, "lead %d detail overflows" % i

    # --- the day on a rail, then thirty briefs ------------------------
    ty = ly + lh + 10
    rail_f = font(SANS, 9)
    rail = "  \u00b7  ".join("%s %s" % (hhmm, txt) for hhmm, txt in stories.TIMELINE)
    rl = wrap(dr, rail, rail_f, S(W - 2 * M))[:2]
    yy = ty
    for ln in rl:
        dr.text((S(M), S(yy)), ln, font=rail_f, fill=SOFT)
        yy += 11
    dr.rectangle([S(M), S(yy + 2), S(W - M), S(yy + 3)], fill=HAIR)

    gy = yy + 9
    cols, rows = 4, 8
    gap = 8
    cw2 = (W - 2 * M - (cols - 1) * gap) / cols
    ch2 = (H - M - gy - (rows - 1) * gap) / rows
    for idx, (region, place, hhmm, head, kind) in enumerate(stories.BRIEFS):
        r, c = divmod(idx, cols)
        x = M + c * (cw2 + gap)
        y = gy + r * (ch2 + gap)
        dr.rectangle([S(x), S(y), S(x + cw2), S(y + ch2)], fill=(250, 248, 242), outline=HAIR, width=SS)
        tile(dr, S(x + 1), S(y + 1), S(38), S(ch2 - 2), kind, region, idx)
        dr.rectangle([S(x + 1), S(y + ch2 - 4), S(x + cw2 - 1), S(y + ch2 - 1)],
                     fill=REGION_INK[region])
        tx = x + 42
        tw = cw2 - 46
        dr.text((S(tx), S(y + 2)), place, font=font(SANS_B, 7.5), fill=REGION_INK[region])
        dr.text((S(tx + tw - 24), S(y + 2)), hhmm, font=font(SANS, 7), fill=SOFT)
        f, lines, size = fit_lines(dr, head, SANS_B, 10.5, S(tw), 3)
        yy = y + 13
        for ln in lines:
            dr.text((S(tx), S(yy)), ln, font=f, fill=INK)
            yy += size + 1.6
        assert yy <= y + ch2 - 5, "brief %d overflows (%s)" % (idx, head)

    # --- footer -------------------------------------------------------
    dr.rectangle([S(M), S(H - M - 12), S(W - M), S(H - M - 11)], fill=HAIR)
    dr.text((S(M), S(H - M - 8)), stories.SCAN_NOTE, font=font(SANS, 7.5), fill=SOFT)

    out = im.resize((W, H), Image.LANCZOS)
    return out


if __name__ == "__main__":
    dst = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    img.save(dst, optimize=True)
    print("wrote", dst, img.size, "light/colour", measure(img))
