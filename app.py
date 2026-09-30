from flask import Flask, render_template, request, jsonify
import json
import sys
import os

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

PRICES_FILE = "prices.json"

def load_prices():
    if os.path.exists(PRICES_FILE):
        with open(PRICES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_prices(prices):
    with open(PRICES_FILE, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    prices = load_prices()
    return render_template('index.html', products=prices)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    if name and price:
        prices = load_prices()
        prices[name] = price
        save_prices(prices)
        return jsonify({"status": "success", "message": f"✅ محصول '{name}' با قیمت {price} اضافه شد."})
    return jsonify({"status": "error", "message": "❌ نام و قیمت را وارد کنید."})

@app.route('/delete', methods=['POST'])
def delete_product():
    name = request.form.get('name')
    if name:
        prices = load_prices()
        if name in prices:
            del prices[name]
            save_prices(prices)
            return jsonify({"status": "success", "message": f"🗑️ محصول '{name}' حذف شد."})
        return jsonify({"status": "error", "message": f"❌ محصول '{name}' یافت نشد."})
    return jsonify({"status": "error", "message": "❌ نام محصول را وارد کنید."})

@app.route('/edit', methods=['POST'])
def edit_product():
    old_name = request.form.get('old_name')
    new_name = request.form.get('new_name')
    new_price = request.form.get('new_price')
    
    if old_name and new_name and new_price:
        prices = load_prices()
        if old_name in prices:
            # حذف محصول قدیمی
            del prices[old_name]
            # اضافه کردن با نام و قیمت جدید
            prices[new_name] = new_price
            save_prices(prices)
            return jsonify({
                "status": "success", 
                "message": f"✅ محصول '{old_name}' به '{new_name}' با قیمت {new_price} ویرایش شد."
            })
        return jsonify({"status": "error", "message": f"❌ محصول '{old_name}' یافت نشد."})
    return jsonify({"status": "error", "message": "❌ تمام فیلدها را پر کنید."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)