A Telegram bot + Flask admin panel for tracking product prices with history.

⚠️ This project was built for learning purposes and is not intended for production use.

✨ Features
Telegram Bot
💰 Get product price by sending its name

➕ Add or update a product: /add <product name>

📊 View price history: /history <product name> (last 10 entries)

🗂 Stores data in JSON files

Flask Admin Panel
🌐 Web interface on port 5000

➕ Add new products

✏️ Edit product name/price

🗑️ Delete products

🛠 Tech Stack
Python 3.x

pyTelegramBotAPI (telebot) — bot

Flask — admin panel

JSON for storage

📁 Project Structure
PriceBot/
├── bot.py # Telegram bot
├── app.py # Flask admin panel
├── requirements.txt
├── README.md
├── .gitignore
├── prices.json # Not in git (user data)
├── price_history.json # Not in git (user data)
└── templates/
└── index.html

🚀 Setup
1. Install dependencies
pip install -r requirements.txt

2. Configure the token
Open bot.py and set your token:

TOKEN = "YOUR_BOT_TOKEN_HERE"

3. Run the bot
python bot.py

4. Run the admin panel (in another terminal)
python app.py

Then open: http://127.0.0.1:5000

📝 Bot Usage
/start — Welcome message

/add <product name> — Add or update a product price

/history <product name> — View last 10 price entries

Just send a product name — Get its current price

📄 License
Educational project — free to use and modify.