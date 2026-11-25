"""Scan the 25 Nov 2026 wires ourselves and write machine-readable items.

Each row is a real RSS item: its UTC time, outlet, headline and the first 160 chars of
the description. Nothing is invented; the page's stories are picked from this file.
Run: node /opt/data/runpy.js python3 scan25h.py
"""
import glob
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

OUT = "/opt/data/tmp/desk/feeds25h"
os.makedirs(OUT, exist_ok=True)

FEEDS = {
    "bbc-world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "bbc-top": "https://feeds.bbci.co.uk/news/rss.xml",
    "bbc-biz": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "bbc-tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "bbc-sci": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "guardian-world": "https://www.theguardian.com/world/rss",
    "guardian-biz": "https://www.theguardian.com/uk/business/rss",
    "guardian-sci": "https://www.theguardian.com/science/rss",
    "guardian-aus": "https://www.theguardian.com/australia-news/rss",
    "npr-world": "https://feeds.npr.org/1004/rss.xml",
    "npr-biz": "https://feeds.npr.org/1006/rss.xml",
    "dw-world": "https://rss.dw.com/rdf/rss-en-world",
    "france24": "https://www.france24.com/en/rss",
    "france24-africa": "https://www.france24.com/en/africa/rss",
    "cbc-world": "https://www.cbc.ca/webfeed/rss/rss-world",
    "scmp-asia": "https://www.scmp.com/rss/3/feed",
    "toi-world": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    "cna-asia": "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml",
    "sky-world": "https://feeds.skynews.com/feeds/rss/world.xml",
    "abc-au": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "rnz-world": "https://www.rnz.co.nz/rss/world.xml",
    "yonhap": "https://en.yna.co.kr/RSS/news.xml",
    "kyiv-ind": "https://kyivindependent.com/rss/",
    "anadolu": "https://www.aa.com.tr/en/rss/default?cat=guncel",
    "dawn": "https://www.dawn.com/feeds/home",
    "japan-times": "https://www.japantimes.co.jp/feed/",
    "gnews-world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
    "gnews-biz": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
}


def fetch(item):
    name, url = item
    dst = os.path.join(OUT, name + ".xml")
    subprocess.run(["curl", "-sSL", "-m", "16", "-A", "Mozilla/5.0", "-o", dst, url],
                   check=False, stderr=subprocess.DEVNULL)
    return name


with ThreadPoolExecutor(max_workers=10) as ex:
    list(ex.map(fetch, FEEDS.items()))

CUT = datetime(2026, 11, 25, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 11, 26, 0, 0, tzinfo=timezone.utc)


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()


rows, seen, nfeeds = [], set(), 0
for path in sorted(glob.glob(os.path.join(OUT, "*.xml"))):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    if len(raw) < 200:
        continue
    nfeeds += 1
    blocks = re.findall(r"<item>(.*?)</item>", raw, re.S) or re.findall(r"<entry>(.*?)</entry>", raw, re.S)
    for blk in blocks:
        mt = re.search(r"<title>(.*?)</title>", blk, re.S)
        if not mt:
            continue
        title = clean(mt.group(1))
        pd = (re.search(r"<pubDate>(.*?)</pubDate>", blk, re.S)
              or re.search(r"<published>(.*?)</published>", blk, re.S)
              or re.search(r"<updated>(.*?)</updated>", blk, re.S))
        if not pd:
            continue
        try:
            when = parsedate_to_datetime(pd.group(1).strip()).astimezone(timezone.utc)
        except Exception:
            try:
                when = datetime.fromisoformat(pd.group(1).strip().replace("Z", "+00:00")).astimezone(timezone.utc)
            except Exception:
                continue
        if when < CUT or when > END:
            continue
        src = re.search(r"<source[^>]*>(.*?)</source>", blk, re.S)
        outlet = clean(src.group(1)) if src else os.path.basename(path)[:-4]
        key = re.sub(r"[^a-z0-9 ]", "", title.lower())[:70]
        if key in seen or "google news" in title.lower():
            continue
        seen.add(key)
        desc = re.search(r"<description>(.*?)</description>", blk, re.S)
        rows.append({"utc": when.strftime("%Y-%m-%dT%H:%M:%SZ"), "hhmm": when.strftime("%H:%M"),
                     "outlet": outlet, "title": title,
                     "desc": clean(desc.group(1))[:160] if desc else ""})

rows.sort(key=lambda r: r["utc"])
json.dump(rows, open("/opt/data/tmp/desk/items25h.json", "w"), indent=0)
print(f"{len(rows)} items from {nfeeds} feeds")
# compact listing, newest first, so the run can curate by hand
for r in reversed(rows):
    print(f"{r['hhmm']}Z | {r['outlet'][:16]:16} | {r['title'][:104]}")
