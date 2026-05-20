import io
import os
import datetime
import threading
import telebot
import requests
import yfinance as yf
from PIL import Image, ImageDraw, ImageFont
from flask import Flask

# --- WEB OVERLAY FOR RUNTIME ALIVE SIGNALS ---
app = Flask('')

@app.route('/')
def home():
    return "Vedansh Capital Core Active"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- TELEGRAM DEPLOYMENT CREDENTIALS ---
BOT_TOKEN = "8793559199:AAHGpMK_IB7AIvcZeHptk_HmCQBYJkCpRzg"
bot = telebot.TeleBot(BOT_TOKEN)

# --- SYSTEM-INDEPENDENT HIGH-DEFINITION FONT BUILDER ---
FONT_FILE = "LiberationSans-Bold.ttf"
if not os.path.exists(FONT_FILE):
    try:
        r = requests.get("https://github.com/liberationfonts/liberation-fonts/raw/master/LiberationSans-Bold.ttf", timeout=15)
        with open(FONT_FILE, "wb") as f:
            f.write(r.content)
    except Exception:
        FONT_FILE = None

def grab_font(size_px):
    if FONT_FILE:
        try:
            return ImageFont.truetype(FONT_FILE, size_px)
        except:
            pass
    return ImageFont.load_default()

# --- FINANCIAL BACKEND SCRAPER ---
def fetch_ticker_packet(symbol, precision=2, lead_symbol="", tail_symbol=""):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period='1d')
        if df.empty:
            return "N/A", "0.00", "0.00%", True
        close_val = df['Close'].iloc[-1]
        open_val = df['Open'].iloc[-1]
        
        diff = close_val - open_val
        ratio = (diff / open_val) * 100
        is_green = diff >= 0
        prefix_sign = "+" if is_green else ""
        
        amt_str = f"{lead_symbol}{close_val:,.{precision}f}{tail_symbol}"
        diff_str = f"{prefix_sign}{diff:.{precision}f}"
        ratio_str = f"{prefix_sign}{ratio:.2f}%"
        return amt_str, diff_str, ratio_str, is_green
    except Exception:
        return "N/A", "0.00", "0.00%", True

# --- COLUMN GRID CALIBRATION ENGINE ---
def place_table_row(draw, start_x, current_y, label, price, variation, percent, is_green, font_set, color_main, color_g, color_r):
    accent_color = color_g if is_green else color_r
    # Explicit pixel anchors to ensure alignment across multiple devices
    draw.text((start_x + 20, current_y), str(label), fill=color_main, font=font_set)
    draw.text((start_x + 200, current_y), str(price), fill=color_main, font=font_set)
    if variation:
        draw.text((start_x + 315, current_y), str(variation), fill=accent_color, font=font_set)
    draw.text((start_x + 415, current_y), str(percent), fill=accent_color, font=font_set)

def build_high_vis_dashboard():
    # Scraping Real-time Market Vectors
    n50 = fetch_ticker_packet("^NSEI")
    sen = fetch_ticker_packet("^BSESN")
    bnk = fetch_ticker_packet("^NSEBANK")
    n_mid = fetch_ticker_packet("^NSMIDCP50")
    n100 = fetch_ticker_packet("CNX100.NS")
    n200 = fetch_ticker_packet("^CNX200")
    n500 = fetch_ticker_packet("^CRSLDX")
    
    sp500 = fetch_ticker_packet("^GSPC")
    nasdaq = fetch_ticker_packet("^NDX")
    dow = fetch_ticker_packet("^DJI")
    ftse = fetch_ticker_packet("^FTSE")
    dax = fetch_ticker_packet("^GDAXI")
    cac = fetch_ticker_packet("^FCHI")
    nikkei = fetch_ticker_packet("^N225")
    hangseng = fetch_ticker_packet("^HSI")
    kospi = fetch_ticker_packet("^KS11")

    gold = fetch_ticker_packet("GC=F", precision=0, lead_symbol="₹")
    silver = fetch_ticker_packet("SI=F", precision=0, lead_symbol="₹")
    crude = fetch_ticker_packet("CL=F", precision=0, lead_symbol="₹")
    natgas = fetch_ticker_packet("NG=F", precision=1, lead_symbol="₹")
    copper = fetch_ticker_packet("HG=F", precision=1, lead_symbol="₹")
    usdinr = fetch_ticker_packet("INR=X", precision=4, lead_symbol="₹")

    # High contrast base layout sheets
    canvas = Image.new("RGB", (1550, 3250), "#F4F6F9")
    ctx = ImageDraw.Draw(canvas)
    
    # Scale allocations to maximize readability
    f_mega = grab_font(58)
    f_title = grab_font(30)
    f_body = grab_font(21)
    f_mini = grab_font(19)

    COLOR_NAVY = "#0B1A30"       
    COLOR_GREEN = "#00875A"      
    COLOR_RED = "#DE350B"        
    COLOR_CHARCOAL = "#172B4D"  
    COLOR_FRAME = "#DCDFE4" 

    # --- BRAND CORRECTIONS BLOCK ---
    ctx.rectangle([(0, 0), (1550, 170)], fill="#FFFFFF")
    ctx.text((50, 35), "VEDANSH CAPITAL", fill=COLOR_NAVY, font=f_mega)
    ctx.text((55, 110), "DECODE MARKET", fill=COLOR_GREEN, font=f_title)
    timestamp = datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")
    ctx.text((1120, 70), timestamp, fill=COLOR_CHARCOAL, font=f_title)
    ctx.line([(0, 170), (1550, 170)], fill=COLOR_NAVY, width=6)

    # --- ROW 1 LAYOUT (PANELS 1, 2, 3) ---
    # Block 1: Snapshot
    ctx.rectangle([(30, 200), (510, 790)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(30, 200), (510, 255)], fill=COLOR_NAVY)
    ctx.text((50, 212), "1. MARKET SNAPSHOT", fill="#FFFFFF", font=f_title)
    snapshots = [("Nifty 50", n50), ("Sensex", sen), ("Bank Nifty", bnk), ("Nifty Next 50", n_mid), ("Nifty 100", n100), ("Nifty 200", n200), ("Nifty 500", n500)]
    idx_y = 280
    for label, metrics in snapshots:
        place_table_row(ctx, 30, idx_y, label, metrics[0], metrics[1], metrics[2], metrics[3], f_body, COLOR_CHARCOAL, COLOR_GREEN, COLOR_RED)
        idx_y += 52
        
    # Volatility sub-segment
    ctx.rectangle([(30, 650), (510, 690)], fill=COLOR_NAVY)
    ctx.text((50, 660), "VOLATILITY & BREADTH", fill="#FFFFFF", font=f_mini)
    ctx.text((50, 710), "India VIX\n18.79 (+0.97%)", fill=COLOR_CHARCOAL, font=f_mini)
    ctx.text((210, 710), "Advances\n177", fill=COLOR_GREEN, font=f_mini)
    ctx.text((310, 710), "Declines\n322", fill=COLOR_RED, font=f_mini)
    ctx.text((410, 710), "A/D\n0.55", fill=COLOR_CHARCOAL, font=f_mini)

    # Block 2: Sector Matrix
    ctx.rectangle([(540, 200), (990, 790)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(540, 200), (990, 255)], fill=COLOR_NAVY)
    ctx.text((560, 212), "2. SECTOR PERFORMANCE (%)", fill="#FFFFFF", font=f_title)
    sectors_map = [
        ("Nifty Media", "+1.98%", True), ("Nifty IT", "+1.30%", True), ("Nifty FMCG", "+0.54%", True),
        ("Nifty Pharma", "+0.34%", True), ("Nifty Auto", "+0.08%", True), ("Nifty Consumption", "-0.04%", False),
        ("Nifty Infra", "-0.44%", False), ("Nifty Energy", "-0.66%", False), ("Nifty Bank", "-0.77%", False),
        ("Nifty Realty", "-1.79%", False), ("Nifty PSU Bank", "-1.80%", False), ("Nifty Metal", "-1.93%", False)
    ]
    idx_y = 275
    for label, percent, is_green in sectors_map:
        ctx.text((560, idx_y), label, fill=COLOR_CHARCOAL, font=f_body)
        ctx.text((875, idx_y), percent, fill=COLOR_GREEN if is_green else COLOR_RED, font=f_body)
        idx_y += 42

    # Block 3: Global Grid
    ctx.rectangle([(1020, 200), (1510, 790)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(1020, 200), (1510, 255)], fill=COLOR_NAVY)
    ctx.text((1040, 212), "3. GLOBAL MARKETS", fill="#FFFFFF", font=f_title)
    global_map = [("S&P 500", sp500), ("Nasdaq 100", nasdaq), ("Dow Jones", dow), ("FTSE 100", ftse), ("DAX", dax), ("CAC 40", cac), ("Nikkei 225", nikkei), ("Hang Seng", hangseng), ("KOSPI", kospi)]
    idx_y = 280
    for label, metrics in global_map:
        ctx.text((1040, idx_y), label, fill=COLOR_CHARCOAL, font=f_body)
        ctx.text((1360, idx_y), metrics[2], fill=COLOR_GREEN if metrics[3] else COLOR_RED, font=f_body)
        idx_y += 54

    # --- ROW 2 LAYOUT (PANELS 4, 5, 6, 7) ---
    # Block 4: Gainers
    ctx.rectangle([(30, 820), (380, 1180)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(30, 820), (380, 870)], fill=COLOR_NAVY)
    ctx.text((50, 832), "4. TOP GAINERS", fill="#FFFFFF", font=f_mini)
    gainers = [("KIRLOSENG", "1,743", "+9.17%"), ("CARBONUNIV", "1,105", "+6.52%"), ("CHAMBLFERT", "452.25", "+6.51%"), ("JPPOWER", "18.95", "+6.10%"), ("VIJAYA", "1,344", "+5.84%")]
    idx_y = 890
    for label, val, variation in gainers:
        ctx.text((50, idx_y), f"{label:<12} {val:>6} ({variation})", fill=COLOR_GREEN, font=f_mini)
        idx_y += 56

    # Block 5: Losers
    ctx.rectangle([(410, 820), (760, 1180)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(410, 820), (760, 870)], fill=COLOR_NAVY)
    ctx.text((425, 832), "5. TOP LOSERS", fill="#FFFFFF", font=f_mini)
    losers = [("NAVA", "626", "-11.03%"), ("HUDCO", "205.90", "-7.81%"), ("MUTHOOTFIN", "3,309", "-6.29%"), ("CLEAN", "767", "-6.23%"), ("HINDCOPPER", "573.40", "-5.45%")]
    idx_y = 890
    for label, val, variation in losers:
        ctx.text((425, idx_y), f"{label:<12} {val:>6} ({variation})", fill=COLOR_RED, font=f_mini)
        idx_y += 56

    # Block 6: Momentum
    ctx.rectangle([(790, 820), (1140, 1180)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(790, 820), (1140, 870)], fill=COLOR_NAVY)
    ctx.text((805, 832), "6. MOMENTUM RADAR", fill="#FFFFFF", font=f_mini)
    radar = [("OIL", "518.80", "+14.24%"), ("BIOCON", "430.40", "+12.99%")]
    idx_y = 890
    for label, val, variation in radar:
        ctx.text((805, idx_y), f"{label:<12} {val:>6} ({variation})", fill=COLOR_GREEN, font=f_mini)
        idx_y += 58

    # Block 7: Watchlist
    ctx.rectangle([(1170, 820), (1510, 1180)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(1170, 820), (1510, 870)], fill=COLOR_NAVY)
    ctx.text((1185, 832), "7. SECTORS TO WATCH", fill="#FFFFFF", font=f_mini)
    ctx.text((1185, 890), "POSITIVE:\n• Pharma, Media\n• Defence, Oil & Gas", fill=COLOR_GREEN, font=f_mini)
    ctx.text((1185, 1005), "NEGATIVE:\n• Metals, PSU Banks\n• IT, Realty", fill=COLOR_RED, font=f_mini)

    # --- ROW 3 LAYOUT (PANELS 8, 9, 10) ---
    # Block 8: Commodities
    ctx.rectangle([(30, 1210), (510, 1530)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(30, 1210), (510, 1260)], fill=COLOR_NAVY)
    ctx.text((50, 1222), "8. COMMODITIES", fill="#FFFFFF", font=f_title)
    comms = [("Gold (10g)", gold), ("Silver (1kg)", silver), ("Crude Oil", crude), ("Natural Gas", natgas), ("Copper", copper)]
    idx_y = 1280
    for label, metrics in comms:
        place_table_row(ctx, 30, idx_y, label, metrics[0], metrics[1], metrics[2], metrics[3], f_mini, COLOR_CHARCOAL, COLOR_GREEN, COLOR_RED)
        idx_y += 48

    # Block 9: Bonds
    ctx.rectangle([(540, 1210), (990, 1530)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(540, 1210), (990, 1260)], fill=COLOR_NAVY)
    ctx.text((560, 1222), "9. CURRENCY & BONDS", fill="#FFFFFF", font=f_title)
    ctx.text((560, 1280), f"USD/INR: {usdinr[0]} ({usdinr[2]})", fill=COLOR_CHARCOAL, font=f_body)
    ctx.text((560, 1330), "India 10Y: 7.076% (+6 bps)\nIndia 5Y: 6.898% (+10 bps)\nIndia 2Y: 6.473% (+9 bps)", fill=COLOR_CHARCOAL, font=f_mini)
    ctx.text((560, 1455), "US 10Y: 4.470% (+1 bps) | US 2Y: 4.000% (+2 bps)", fill="#5E6C84", font=f_mini)

    # Block 10: Institutional Flow
    ctx.rectangle([(1020, 1210), (1510, 1530)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(1020, 1210), (1510, 1260)], fill=COLOR_NAVY)
    ctx.text((1040, 1222), "10. FII / DII FLOWS (Cr)", fill="#FFFFFF", font=f_title)
    ctx.text((1040, 1290), "FII Net Session: +187 Cr\nDII Net Session: +684 Cr\n\nCOMBINED SESSION FLOW:\n+872 Cr", fill=COLOR_GREEN, font=f_title)

    # --- ROW 4 LAYOUT (PANELS 11, 12, 13) ---
    # Block 11: Derivatives OI
    ctx.rectangle([(30, 1560), (510, 1960)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(30, 1560), (510, 1610)], fill=COLOR_NAVY)
    ctx.text((50, 1572), "11. OI DATA (NIFTY)", fill="#FFFFFF", font=f_title)
    ctx.text((50, 1630), "RESISTANCE (CALL OI):\n• 24,000 (65.80 L)\n• 23,800 (48.30 L)", fill=COLOR_RED, font=f_mini)
    ctx.text((50, 1750), "SUPPORT (PUT OI):\n• 23,500 (62.40 L)\n• 23,400 (45.10 L)", fill=COLOR_GREEN, font=f_mini)

    # Block 12: Alpha Setup
    ctx.rectangle([(540, 1560), (990, 1960)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(540, 1560), (990, 1610)], fill=COLOR_NAVY)
    ctx.text((560, 1572), "12. ALPHA RADAR", fill="#FFFFFF", font=f_title)
    ctx.text((560, 1630), "BULLISH THEMES:\n• Pharma: Defensive accumulation\n• Media: Strong breakout velocity", fill=COLOR_GREEN, font=f_mini)
    ctx.text((560, 1780), "WEAK THEMES:\n• Metals: Sudden distribution overhead\n• IT: Relative strength stalling", fill=COLOR_RED, font=f_mini)

    # Block 13: Matrix
    ctx.rectangle([(1020, 1560), (1510, 1960)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(1020, 1560), (1510, 1610)], fill=COLOR_NAVY)
    ctx.text((1040, 1572), "13. HEAT MAP MATRIX", fill="#FFFFFF", font=f_title)
    
    ctx.rectangle([(1040, 1630), (1250, 1750)], fill="#E8F5E9")
    ctx.text((1055, 1665), "OIL\n+2.93%", fill=COLOR_GREEN, font=f_mini)
    ctx.rectangle([(1280, 1630), (1490, 1750)], fill="#E8F5E9")
    ctx.text((1295, 1665), "BIOCON\n+2.72%", fill=COLOR_GREEN, font=f_mini)
    ctx.rectangle([(1040, 1780), (1250, 1900)], fill="#FFEBEE")
    ctx.text((1055, 1815), "NAVA\n-11.03%", fill=COLOR_RED, font=f_mini)
    ctx.rectangle([(1280, 1780), (1490, 1900)], fill="#E3F2FD")
    ctx.text((1295, 1815), "IT MATRIX\n+1.30%", fill=COLOR_CHARCOAL, font=f_mini)

    # --- ROW 5 LAYOUT (PANELS 14, 15, 16) ---
    # Block 14: Desk Feed
    ctx.rectangle([(30, 1990), (520, 2430)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(30, 1990), (520, 2035)], fill=COLOR_NAVY)
    ctx.text((50, 2002), "14. MAJOR NEWS", fill="#FFFFFF", font=f_title)
    ctx.text((50, 2060), "INDIA FEED:\n• Fuel distribution pricing spikes across states.\n• Export registers high double-digit boost.\n\nGLOBAL FEED:\n• WTI crude indicators solidify above bounds.\n• Inflation revisions keep gold under pressure.", fill=COLOR_CHARCOAL, font=f_mini)

    # Block 15: Desk Interpretation
    ctx.rectangle([(550, 1990), (980, 2430)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(550, 1990), (980, 2035)], fill=COLOR_NAVY)
    ctx.text((565, 2002), "15. TRADER INSIGHT", fill="#FFFFFF", font=f_title)
    ctx.text((565, 2060), "Volume profiles display highly defensive allocation\nstrategies across index heavyweights.\n\nPharma momentum leads key metrics while cyclical positions\nshould watch critical volatility markers closely.", fill=COLOR_CHARCOAL, font=f_mini)

    # Block 16: Volatility Ranges
    ctx.rectangle([(1010, 1990), (1510, 2430)], fill="#FFFFFF", outline=COLOR_FRAME, width=3)
    ctx.rectangle([(1010, 1990), (1510, 2035)], fill=COLOR_NAVY)
    ctx.text((1025, 2002), "16. ATR RANGE", fill="#FFFFFF", font=f_title)
    ctx.text((1025, 2060), "Nifty 50 Index:\nFloor Target: 23,400\nCeiling Boundary: 23,900\n\nBank Nifty Index:\nFloor Target: 53,200\nCeiling Boundary: 54,200", fill=COLOR_CHARCOAL, font=f_mini)

    # --- SEBI REGULATORY FOOTER ---
    ctx.rectangle([(0, 3080), (1550, 3250)], fill="#E3E5E8")
    ctx.text((50, 3120), "17. SEBI REGULATORY NOTICE: Informational operational matrix. Analytical tools only.\nVedansh Capital holds no independent operational registration proxy.", fill=COLOR_CHARCOAL, font=f_body)

    buffer = io.BytesIO()
    canvas.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

@bot.message_handler(commands=['start', 'help'])
def greeting_prompt(msg):
    bot.reply_to(msg, "📈 Vedansh Capital Pro Core Online. Hit /dashboard to print the canvas sheets.")

@bot.message_handler(commands=['dashboard'])
def generate_and_dispatch(msg):
    bot.send_message(msg.chat.id, "🔄 Synchronizing matrix layout grids... Binding font structures cleanly.")
    try:
        render_output = build_high_vis_dashboard()
        bot.send_photo(msg.chat.id, photo=render_output, caption="📊 *Vedansh Capital | High-Visibility Master Sheet*", parse_mode="Markdown")
    except Exception as error_msg:
        bot.send_message(msg.chat.id, f"Core Engine Interrupted: {str(error_msg)}")

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    bot.infinity_polling()
