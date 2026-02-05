from scraper import fetch_listing_links, fetch_product_name
from notifier import send_telegram
from storage import load_seen, save_seen
from config import (
    FIRSTCRY_LISTING_URL,
    FIRSTCRY_SEARCH_URL,
    SEEN_FILE
)
import os

def main():
    print("MONITOR STARTED")

    os.makedirs("data", exist_ok=True)

    seen = load_seen(SEEN_FILE)
    print("Seen products:", len(seen))

    # 🔹 Fetch from brand listing
    listing_links = fetch_listing_links(FIRSTCRY_LISTING_URL)
    print("Listing links:", len(listing_links))

    # 🔹 Fetch from search page (Fix 1)
    search_links = fetch_listing_links(FIRSTCRY_SEARCH_URL)
    print("Search links:", len(search_links))

    # 🔹 Merge + deduplicate
    links = list(set(listing_links + search_links))
    print("Total unique links:", len(links))

    # 🔹 Detect new products
    new_links = [l for l in links if l not in seen]
    print("New products found:", len(new_links))

    for link in new_links:
        try:
            name = fetch_product_name(link)

            message = (
                "🔥 NEW HOT WHEELS DROP 🔥\n\n"
                f"Name: {name}\n\n"
                f"Buy now:\n{link}"
            )

            send_telegram(message)

        except Exception as e:
            # Do NOT crash the whole run for one bad product
            print("Error processing product:", link)
            print(e)

    if new_links:
        seen.update(new_links)
        save_seen(SEEN_FILE, seen)
        print("Seen list updated")

    print("MONITOR FINISHED")

if __name__ == "__main__":
    main()
