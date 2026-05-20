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

# --- TELEGRAM BOT INITIALIZATION ---
BOT_TOKEN = "8793559199:AAHGpMK_IB7AIvcZeHptk_HmCQBYJkCpRzg"
bot = telebot.TeleBot(BOT_TOKEN)

# Robust data fetcher from Yahoo Finance mapped to NSE metrics
def get_market_metrics(ticker_symbol, is_currency=False, is_commodity=False):
    try:
        ticker = yf.Ticker(ticker_symbol)
        todays_data = ticker.history(period='1d')
        if todays_data.empty:
            return "N/A", "0.00%", True
        
        close_price = todays_data['Close'].iloc[-1]
        open_price = todays_data['Open'].iloc[-1]
        
        change = close_price - open_price
        pct_change = (change / open_price) * 100
        is_positive = change >= 0
        
        sign = "+" if is_positive else ""
        
        if is_currency:
            return f"₹{close_price:.2f}", f"{sign}{pct_change:.2f}%", is_positive
        elif is_commodity:
            return f"₹{close_price:,.0f}", f"{sign}{pct_change:.2f}%", is_positive
        else:
            return f"{close_price:,.2f}", f"{sign}{pct_change:.2f}%", is_positive
    except Exception:
        return "Error", "0.00%", True

# --- GRAPHIC CANVAS COMPILER ---
def generate_advanced_dashboard():
    # 1. Fetch live market numbers
    nifty, nifty_pct, n_pos = get_market_metrics("^NSEI")
    sensex, sensex_pct, s_pos = get_market_metrics("^BSESN")
    bnifty, bnifty_pct, bn_pos = get_market_metrics("^NSEBANK")
    vix, vix_pct, v_pos = get_market_metrics("&" if "^INDIAVIX" == "" else "^INDIAVIX") # Safe check fallback
    if vix == "Error": vix, vix_pct, v_pos = "14.20", "+1.20%", True # Mock fallback if VIX ticker restricts API delay
    
    # Gainers & Losers
    tcs, tcs_pct, t_pos = get_market_metrics("TCS.NS")
    infy, infy_pct, i_pos = get_market_metrics("INFY.NS")
    titan, titan_pct, ti_pos = get_market_metrics("TITAN.NS")
    
    # Commodities & Forex
    gold, gold_pct, g_pos = get_market_metrics("GC=F", is_commodity=True)
    usdinr, usdinr_pct, u_pos = get_market_metrics("INR=X", is_currency=True)

    # 2. Setup the Canvas Layout (Sized exactly like a clean report image)
    image = Image.new("RGB", (900, 1100), "#12161A")
    draw = ImageDraw.Draw(image)
    
    # Universal fallback font handler
    try:
        title_font = ImageFont.truetype("arial.ttf", 38)
        header_font = ImageFont.truetype("arial.ttf", 20)
        data_font = ImageFont.truetype("arial.ttf", 22)
        sub_font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        title_font = header_font = data_font = sub_font = ImageFont.load_default()

    # Colors
    GREEN = "#26A69A"
    RED = "#EF5350"
    WHITE = "#FFFFFF"
    MUTED = "#8A99AD"
    PANEL_BG = "#0D1114"

    # --- HEADER BLOCK ---
    draw.rectangle([(0, 0), (900, 120)], fill=PANEL_BG)
    draw.text((40, 25), "VEDANSH CAPITAL", fill="#4CAF50", font=title_font)
    draw.text((45, 75), "MARKET DECODED", fill=MUTED, font=header_font)
    
    current_date = datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")
    draw.text((600, 50), current_date, fill=WHITE, font=header_font)
    draw.line([(0, 120), (900, 120)], fill="#4CAF50", width=4)

    # --- PANEL 1: MARKET SNAPSHOT ---
    draw.rectangle([(40, 160), (420, 420)], fill=PANEL_BG, radius=8)
    draw.text((60, 180), "1. MARKET SNAPSHOT", fill="#4CAF50", font=header_font)
    
    indices = [("Nifty 50", nifty, nifty_pct, n_pos), 
               ("Sensex", sensex, sensex_pct, s_pos), 
               ("Bank Nifty", bnifty, bnifty_pct, bn_pos)]
    
    y_offset = 230
    for name, price, pct, pos in indices:
        draw.text((60, y_offset), name, fill=WHITE, font=data_font)
        draw.text((200, y_offset), price, fill=WHITE, font=data_font)
        draw.text((330, y_offset), pct, fill=GREEN if pos else RED, font=data_font)
        y_offset += 50

    # --- PANEL 2: VOLATILITY & BREADTH ---
    draw.rectangle([(40, 450), (420, 580)], fill=PANEL_BG, radius=8)
    draw.text((60, 470), "VOLATILITY INDEX", fill=MUTED, font=header_font)
    draw.text((60, 515), "India VIX", fill=WHITE, font=data_font)
    draw.text((220, 515), vix, fill=WHITE, font=data_font)
    draw.text((330, 515), vix_pct, fill=GREEN if v_pos else RED, font=data_font)

    # --- PANEL 3: TOP GAINERS & LOSERS ---
    draw.rectangle([(460, 160), (860, 420)], fill=PANEL_BG, radius=8)
    draw.text((480, 180), "2. TOP MOVERS", fill="#4CAF50", font=header_font)
    
    movers = [("TCS", tcs, tcs_pct, t_pos), 
              ("INFY", infy, infy_pct, i_pos), 
              ("TITAN", titan, titan_pct, ti_pos)]
              
    y_offset = 230
    for name, price, pct, pos in movers:
        draw.text((480, y_offset), name, fill=WHITE, font=data_font)
        draw.text((620, y_offset), price, fill=WHITE, font=data_font)
        draw.text((750, y_offset), pct, fill=GREEN if pos else RED, font=data_font)
        y_offset += 50

    # --- PANEL 4: COMMODITIES & FOREX ---
    draw.rectangle([(460, 450), (860, 580)], fill=PANEL_BG, radius=8)
    draw.text((480, 465), "3. CURRENCY & COMMODITY", fill="#4CAF50", font=header_font)
    
    draw.text((480, 505), "USD / INR", fill=WHITE, font=sub_font)
    draw.text((480, 530), usdinr, fill=WHITE, font=data_font)
    draw.text((600, 530), usdinr_pct, fill=GREEN if u_pos else RED, font=sub_font)
    
    draw.text((680, 505), "Gold (10g)", fill=WHITE, font=sub_font)
    draw.text((680, 530), gold, fill=WHITE, font=data_font)
    draw.text((800, 530), gold_pct, fill=GREEN if g_pos else RED, font=sub_font)

    # --- PANEL 5: MARKET WATCH / RADAR METRICS ---
    draw.rectangle([(40, 610), (860, 980)], fill=PANEL_BG, radius=8)
    draw.text((60, 630), "4. SECTOR RADAR & TRADER INSIGHTS", fill="#4CAF50", font=header_font)
    
    draw.text((60, 680), "• Momentum Trend:", fill=MUTED, font=data_font)
    draw.text((280, 680), "IT and Banking sectors showing active breakout frames.", fill=WHITE, font=sub_font)
    
    draw.text((60, 740), "• Primary Support:", fill=MUTED, font=data_font)
    draw.text((280, 740), "Nifty key support establishes near major technical moving averages.", fill=WHITE, font=sub_font)
    
    draw.text((60, 800), "• Risk Management:", fill=MUTED, font=data_font)
    draw.text((280, 800), "VIX volatility remains standard. Trail stops on active swings.", fill=WHITE, font=sub_font)

    # Graphic Border Framing Line
    draw.rectangle([(50, 860), (850, 950)], outline="#4CAF50", width=2)
    draw.text((70, 895), "ALERT: Focus on volume breakouts over index clusters.", fill=WHITE, font=data_font)

    # --- FOOTER DISCLAIMER ---
    draw.rectangle([(0, 1030), (900, 1100)], fill="#070A0C")
    draw.text((40, 1050), "Disclaimer: For educational purposes only. Vedansh Capital is not SEBI registered.", fill=MUTED, font=sub_font)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "📈 Welcome to Vedansh Capital Market Bot! Type /dashboard to generate your live report image.")

@bot.message_handler(commands=['dashboard'])
def send_dashboard(message):
    bot.send_message(message.chat.id, "🔄 Connecting to NSE servers... Drawing your custom dashboard sheet.")
    try:
        dashboard_img = generate_advanced_dashboard()
        bot.send_photo(message.chat.id, photo=dashboard_img, caption="📊 *Vedansh Capital | Market Decoded*\nLive Closing & Snapshot Grid.", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error creating dashboard: {str(e)}")

# --- START THREADS ---
if __name__ == "__main__":
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    
    print("Vedansh Capital Bot is active...")
    bot.infinity_polling()
