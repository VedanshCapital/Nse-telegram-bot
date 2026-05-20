import io
import datetime
import threading
import telebot
import yfinance as yf
from PIL import Image, ImageDraw, ImageFont
from flask import Flask

# --- FAKE WEB SERVER FOR RENDER FREE TIER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- YOUR TELEGRAM BOT CODE ---
BOT_TOKEN = "8793559199:AAHGpMK_IB7AIvcZeHptk_HmCQBYJkCpRzg"
bot = telebot.TeleBot(BOT_TOKEN)

def get_live_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        todays_data = ticker.history(period='1d')
        if todays_data.empty: return "N/A", "0.00%"
        close_price = todays_data['Close'].iloc[-1]
        open_price = todays_data['Open'].iloc[-1]
        change = close_price - open_price
        pct_change = (change / open_price) * 100
        sign = "+" if change >= 0 else ""
        return f"{close_price:,.2f}", f"{sign}{pct_change:.2f}%"
    except:
        return "Error", "0.00%"

def generate_market_dashboard():
    nifty_price, nifty_pct = get_live_data("^NSEI")
    sensex_price, sensex_pct = get_live_data("^BSESN")
    
    image = Image.new("RGB", (800, 500), "#12161A")
    draw = ImageDraw.Draw(image)
    
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        sub_font = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        title_font = sub_font = ImageFont.load_default()

    draw.rectangle([(0, 0), (800, 100)], fill="#0D1114")
    draw.text((30, 20), "VEDANSH CAPITAL", fill="#4CAF50", font=title_font)
    draw.text((35, 65), "MARKET DECODED", fill="#8A99AD", font=sub_font)
    
    draw.text((30, 150), f"Nifty 50: {nifty_price} ({nifty_pct})", fill="#FFFFFF", font=title_font)
    draw.text((30, 220), f"Sensex: {sensex_price} ({sensex_pct})", fill="#FFFFFF", font=title_font)
    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

@bot.message_handler(commands=['start', 'dashboard'])
def send_dashboard(message):
    bot.send_message(message.chat.id, "Fetching live NSE data...")
    try:
        dashboard_img = generate_market_dashboard()
        bot.send_photo(message.chat.id, photo=dashboard_img, caption="📊 Vedansh Capital Dashboard")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")

# --- START BOTH SESSiONS ---
if __name__ == "__main__":
    # Start the web server in a separate background thread
    t = threading.Thread(target=run_web_server)
    t.start()
    
    # Start the telegram bot polling
    print("Vedansh Capital Bot is active...")
    bot.infinity_polling()
