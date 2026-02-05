from scraper import (
    fetch_listing_links,
    fetch_product_name,
    extract_product_id
)
from notifier import send_telegram
from storage import load_seen, save_seen
from id_tracker import load_last_product_id, save_last_product_id
from config import (
    FIRSTCRY_LISTING_URL,
    FIRSTCRY_SEARCH_URL,
    SEEN_FILE,
    LAST_PRODUCT_ID_FILE
)
import os


def main():
    print("MONITOR STARTED")

    os.makedirs("data", exist_ok=True)

    # --------------------
    # Load state
    # --------------------
    seen = load_seen(SEEN_FILE)
    last_product_id = load_last_product_id(LAST_PRODUCT_ID_FILE)

    print("Seen products:", len(seen))
    print("Last product ID:", last_product_id)

    # --------------------
    # Fix 1: Listing + Search
    # --------------------
    listing_links = fetch_listing_links(FIRSTCRY_LISTING_URL)
    print("Listing links:", len(listing_links))

    search_links = fetch_listing_links(FIRSTCRY_SEARCH_URL)
    print("Search links:", len(search_links))

    links = list(set(listing_links + search_links))
    print("Total unique links:", len(links))

    # --------------------
    # Fix 1 logic (safe detection)
    # --------------------
    new_links = [l for l in links if l not in seen]
    print("New products found (listing/search):", len(new_links))

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
            print("Error processing product (Fix 1):", link)
            print(e)

    if new_links:
        seen.update(new_links)
        save_seen(SEEN_FILE, seen)
        print("Seen list updated")

    # --------------------
    # Fix 2: Product-ID early detection (aggressive)
    # --------------------
    max_detected_id = last_product_id

    for link in links:
        pid = extract_product_id(link)

        if pid and pid > last_product_id:
            try:
                name = fetch_product_name(link)

                message = (
                    "⚡ EARLY HOT WHEELS DROP ⚡\n\n"
                    f"Name: {name}\n\n"
                    f"Buy now:\n{link}"
                )

                send_telegram(message)

                if pid > max_detected_id:
                    max_detected_id = pid

            except Exception as e:
                print("Error processing product (Fix 2):", link)
                print(e)

    if max_detected_id > last_product_id:
        save_last_product_id(LAST_PRODUCT_ID_FILE, max_detected_id)
        print("Updated last product ID to:", max_detected_id)

    print("MONITOR FINISHED")


if __name__ == "__main__":
    main()
