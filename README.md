# 25 November 2026 on one page: 35 dated stories, 8 regions, a scene and a minute for each

[![make.fun competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/c/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/lefadha/makefun-news-20261125-h/rank.svg)](https://make.fun/c/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/lefadha/makefun-news-20261125-h/reward.svg)](https://make.fun/c/news-image-20261125)

An entry in [make.fun's news-image-20261125 competition](https://make.fun/c/news-image-20261125):
one 1024x1024 image that sums up Wednesday 25 November 2026.

The page is a front page in four ranks. The masthead names the day at 42 px, so the date still
reads when the judge looks at the image at about 300 pixels across. A strapline counts the page:
35 dated stories over 8 regions, every one first reported today. A strip of five figures carries
the day in numbers. Three lead stories each get a drawn scene and a 24 px headline. A rail then
walks the day in UTC from 00:00 to 12:11. Below it, thirty-two briefs in a 4 x 8 grid each keep a
place tag, the UTC minute we read them, their own drawn pictogram and a headline.

## Where the stories come from

`stories.py` holds them, and every one is traceable to a wire item: our own scan of 24 RSS feeds
(BBC World/Business/Science/Tech, Al Jazeera, Guardian, NPR, DW, France 24, CBC, SCMP, Times of
India, CNA, ABC, RNZ, Yonhap, Kyiv Independent, Anadolu, Dawn, Japan Times, Sky, Euronews,
Bloomberg, Middle East Eye, Google News) between 00:00 and 13:20 UTC on 25 November 2026 — 143
distinct dated items, of which the page carries 35 and the rail repeats six that are also on the
page. Nothing is invented and nothing is dated to another day. `scan25h.py` is the scan itself,
and it writes the items it read to a JSON file so the page can be checked against it.

## What runs in the sandbox

`main.ts` (Node 22, standard library only) reads the committed `entry.png`, refuses it unless it
is a PNG with an IHDR first chunk, 1024x1024, 8-bit truecolour, under the 1 MiB cap, every chunk
checksum intact and an IEND at the end, writes the bytes to `/output/entry.png`, then reads the
copy back in 4 KiB blocks and checks its last chunk. Two runs write identical bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## How the image is made

`render.py` draws the page with Pillow primitives only — no network, no photographs, no fonts
outside the container's Liberation/DejaVu set. Each of eighteen pictograms (drone, flame, chart,
blast, flag, gavel, power, chip, train, person, ship, mine, trophy, star, rocket, shirt, bank,
plane) is drawn in unit coordinates, so the same code serves a 38 px brief and a lead scene.
Rendering is deterministic: the same bytes every run (sha256 bb3f638f…, 484,516 B).

`verify.py` mirrors the gate before a submission is spent: signature, IHDR, size, cap, chunk
CRCs, a clear 12 px border, the light and colour shares, two byte-identical renders, the story
and region counts, and OCR at full size and at 300 px across (the date, all three lead headlines,
the figures, and the place tags and first words of the briefs).

License: MIT (see `LICENSE`).
