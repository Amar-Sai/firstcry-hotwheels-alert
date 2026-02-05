from scraper import (
    fetch_listing_links,
    fetch_product_name,
    extract_product_id,
    is_buyable
)
from notifier import send_telegram
from state_tracker import load_states, save_states
from config import (
    FIRSTCRY_LISTING_URL,
    FIRSTCRY_SEARCH_URL,
    PRODUCT_STATE_FILE
)
import os

def main():
    print("MONITOR STARTED")

    os.makedirs("data", exist_ok=True)

    states = load_states(PRODUCT_STATE_FILE)

    # ---- Discovery layer ----
    listing_links = fetch_listing_links(FIRSTCRY_LISTING_URL)
    search_links = fetch_listing_links(FIRSTCRY_SEARCH_URL)

    links = list(set(listing_links + search_links))
    print("Total discovered links:", len(links))

    visible_ids = set()

    for link in links:
        pid = extract_product_id(link)
        if not pid:
            continue

        pid = str(pid)
        visible_ids.add(pid)

        buyable = is_buyable(link)
        prev_state = states.get(pid, "NEW")

        # Determine current state
        if buyable:
            current_state = "ACTIVE"
        else:
            current_state = "OUT_OF_STOCK"

        # ---- Notification rules ----
        notify = False

        if prev_state in ["NEW", "OUT_OF_STOCK", "HIDDEN"] and current_state == "ACTIVE":
            notify = True

        if notify:
            name = fetch_product_name(link)
            message = (
                "🔥 HOT WHEELS AVAILABLE 🔥\n\n"
                f"Name: {name}\n\n"
                f"Buy now:\n{link}"
            )
            send_telegram(message)

        states[pid] = current_state

    # ---- Handle hidden products ----
    for pid in list(states.keys()):
        if pid not in visible_ids:
            if states[pid] == "ACTIVE":
                states[pid] = "HIDDEN"

    save_states(PRODUCT_STATE_FILE, states)

    print("MONITOR FINISHED")

if __name__ == "__main__":
    main()
