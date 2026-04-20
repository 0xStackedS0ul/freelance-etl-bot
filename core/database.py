import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'records.db')


def init_db():
    """
    Initializes the SQLite database. Creates the data directory if it doesn't exist
    and sets up the target table for asset prices.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asset_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset TEXT NOT NULL,
                price TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        print(f"[DB INFO] Database initialized at {DB_PATH}")


def save_and_check_if_new(asset: str, price: str, timestamp: str) -> bool:
    """
    Checks if the price has changed since the last record.
    If it's a new price (or a new asset), it saves it to the DB and returns True.
    If the price is identical to the last one, it returns False.

    Args:
        asset (str): Name of the asset (e.g., 'Apple (Tech)')
        price (str): Current scraped price
        timestamp (str): Time of extraction

    Returns:
        bool: True if the price is new/changed, False otherwise.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT price FROM asset_prices 
            WHERE asset = ? 
            ORDER BY id DESC LIMIT 1
        ''', (asset,))

        result = cursor.fetchone()
        last_price = result[0] if result else None

        if price != last_price:
            cursor.execute('''
                INSERT INTO asset_prices (asset, price, timestamp)
                VALUES (?, ?, ?)
            ''', (asset, price, timestamp))
            conn.commit()
            return True

        return False


# --- Testing Level 1 ---
if __name__ == "__main__":
    print("Initiating Level 1: Database Test...\n")

    init_db()

    print("\n--- First Execution ---")
    is_new_1 = save_and_check_if_new("Test Coin", "$100.00", "2026-04-20 19:00:00")
    print(f"Added 'Test Coin' at $100.00 -> Is new? {is_new_1}")

    print("\n--- Second Execution (Same Price) ---")
    is_new_2 = save_and_check_if_new("Test Coin", "$100.00", "2026-04-20 19:05:00")
    print(f"Added 'Test Coin' at $100.00 -> Is new? {is_new_2}")

    print("\n--- Third Execution (Price Changed) ---")
    is_new_3 = save_and_check_if_new("Test Coin", "$105.50", "2026-04-20 19:10:00")
    print(f"Added 'Test Coin' at $105.50 -> Is new? {is_new_3}")