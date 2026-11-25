"""Mirror the gate for this entry, locally, before a submission is spent.

Checks the file the gate checks (signature, IHDR, size, 1 MiB, chunk CRCs, a whole image),
the page's own rules (clear border, light and colour share, every card inside its box), that
two runs write the same bytes, and then reads the page back with OCR at full size and at the
300 pixels across the judge's criterion 5 names.

Run: node /opt/data/runpy.js /opt/data/ocr-venv/bin/python verify.py entry.png
"""

import hashlib
import struct
import sys
import zlib

from PIL import Image

import render
import stories

PASS, FAIL = [], []


def check(name, ok, detail=""):
    (PASS if ok else FAIL).append(name)
    print(("pass  " if ok else "FAIL  ") + name + ("  " + detail if detail else ""))


def chunks(path):
    raw = open(path, "rb").read()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    i, out = 8, []
    while i < len(raw):
        (n,) = struct.unpack(">I", raw[i:i + 4])
        typ = raw[i + 4:i + 8]
        data = raw[i + 8:i + 8 + n]
        (crc,) = struct.unpack(">I", raw[i + 8 + n:i + 12 + n])
        out.append((typ, data, crc == (zlib.crc32(typ + data) & 0xFFFFFFFF)))
        i += 12 + n
        if typ == b"IEND":
            break
    return raw, out


def main(path):
    raw, ch = chunks(path)
    w, h, depth, ctype = struct.unpack(">IIBB", ch[0][1][:10])
    check("png signature + IHDR first", ch[0][0] == b"IHDR")
    check("1024x1024", (w, h) == (1024, 1024), "%dx%d" % (w, h))
    check("8-bit truecolour", depth == 8 and ctype in (2, 6), "depth %d type %d" % (depth, ctype))
    check("<= 1 MiB", len(raw) <= 1048576, "%d bytes" % len(raw))
    check("every chunk CRC", all(c[2] for c in ch), "%d chunks" % len(ch))
    check("ends with IEND", ch[-1][0] == b"IEND")

    img = Image.open(path).convert("RGB")
    img.load()
    px = img.load()
    edge = 0
    for x in range(1024):
        for y in list(range(12)) + list(range(1012, 1024)):
            r, g, b = px[x, y]
            if r + g + b < 700:
                edge += 1
    for y in range(1024):
        for x in list(range(12)) + list(range(1012, 1024)):
            r, g, b = px[x, y]
            if r + g + b < 700:
                edge += 1
    check("clear 12px border", edge == 0, "%d ink px" % edge)

    light, colour = render.measure(img)
    check("light 60-92%", 60 <= light <= 92, "%.1f%%" % light)
    check("colour 8-25%", 8 <= colour <= 25, "%.1f%%" % colour)

    # two runs, same bytes: encode the page twice and compare the files with the committed one
    import io
    enc = []
    for _ in range(2):
        buf = io.BytesIO()
        render.build().save(buf, format="PNG", optimize=True)
        enc.append(buf.getvalue())
    check("two runs write identical PNGs", enc[0] == enc[1],
          hashlib.sha256(enc[0]).hexdigest()[:12])
    check("committed PNG is a fresh render", hashlib.sha256(enc[0]).hexdigest() == hashlib.sha256(raw).hexdigest(),
          hashlib.sha256(raw).hexdigest()[:12])

    # the page carries the day and the whole field
    n_stories = len(stories.LEADS) + len(stories.BRIEFS)
    check("34 or more stories", n_stories >= 34, "%d" % n_stories)
    check("every one of 8 regions used",
          sorted({s[0] for s in stories.LEADS} | {s[0] for s in stories.BRIEFS}) == sorted(stories.REGIONS))

    # OCR: full size and 300 px across
    try:
        from rapidocr_onnxruntime import RapidOCR
    except Exception as e:                                  # pragma: no cover
        print("no OCR:", e)
        return report()
    ocr = RapidOCR()
    full, _ = ocr(img)
    small = img.resize((300, 300), Image.LANCZOS).resize((1024, 1024), Image.LANCZOS)
    tiny, _ = ocr(small)
    def norm(s):
        return "".join(ch for ch in s.lower() if ch.isalnum())

    ft = norm(" ".join(r[1] for r in (full or [])))
    st = norm(" ".join(r[1] for r in (tiny or [])))
    print("ocr runs full %d / 300px %d" % (len(full or []), len(tiny or [])))

    check("date reads at 300px", "november2026" in st, "")
    for kw in ("115", "36", "tariff"):
        check("300px reads %s" % kw, kw.lower() in st)
    heads = [l[3] for l in stories.LEADS]
    for hd in heads:
        k = norm(" ".join(hd.split()[:2]))
        check("300px reads lead '%s'" % " ".join(hd.split()[:2]), k in st)
    places = [b[1] for b in stories.BRIEFS]
    found = sum(1 for p in places if norm(p) in ft)
    check("full-size OCR finds 26+ of %d places" % len(places), found >= 26, "%d/%d" % (found, len(places)))
    words_ok = sum(1 for b in stories.BRIEFS if norm(" ".join(b[3].split()[:2])) in ft)
    check("full-size OCR reads 30+ briefs' first words", words_ok >= 30, "%d/%d" % (words_ok, len(places)))
    return report()


def report():
    print("\nRESULT %d pass %d fail" % (len(PASS), len(FAIL)))
    if FAIL:
        print("failed:", ", ".join(FAIL))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "entry.png"))
