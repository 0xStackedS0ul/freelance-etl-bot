# ETL Pipeline: Financial Market Monitor

A lightweight, highly reliable Python-based ETL (Extract, Transform, Load) microservice. It monitors financial assets via Google Finance, uses a local SQLite database for state management (preventing duplicate alerts), and dispatches real-time, aggregated notifications via the Telegram API.

# // Core Features

[EXTRACT] Web Scraping: Fetches real-time prices using requests and BeautifulSoup4. Includes polite scraping mechanisms (delays) and robust error handling.

[TRANSFORM & LOAD] State Management: Uses a local SQLite database to store records and detect price changes. Only new or updated prices trigger the next stage.

[NOTIFY] Alerts: Sends beautifully formatted, aggregated HTML messages to a designated Telegram chat to minimize API calls and avoid spam.

[SECURITY] Environment: Secures sensitive credentials (API tokens) using .env variables to prevent accidental leaks.

# // Project Architecture

```
* freelance-etl-bot/
* ├── core/                  # Core business logic (Separation of Concerns)
* │   ├── __init__.py
* │   ├── extractor.py       # Level 0: Web scraping and data collection
* │   ├── database.py        # Level 1: SQLite connection & deduplication
* │   └── notifier.py        # Level 2: Telegram API integration
* ├── data/                  # Local database storage (Git-ignored)
* │   └── records.db         
* ├── .env.example           # Template for environment variables
* ├── .gitignore             # Ignored files and sensitive data
* ├── requirements.txt       # Python dependencies
* ├── main.py                # Pipeline Orchestrator & Entry Point
* └── README.md              # Project documentation
```


# // Installation & Setup

## [1] Clone the repository

git clone https://github.com/yourusername/freelance-etl-bot.git
cd freelance-etl-bot


# [2] Install dependencies

It is recommended to use a virtual environment (e.g., venv)
pip install -r requirements.txt


## [3] Configure Environment Variables

Create a .env file in the root directory and add your Telegram credentials:
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here


## [4] Run the Pipeline

# Execute the main orchestrator script:
python main.py


// Future Improvements & Roadmap

[TODO: SCHEDULING] Integrate schedule or cron for automated daily/hourly executions.

[TODO: PERFORMANCE] Migrate to asynchronous requests (aiohttp) for faster extraction of massive asset lists.

[TODO: OBSERVABILITY] Add the Python logging module to replace console prints for production deployment and debugging.