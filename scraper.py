import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://www.firstcry.com/"
}

def fetch_listing_links(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    links = set()

    for a in soup.select("a[href]"):
        href = a.get("href")
        if not href:
            continue

        if "/hot-wheels/" in href and "/product-detail" in href:

            # ✅ COMPLETE FirstCry URL normalization
            if href.startswith("http"):
                pass
            elif href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/www.firstcry.com"):
                href = "https://" + href.lstrip("/")
            elif href.startswith("/"):
                href = "https://www.firstcry.com" + href
            else:
                continue

            href = href.split("?")[0]
            links.add(href)

    return list(links)


def fetch_product_name(product_url):
    r = requests.get(product_url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # 1️⃣ Try structured product name
    h1 = soup.find("h1", attrs={"itemprop": "name"})
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)

    # 2️⃣ Try OpenGraph title
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()

    # 3️⃣ Fallback to page title
    title = soup.title.string if soup.title else None
    if title:
        return title.replace(" | FirstCry.com", "").strip()

    return "Hot Wheels Product"

