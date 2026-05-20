import io
import datetime
import telebot
import yfinance as yf
from PIL import Image, ImageDraw, ImageFont

# 1. Initialize Bot
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"  # <-- Replace with your BotFather Token
bot = telebot.TeleBot(BOT_TOKEN)

# Helper function to pull live stock data safely
def get_live_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        todays_data = ticker.history(period='1d')
        if todays_data.empty:
            return "N/A", "0.00%"
        
        close_price = todays_data['Close'].iloc[-1]
        open_price = todays_data['Open'].iloc[-1]
        
        change = close_price - open_price
        pct_change = (change / open_price) * 180  # Simple % calculation
        
        sign = "+" if change >= 0 else ""
        return f"{close_price:,.2f}", f"{sign}{pct_change:.2f}%"
    except Exception:
        return "Error", "0.00%"

# 2. Function to build the custom graphic layout
def generate_market_dashboard():
    # Fetch real live data points from markets
    nifty_price, nifty_pct = get_live_data("^NSEI")       # Nifty 50 Ticker
    sensex_price, sensex_pct = get_live_data("^BSESN")   # Sensex Ticker
    tcs_price, tcs_pct = get_live_data("TCS.NS")          # TCS example
    
    # Create a base canvas (Width: 800, Height: 600) with a clean dark background
    image = Image.new("RGB", (800, 600), "#12161A")
    draw = ImageDraw.Draw(image)
    
    # Load fonts (Defaults to basic system font if custom .ttf is missing)
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        sub_font = ImageFont.truetype("arial.ttf", 18)
        data_font = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        title_font = sub_font = data_font = ImageFont.load_default()

    # --- Draw Header Block ---
    draw.rectangle([(0, 0), (800, 100)], fill="#0D1114")
    draw.text((30, 20), "VEDANSH CAPITAL", fill="#4CAF50", font=title_font)
    draw.text((35, 65), "MARKET DECODED", fill="#8A99AD", font=sub_font)
    
    current_date = datetime.datetime.now().strftime("%d %B %Y | %I:%M %p")
    draw.text((550, 40), current_date, fill="#FFFFFF", font=sub_font)
    
    # Draw a separating accent line
    draw.line([(0, 100), (800, 100)], fill="#4CAF50", width=3)

    # --- Section: Market Snapshot Snapshot ---
    draw.text((30, 130), "1. MARKET SNAPSHOT", fill="#4CAF50", font=sub_font)
    
    # Headers
    draw.text((30, 170), "Index", fill="#8A99AD", font=sub_font)
    draw.text((250, 170), "Price", fill="#8A99AD", font=sub_font)
    draw.text((450, 170), "% Change", fill="#8A99AD", font=sub_font)
    
    # Nifty Row
    draw.text((30, 210), "Nifty 50", fill="#FFFFFF", font=data_font)
    draw.text((250, 210), nifty_price, fill="#FFFFFF", font=data_font)
    nifty_color = "#26A69A" if "-" not in nifty_pct else "#EF5350"
    draw.text((450, 210), nifty_pct, fill=nifty_color, font=data_font)
    
    # Sensex Row
    draw.text((30, 250), "Sensex", fill="#FFFFFF", font=data_font)
    draw.text((250, 250), sensex_price, fill="#FFFFFF", font=data_font)
    sensex_color = "#26A69A" if "-" not in sensex_pct else "#EF5350"
    draw.text((450, 250), sensex_pct, fill=sensex_color, font=data_font)

    # --- Section: Top Gainers Example ---
    draw.text((30, 330), "2. TOP GAINERS", fill="#4CAF50", font=sub_font)
    draw.text((30, 370), "TCS", fill="#FFFFFF", font=data_font)
    draw.text((250, 370), f"₹{tcs_price}", fill="#FFFFFF", font=data_font)
    tcs_color = "#26A69A" if "-" not in tcs_pct else "#EF5350"
    draw.text((450, 370), tcs_pct, fill=tcs_color, font=data_font)

    # --- Footer ---
    draw.rectangle([(0, 560), (800, 600)], fill="#0D1114")
    draw.text((30, 570), "Disclaimer: For educational purposes only.", fill="#627387", font=sub_font)

    # Save image directly to a byte buffer in memory (instead of writing to disk)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

# 3. Telegram Command Handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Vedansh Capital Bot! Type /dashboard to get the live market image updates.")

@bot.message_handler(commands=['dashboard'])
def send_dashboard(message):
    bot.send_message(message.chat.id, "Fetching live NSE data and drawing your dashboard... Please wait.")
    try:
        # Generate the dynamic layout image buffer
        dashboard_img = generate_market_dashboard()
        # Fire it over Telegram API
        bot.send_photo(message.chat.id, photo=dashboard_img, caption="📊 Here is your live Market Dashboard snapshot.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Oops! Something went wrong drawing the graphic: {str(e)}")

# Run the bot continuously
print("Vedansh Capital Bot is active and listening...")
bot.infinity_polling()
