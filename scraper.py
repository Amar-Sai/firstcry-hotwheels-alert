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

        # STRICT pattern based on real URLs you shared
        if "/hot-wheels/" in href and "/product-detail" in href:
            if href.startswith("/"):
                href = "https://www.firstcry.com" + href
            href = href.split("?")[0]
            links.add(href)

    return list(links)

def fetch_product_name(product_url):
    r = requests.get(product_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # FirstCry product name is in <h1>
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)

    return "Unknown Hot Wheels Product"
