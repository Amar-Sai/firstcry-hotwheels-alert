from scraper import fetch_listing_links, fetch_product_name
from notifier import send_telegram
from storage import load_seen, save_seen
from config import (
    FIRSTCRY_LISTING_URL,
    FIRSTCRY_SEARCH_URL,
    SEEN_FILE,
    HOTWHEELS_KEYWORDS
)
import os


def matches_keywords(product_name: str) -> bool:
    name = product_name.lower()
    return any(keyword in name for keyword in HOTWHEELS_KEYWORDS)


def main():
    print("MONITOR STARTED")

    os.makedirs("data", exist_ok=True)

    seen = load_seen(SEEN_FILE)
    print("Seen products:", len(seen))

    # Fetch links
    listing_links = fetch_listing_links(FIRSTCRY_LISTING_URL)
    search_links = fetch_listing_links(FIRSTCRY_SEARCH_URL)

    links = list(set(listing_links + search_links))
    print("Total unique links:", len(links))

    # Detect new products
    new_links = [l for l in links if l not in seen]
    print("New products found:", len(new_links))

    for link in new_links:
        try:
            name = fetch_product_name(link)

            # 🔒 KEYWORD GATE (critical change)
            if not matches_keywords(name):
                print("Skipping (keyword filter):", name)
                continue

            message = (
                "🔥 HIGH-PRIORITY HOT WHEELS DROP 🔥\n\n"
                f"Name: {name}\n\n"
                f"Buy now:\n{link}"
            )

            send_telegram(message)

        except Exception as e:
            print("Error processing product:", link)
            print(e)

    # Mark all new links as seen (even skipped ones)
    if new_links:
        seen.update(new_links)
        save_seen(SEEN_FILE, seen)
        print("Seen list updated")

    print("MONITOR FINISHED")


if __name__ == "__main__":
    main()

