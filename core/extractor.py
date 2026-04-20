import requests
from bs4 import BeautifulSoup
import time


def scrape_financial_data(assets: dict) -> list[dict]:
    """
    Scrapes current prices for a given list of financial assets from Google Finance.

    Args:
        assets (dict): A dictionary where keys are asset names and values are their
                       Google Finance URLs or ticker paths.

    Returns:
        list[dict]: A list of dictionaries containing the asset name, price, and timestamp.
    """

    # Headers are crucial to prevent the server from blocking us as a bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    extracted_data = []

    for name, url in assets.items():
        try:
            # Step 1: Make the HTTP request
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Will raise an exception for 4xx or 5xx errors

            # Step 2: Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Step 3: Extract the price.
            # Note: The class 'YMlKec fxKbKc' is currently used by Google Finance for main prices.
            # In real scraping, HTML classes can change, which requires maintenance.
            price_element = soup.find('div', class_='YMlKec fxKbKc')

            if price_element:
                price_text = price_element.text.strip()

                extracted_data.append({
                    'asset': name,
                    'price': price_text,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f"[SUCCESS] {name}: {price_text}")
            else:
                print(f"[WARNING] Could not find the price element for {name}. HTML structure might have changed.")

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Network error while fetching {name}: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error processing {name}: {e}")

        # Polite scraping: short pause between requests to avoid rate limits
        time.sleep(2)

    return extracted_data


# --- Testing Level 0 ---
if __name__ == "__main__":
    # Dictionary of target assets: Tech, Resources, Crypto
    target_assets = {
        "Apple (Tech)": "https://www.google.com/finance/quote/AAPL:NASDAQ",
        "Gold (Resource)": "https://www.google.com/finance/quote/GCW00:COMEX",
        "Bitcoin (Crypto)": "https://www.google.com/finance/quote/BTC-USD"
    }

    print("Initiating Level 0: Data Extraction...\n")
    results = scrape_financial_data(target_assets)

    print("\nExtraction Complete. Raw Data Output:")
    for item in results:
        print(item)