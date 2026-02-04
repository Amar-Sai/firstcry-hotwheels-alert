import requests
from bs4 import BeautifulSoup

def fetch_product_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; HotWheelsMonitor/1.0)"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    product_links = set()

    for a in soup.select("a[href]"):
        href = a.get("href")
        if href and "/product/" in href:
            if href.startswith("/"):
                href = "https://www.firstcry.com" + href
            product_links.add(href)

    return list(product_links)
