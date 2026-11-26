"""뽐뿌 + Google 뉴스 수집 데모. 표준 라이브러리만 사용.

실행: python3 collect.py            -> data.json 갱신
테스트: FIXTURE_DIR=tests/fixtures python3 collect.py   (네트워크 없이 저장된 응답으로 실행)
"""
import html
import json
import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

KST = timezone(timedelta(hours=9))
UA = "Mozilla/5.0 (deal-tracker-demo; personal use)"
HEADERS = {"User-Agent": UA}
FIXTURE_DIR = os.environ.get("FIXTURE_DIR")


def fetch(url, fixture_name):
    if FIXTURE_DIR:
        path = os.path.join(FIXTURE_DIR, fixture_name)
        return open(path, "rb").read() if os.path.exists(path) else None
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read()


def iso(dt):
    return dt.astimezone(KST).isoformat(timespec="minutes")


def text(el, tag):
    found = el.find(tag)
    return (found.text or "").strip() if found is not None else ""


def parse_deal_title(title):
    """'[롯데온] 상품명 (47,740원/무료)' -> 쇼핑몰, 가격"""
    shop = re.match(r"\s*\[([^\]]+)\]", title)
    price = re.search(r"([\d,]+)\s*원", title)
    return (shop.group(1) if shop else ""), (price.group(1) + "원" if price else "")


# ---------- 뽐뿌 ----------
def ppomppu_rss():
    raw = fetch("https://www.ppomppu.co.kr/rss.php?id=ppomppu", "ppomppu_rss.xml")
    if not raw:
        return []
    items = []
    for it in ET.fromstring(raw).iter("item"):
        link = text(it, "link")
        no = re.search(r"no=(\d+)", link)
        title = html.unescape(text(it, "title"))
        shop, price = parse_deal_title(title)
        items.append({
            "id": f"pp-{no.group(1) if no else link}",
            "source": "뽐뿌",
            "title": title,
            "shop": shop,
            "price": price,
            "category": "",
            "summary": html.unescape(text(it, "description"))[:120],
            "link": link.replace("http://", "https://"),
            "published": iso(parsedate_to_datetime(text(it, "pubDate"))),
        })
    return items


def ppomppu_list(page):
    """목록 페이지(20건/페이지, EUC-KR). 스크립트 접근은 403으로 막혀 있어 기본값은 사용 안 함(config: ppomppu_list_pages=0)."""
    raw = fetch(f"https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page={page}",
                f"ppomppu_list_{page}.html")
    if not raw:
        return []
    page_html = raw.decode("euc-kr", errors="replace")
    items = []
    for row in re.findall(r'<tr[^>]*class="baseList[^"]*"[^>]*>(.*?)</tr>', page_html, re.S):
        no = re.search(r'baseList-numb"[^>]*>\s*(\d+)', row)
        title_m = re.search(r'class="baseList-title[^"]*"[^>]*>(.*?)</a>', row, re.S)
        when = re.search(r'title="(\d\d\.\d\d\.\d\d \d\d:\d\d:\d\d)"', row)
        if not (no and title_m and when):
            continue  # 공지·광고 행 등
        title = html.unescape(re.sub(r"<[^>]+>", " ", title_m.group(1)))
        title = re.sub(r"\]\s*", "] ", re.sub(r"\s+", " ", title)).strip()
        cat = re.search(r'baseList-small">\s*\[([^\]]+)\]', row)
        shop, price = parse_deal_title(title)
        published = datetime.strptime(when.group(1), "%y.%m.%d %H:%M:%S").replace(tzinfo=KST)
        items.append({
            "id": f"pp-{no.group(1)}",
            "source": "뽐뿌",
            "title": title,
            "shop": shop,
            "price": price,
            "category": cat.group(1) if cat else "",
            "summary": "",
            "link": f"https://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&no={no.group(1)}",
            "published": iso(published),
        })
    return items


# ---------- Google 뉴스 ----------
def google_news(query, period):
    q = urllib.parse.quote(f"{query} when:{period}")
    url = f"https://news.google.com/rss/search?q={q}&hl=ko&gl=KR&ceid=KR:ko"
    raw = fetch(url, f"gnews_{query.replace(' ', '_')}.xml")
    if not raw:
        return []
    items = []
    for it in ET.fromstring(raw).iter("item"):
        source = text(it, "source")
        title = html.unescape(text(it, "title"))
        if source and title.endswith(" - " + source):
            title = title[: -len(source) - 3]  # 제목 끝 ' - 언론사' 제거
        items.append({
            "id": "gn-" + text(it, "guid")[:40],
            "source": "뉴스",
            "title": title,
            "shop": source,  # 뉴스는 언론사 이름
            "price": "",
            "category": query,
            "summary": "",
            "link": text(it, "link"),
            "published": iso(parsedate_to_datetime(text(it, "pubDate"))),
        })
    return items


def news_key(title):
    """같은 보도자료를 여러 언론사가 쓴 경우 묶기 위한 키"""
    return re.sub(r"[^가-힣A-Za-z0-9]", "", title)[:18]


def main():
    cfg = json.load(open("config.json", encoding="utf-8"))
    errors = []

    def safe(name, fn, *args):
        try:
            return fn(*args)
        except Exception as e:  # 한 소스가 실패해도 나머지는 계속
            errors.append(f"{name}: {e}")
            return []

    new = safe("뽐뿌 RSS", ppomppu_rss)
    for p in range(1, cfg.get("ppomppu_list_pages", 0) + 1):
        new += safe(f"뽐뿌 목록 {p}p", ppomppu_list, p)
    for q in cfg["news_queries"]:
        new += safe(f"뉴스 '{q}'", google_news, q, cfg.get("news_period", "7d"))

    old = []
    if os.path.exists("data.json"):
        old = json.load(open("data.json", encoding="utf-8")).get("items", [])

    by_id = {i["id"]: i for i in old}
    for i in new:  # 새로 받은 값 우선, 빈 칸은 이전 값(예: 목록에만 있는 category)으로 채움
        merged = dict(i)
        for k, v in by_id.get(i["id"], {}).items():
            if not merged.get(k):
                merged[k] = v
        by_id[i["id"]] = merged

    cutoff = datetime.now(KST) - timedelta(days=cfg.get("keep_days", 7))
    items, seen_news = [], set()
    for i in sorted(by_id.values(), key=lambda x: x["published"], reverse=True):
        if datetime.fromisoformat(i["published"]) < cutoff and not FIXTURE_DIR:
            continue
        if i["source"] == "뉴스":
            k = news_key(i["title"])
            if k in seen_news:
                continue
            seen_news.add(k)
        items.append(i)

    out = {"updated": iso(datetime.now(KST)), "errors": errors, "items": items}
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"items={len(items)} (뽐뿌 {sum(i['source']=='뽐뿌' for i in items)}, "
          f"뉴스 {sum(i['source']=='뉴스' for i in items)}) errors={errors}")


if __name__ == "__main__":
    main()
