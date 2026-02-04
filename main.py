from scraper import fetch_product_links
from database import init_db, is_new_product
from notifier import send_telegram_message
from config import FIRSTCRY_URL, DB_PATH

def main():
    init_db(DB_PATH)

    links = fetch_product_links(FIRSTCRY_URL)
    new_links = []

    for link in links:
        if is_new_product(DB_PATH, link):
            new_links.append(link)

    for link in new_links:
        msg = f"🔥 NEW HOT WHEELS PRODUCT DETECTED 🔥\n\n{link}"
        send_telegram_message(msg)

if __name__ == "__main__":
    main()
