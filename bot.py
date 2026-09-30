import telebot
import json
import os
from datetime import datetime

TOKEN = "8770454343:AAHS32QFIQf9ZuZS8zqOKaZVP3lcsq54ZrA"
bot = telebot.TeleBot(TOKEN)

PRICES_FILE = "prices.json"
HISTORY_FILE = "price_history.json"

def load_prices():
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_prices(prices):
    with open(PRICES_FILE, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

temp_product = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
        "👋 به ربات قیمت‌یاب خوش آمدی!\n"
        "💰 اسم یک محصول رو بفرست تا قیمتش رو برات پیدا کنم.\n"
        "➕ برای اضافه کردن محصول جدید: /add\n"
        "📊 برای مشاهده تاریخچه قیمت: /history نام محصول"
    )

@bot.message_handler(commands=['add'])
def ask_for_price(message):
    try:
        product_name = message.text.split(maxsplit=1)[1]
        temp_product[message.chat.id] = product_name
        bot.reply_to(message, f"✅ نام محصول '{product_name}' ثبت شد.\n"
                              "💰 حالا قیمت رو به صورت عدد وارد کن (مثلاً 600000)")
    except IndexError:
        bot.reply_to(message, "❌ اسم محصول رو بعد از /add بنویس. مثال:\n/add کتاب کار کلاس سوم")

@bot.message_handler(commands=['history'])
def show_history(message):
    try:
        # گرفتن نام محصول از پیام (بعد از دستور)
        product_name = message.text.split(maxsplit=1)[1]
        history = load_history()
        
        if product_name in history:
            history_list = history[product_name]
            text = f"📊 تاریخچه قیمت‌های {product_name}:\n"
            for entry in history_list[-10:]:  # ۱۰ مورد آخر
                old = entry.get('old_price', 'ندارد')
                text += f"- {entry['date']}: {entry['price']} (قبلی: {old})\n"
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, f"❌ هیچ تاریخچه‌ای برای '{product_name}' پیدا نشد.")
    except IndexError:
        bot.reply_to(message, "❌ اسم محصول رو بعد از /history بنویس. مثال:\n/history کتاب کار کلاس سوم")

@bot.message_handler(func=lambda message: True)
def handle_price_or_search(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    # اگر کاربر در مرحله‌ی وارد کردن قیمت است
    if chat_id in temp_product:
        product_name = temp_product.pop(chat_id)
        try:
            price = int(text.replace(",", ""))
            price_str = f"{price:,} تومان"
            
            prices = load_prices()
            old_price = prices.get(product_name)
            prices[product_name] = price_str
            save_prices(prices)
            
            history = load_history()
            if product_name not in history:
                history[product_name] = []
            history[product_name].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "price": price_str,
                "old_price": old_price
            })
            save_history(history)
            
            if old_price:
                bot.reply_to(message, f"✅ قیمت '{product_name}' از {old_price} به {price_str} تغییر کرد!")
            else:
                bot.reply_to(message, f"✅ محصول '{product_name}' با قیمت {price_str} اضافه شد!")
                
        except ValueError:
            bot.reply_to(message, "❌ لطفاً قیمت رو به صورت عدد وارد کن. مثلاً 600000")
        return
    
    # جستجوی محصول
    prices = load_prices()
    if text in prices:
        bot.reply_to(message, f"💰 قیمت {text}: {prices[text]}")
    else:
        bot.reply_to(message,
            f"❌ قیمتی برای '{text}' پیدا نکردم.\n"
            "📋 لیست محصولات موجود:\n" +
            "\n".join(prices.keys())
        )

print("🤖 ربات با تاریخچه قیمت روشن شد...")
bot.infinity_polling()