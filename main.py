import time
from core.extractor import scrape_financial_data
from core.database import init_db, save_and_check_if_new
from core.notifier import send_telegram_message


def main():
    print("🚀 Starting ETL Pipeline...")

    # 1. Initialize the database (ensures the table exists)
    init_db()

    # 2. Target assets for scraping
    target_assets = {
        "Apple (Tech)": "https://www.google.com/finance/quote/AAPL:NASDAQ",
        "Gold (Resource)": "https://www.google.com/finance/quote/GCW00:COMEX",
        "Bitcoin (Crypto)": "https://www.google.com/finance/quote/BTC-USD"
    }

    # --- STEP 1: EXTRACT (Gather data) ---
    print("\n[STEP 1] Extracting data from Google Finance...")
    scraped_data = scrape_financial_data(target_assets)

    if not scraped_data:
        print("[WARNING] No data was scraped. Exiting pipeline.")
        return

    # --- STEP 2 & 3: LOAD & NOTIFY (Filter via DB and prepare alerts) ---
    print("\n[STEP 2 & 3] Checking database and preparing notifications...")

    updated_items = []  # List to store texts of updated assets

    for item in scraped_data:
        asset = item['asset']
        price = item['price']
        timestamp = item['timestamp']

        # Check if the price has changed since the last run
        is_new = save_and_check_if_new(asset, price, timestamp)

        if is_new:
            # If the price is new, add a beautifully formatted block to our list
            item_message = (
                f"📈 <b>{asset}</b>\n"
                f"💵 <b>Current Price:</b> {price}\n"
                f"🕒 <b>Time:</b> {timestamp}"
            )
            updated_items.append(item_message)
            print(f"[ACTION] Price changed for {asset}. Added to notification queue.")
        else:
            print(f"[SKIP] {asset} - Price unchanged ({price}). No notification needed.")

    # If the updates list is not empty, send everything in a single message
    if updated_items:
        # Create a visual separator
        separator = "\n\n──────────────\n\n"

        # Format the final summary message
        summary_message = (
                "🚨 <b>Market Updates Summary</b> 🚨\n\n" +
                separator.join(updated_items)
        )

        print(f"\n[ACTION] Sending summary Telegram notification for {len(updated_items)} assets...")
        send_telegram_message(summary_message)
    else:
        print("\n[INFO] No new updates to send.")

    print(f"\n✅ Pipeline execution finished successfully. Assets updated: {len(updated_items)}.")


if __name__ == "__main__":
    main()