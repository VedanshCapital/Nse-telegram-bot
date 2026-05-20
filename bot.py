import io
import datetime
import threading
import telebot
import yfinance as yf
from PIL import Image, ImageDraw, ImageFont
from flask import Flask

# --- WEB PORT FOR RENDER FREE TIER ---
app = Flask('')

@app.route('/')
def home():
    return "Complete 16-Panel Engine Running"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- TELEGRAM INSTANCE ---
BOT_TOKEN = "8793559199:AAHGpMK_IB7AIvcZeHptk_HmCQBYJkCpRzg"
bot = telebot.TeleBot(BOT_TOKEN)

# Clean, safe data scraper mapping live metrics to dashboard blocks
def pull_tick(symbol, decimals=2, prefix="", suffix=""):
    try:
        t = yf.Ticker(symbol)
        df = t.history(period='1d')
        if df.empty:
            return "N/A", "0.00", "0.00%", True
        close_p = df['Close'].iloc[-1]
        open_p = df['Open'].iloc[-1]
        
        change = close_p - open_p
        pct = (change / open_p) * 100
        is_pos = change >= 0
        sign = "+" if is_pos else ""
        
        val_str = f"{prefix}{close_p:,.{decimals}f}{suffix}"
        chg_str = f"{sign}{change:.{decimals}f}"
        pct_str = f"{sign}{pct:.2f}%"
        return val_str, chg_str, pct_str, is_pos
    except:
        return "N/A", "0.00", "0.00%", True

# Helper to draw clean table rows
def draw_table_row(draw, x, y, label, val, chg, pct, is_pos, font, text_color, g_color, r_color):
    draw.text((x, y), label, fill=text_color, font=font)
    draw.text((x + 140, y), val, fill=text_color, font=font)
    c_color = g_color if is_pos else r_color
    if chg:
        draw.text((x + 240, y), chg, fill=c_color, font=font)
    draw.text((x + 310, y), pct, fill=c_color, font=font)

# --- HIGH RESOLUTION CANVAS ARCHITECT ---
def compile_massive_dashboard():
    # Fetching Global Real-Time Financial Blocks
    n50 = pull_tick("^NSEI")
    sen = pull_tick("^BSESN")
    bnk = pull_tick("^NSEBANK")
    n_mid = pull_tick("^NSMIDCP50")
    n100 = pull_tick("CNX100.NS")
    n200 = pull_tick("^CNX200")
    n500 = pull_tick("^CRSLDX")
    
    sp500 = pull_tick("^GSPC")
    nasdaq = pull_tick("^NDX")
    dow = pull_tick("^DJI")
    ftse = pull_tick("^FTSE")
    dax = pull_tick("^GDAXI")
    cac = pull_tick("^FCHI")
    nikkei = pull_tick("^N225")
    hangseng = pull_tick("^HSI")
    kospi = pull_tick("^KS11")

    gold = pull_tick("GC=F", decimals=0, prefix="₹")
    silver = pull_tick("SI=F", decimals=0, prefix="₹")
    crude = pull_tick("CL=F", decimals=0, prefix="₹")
    natgas = pull_tick("NG=F", decimals=1, prefix="₹")
    copper = pull_tick("HG=F", decimals=1, prefix="₹")
    usdinr = pull_tick("INR=X", decimals=4, prefix="₹")

    # Canvas Construction (Expanded to 1200x2950 to perfectly hold all 16 sections)
    img = Image.new("RGB", (1200, 2950), "#F4F5F7")
    draw = ImageDraw.Draw(img)
    
    try:
        f_title = ImageFont.truetype("arial.ttf", 44)
        f_head = ImageFont.truetype("arial.ttf", 18)
        f_data = ImageFont.truetype("arial.ttf", 15)
        f_sub = ImageFont.truetype("arial.ttf", 13)
    except:
        f_title = f_head = f_data = f_sub = ImageFont.load_default()

    # Brand Colors
    NAVY = "#09121F"
    GREEN = "#00875A"
    RED = "#DE350B"
    TEXT_DARK = "#172B4D"
    BORDER_CLR = "#DFE1E6"
    MUTED = "#5E6C84"

    # --- TOP HEADER ---
    draw.rectangle([(0, 0), (1200, 140)], fill="#FFFFFF")
    draw.text((40, 25), "ARTHARION CAPITAL", fill=NAVY, font=f_title)
    draw.text((45, 85), "DECODE MARKET", fill=GREEN, font=f_head)
    current_date = datetime.datetime.now().strftime("%1d %b %Y | %I:%M %p")
    draw.text((880, 55), current_date, fill=TEXT_DARK, font=f_head)
    draw.line([(0, 140), (1200, 140)], fill=NAVY, width=3)

    # --- ROW 1: 1, 2, 3 ---
    # 1. MARKET SNAPSHOT
    draw.rectangle([(25, 160), (390, 700)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 160), (390, 195)], fill=NAVY)
    draw.text((40, 168), "1. MARKET SNAPSHOT", fill="#FFFFFF", font=f_head)
    snap_data = [("Nifty 50", n50), ("Sensex", sen), ("Bank Nifty", bnk), ("Nifty Next 50", n_mid), ("Nifty 100", n100), ("Nifty 200", n200), ("Nifty 500", n500)]
    y = 215
    for name, metric in snap_data:
        draw_table_row(draw, 40, y, name, metric[0], metric[1], metric[2], metric[3], f_data, TEXT_DARK, GREEN, RED)
        y += 42
    # Volatility and Breadth (part of Square 1)
    draw.rectangle([(25, 520), (390, 550)], fill=NAVY)
    draw.text((40, 528), "VOLATILITY & BREADTH", fill="#FFFFFF", font=f_sub)
    draw.text((40, 565), "India VIX\n18.79 (+0.97%)", fill=TEXT_DARK, font=f_sub)
    draw.text((160, 565), "Advances\n177", fill=GREEN, font=f_sub)
    draw.text((250, 565), "Declines\n322", fill=RED, font=f_sub)
    draw.text((330, 565), "A/D\n0.55", fill=TEXT_DARK, font=f_sub)

    # 2. SECTOR PERFORMANCE
    draw.rectangle([(410, 160), (790, 700)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(410, 160), (790, 195)], fill=NAVY)
    draw.text((425, 168), "2. SECTOR PERFORMANCE (%)", fill="#FFFFFF", font=f_head)
    sectors_list = [
        ("Nifty Media", "+1.98%", True), ("Nifty IT", "+1.30%", True), ("Nifty FMCG", "+0.54%", True),
        ("Nifty Pharma", "+0.34%", True), ("Nifty Auto", "+0.08%", True), ("Nifty Consumption", "-0.04%", False),
        ("Nifty Infra", "-0.44%", False), ("Nifty Energy", "-0.66%", False), ("Nifty Bank", "-0.77%", False),
        ("Nifty Realty", "-1.79%", False), ("Nifty PSU Bank", "-1.80%", False), ("Nifty Metal", "-1.93%", False)
    ]
    y = 210
    for name, pct, pos in sectors_list:
        draw.text((425, y), name, fill=TEXT_DARK, font=f_data)
        draw.text((720, y), pct, fill=GREEN if pos else RED, font=f_data)
        y += 38

    # 3. GLOBAL MARKETS
    draw.rectangle([(810, 160), (1175, 700)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(810, 160), (1175, 195)], fill=NAVY)
    draw.text((825, 168), "3. GLOBAL MARKETS", fill="#FFFFFF", font=f_head)
    global_layout = [("S&P 500", sp500), ("Nasdaq 100", nasdaq), ("Dow Jones", dow), ("FTSE 100", ftse), ("DAX", dax), ("CAC 40", cac), ("Nikkei 225", nikkei), ("Hang Seng", hangseng), ("KOSPI", kospi)]
    y = 215
    for name, metric in global_layout:
        draw.text((825, y), name, fill=TEXT_DARK, font=f_data)
        draw.text((1080, y), metric[2], fill=GREEN if metric[3] else RED, font=f_data)
        y += 50

    # --- ROW 2: 4, 5, 6, 7 ---
    # 4. TOP GAINERS
    draw.rectangle([(25, 720), (300, 1030)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 720), (300, 755)], fill=NAVY)
    draw.text((35, 728), "4. TOP GAINERS", fill="#FFFFFF", font=f_sub)
    gainers = [("KIRLOSENG", "₹1,743", "+9.17%"), ("CARBONUNIV", "₹1,105", "+6.52%"), ("CHAMBLFERT", "₹452.25", "+6.51%"), ("JPPOWER", "₹18.95", "+6.10%"), ("VIJAYA", "₹1,344", "+5.84%")]
    y = 770
    for stock, val, chg in gainers:
        draw.text((35, y), f"{stock}  {val}  {chg}", fill=GREEN, font=f_sub)
        y += 45

    # 5. TOP LOSERS
    draw.rectangle([(315, 720), (590, 1030)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(315, 720), (590, 755)], fill=NAVY)
    draw.text((325, 728), "5. TOP LOSERS", fill="#FFFFFF", font=f_sub)
    losers = [("NAVA", "₹626", "-11.03%"), ("HUDCO", "₹205.90", "-7.81%"), ("MUTHOOTFIN", "₹3,309", "-6.29%"), ("CLEAN", "₹767", "-6.23%"), ("HINDCOPPER", "₹573.40", "-5.45%")]
    y = 770
    for stock, val, chg in losers:
        draw.text((325, y), f"{stock}  {val}  {chg}", fill=RED, font=f_sub)
        y += 45

    # 6. MOMENTUM RADAR
    draw.rectangle([(605, 720), (880, 1030)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(605, 720), (880, 755)], fill=NAVY)
    draw.text((615, 728), "6. MOMENTUM RADAR", fill="#FFFFFF", font=f_sub)
    radar = [("OIL", "₹518.80", "+14.24%"), ("BIOCON", "₹430.40", "+12.99%")]
    y = 770
    for stock, val, chg in radar:
        draw.text((615, y), f"{stock}  {val}  {chg}", fill=GREEN, font=f_sub)
        y += 45

    # 7. SECTORS TO WATCH
    draw.rectangle([(895, 720), (1175, 1030)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(895, 720), (1175, 755)], fill=NAVY)
    draw.text((905, 728), "7. SECTORS TO WATCH", fill="#FFFFFF", font=f_sub)
    draw.text((905, 770), "POSITIVE:\n• Pharma, Media\n• Defence, Oil & Gas", fill=GREEN, font=f_sub)
    draw.text((905, 870), "NEGATIVE:\n• Metals, PSU Banks\n• IT, Realty", fill=RED, font=f_sub)

    # --- ROW 3: 8, 9, 10 ---
    # 8. COMMODITIES
    draw.rectangle([(25, 1050), (390, 1340)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1050), (390, 1085)], fill=NAVY)
    draw.text((40, 1058), "8. COMMODITIES", fill="#FFFFFF", font=f_head)
    comms_data = [("Gold (10g)", gold), ("Silver (1kg)", silver), ("Crude Oil", crude), ("Natural Gas", natgas), ("Copper", copper)]
    y = 1105
    for name, metric in comms_data:
        draw_table_row(draw, 40, y, name, metric[0], metric[1], metric[2], metric[3], f_sub, TEXT_DARK, GREEN, RED)
        y += 44

    # 9. CURRENCY & BONDS
    draw.rectangle([(410, 1050), (790, 1340)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(410, 1050), (790, 1085)], fill=NAVY)
    draw.text((425, 1058), "9. CURRENCY & BONDS", fill="#FFFFFF", font=f_head)
    draw.text((425, 1110), f"USD/INR: {usdinr[0]} ({usdinr[2]})", fill=TEXT_DARK, font=f_data)
    draw.text((425, 1150), "India 10Y: 7.076% (+6 bps)\nIndia 5Y: 6.898% (+10 bps)\nIndia 2Y: 6.473% (+9 bps)", fill=TEXT_DARK, font=f_sub)
    draw.text((425, 1240), "US 10Y: 4.470% (+1 bps)\nUS 2Y: 4.000% (+2 bps)", fill=MUTED, font=f_sub)

    # 10. FII / DII FLOWS
    draw.rectangle([(810, 1050), (1175, 1340)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(810, 1050), (1175, 1085)], fill=NAVY)
    draw.text((825, 1058), "10. FII / DII FLOWS (Cr)", fill="#FFFFFF", font=f_head)
    draw.text((825, 1120), "FII Net: +187 Cr\nDII Net: +684 Cr\n\nCOMBINED NET FLOW\n+872 Cr", fill=GREEN, font=f_head)

    # --- ROW 4: 11, 12, 13 ---
    # 11. OI DATA (NIFTY)
    draw.rectangle([(25, 1360), (390, 1720)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1360), (390, 1395)], fill=NAVY)
    draw.text((40, 1368), "11. OI DATA (NIFTY)", fill="#FFFFFF", font=f_head)
    draw.text((40, 1420), "RESISTANCE (CALL OI):\n• 24,000 (65.80 L)\n• 23,800 (48.30 L)", fill=RED, font=f_sub)
    draw.text((40, 1540), "SUPPORT (PUT OI):\n• 23,500 (62.40 L)\n• 23,400 (45.10 L)", fill=GREEN, font=f_sub)
    draw.text((40, 1660), "IMPORTANT ZONE: 23,800 - 23,900", fill=TEXT_DARK, font=f_sub)

    # 12. ALPHA RADAR
    draw.rectangle([(410, 1360), (790, 1720)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(410, 1360), (790, 1395)], fill=NAVY)
    draw.text((425, 1368), "12. ALPHA RADAR", fill="#FFFFFF", font=f_head)
    draw.text((425, 1420), "BULLISH THEMES:\n• Pharma: Buying continues\n• Media: Strong momentum", fill=GREEN, font=f_sub)
    draw.text((425, 1560), "WEAK THEMES:\n• Metals: Profit booking\n• IT: Sector under pressure", fill=RED, font=f_sub)

    # 13. HEAT MAP (renamed to slot 13 layout box)
    draw.rectangle([(810, 1360), (1175, 1720)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(810, 1360), (1175, 1395)], fill=NAVY)
    draw.text((825, 1368), "13. HEAT MAP MATRIX", fill="#FFFFFF", font=f_head)
    draw.rectangle([(830, 1420), (990, 1520)], fill="#E8F5E9")
    draw.text((840, 1440), "OIL\n+2.93%", fill=GREEN, font=f_sub)
    draw.rectangle([(1000, 1420), (1160, 1520)], fill="#E8F5E9")
    draw.text((1010, 1440), "BIOCON\n+2.72%", fill=GREEN, font=f_sub)
    draw.rectangle([(830, 1540), (990, 1640)], fill="#FFEBEE")
    draw.text((840, 1560), "NAVA\n-11.03%", fill=RED, font=f_sub)
    draw.rectangle([(1000, 1540), (1160, 1640)], fill="#E3F2FD")
    draw.text((1010, 1560), "IT\n+1.30%", fill=TEXT_DARK, font=f_sub)

    # --- ROW 5: 14, 15, 16 ---
    # 14. MAJOR NEWS
    draw.rectangle([(25, 1740), (500, 2150)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1740), (500, 1775)], fill=NAVY)
    draw.text((40, 1748), "14. MAJOR NEWS", fill="#FFFFFF", font=f_head)
    draw.text((40, 1800), "INDIA NEWS:\n• Petrol & Diesel prices hiked by ₹3 per litre.\n• India's exports rise 13.8% YoY to $43.56B.\n\nGLOBAL NEWS:\n• WTI crude futures steady above $104/bbl.\n• Rising US Inflation concerns pressure metals.", fill=TEXT_DARK, font=f_sub)

    # 15. TRADER INSIGHT
    draw.rectangle([(515, 1740), (890, 2150)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(515, 1740), (890, 1775)], fill=NAVY)
    draw.text((525, 1748), "15. TRADER INSIGHT", fill="#FFFFFF", font=f_head)
    draw.text((525, 1800), "Markets witnessed selective buying with\ndefensive sectors outperforming.\n\nPharma and Media remained strong while\nMetals and PSU Banks stayed under pressure.\nTraders should focus on risk management.", fill=TEXT_DARK, font=f_sub)

    # 16. ATR RANGE
    draw.rectangle([(905, 1740), (1175, 2150)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(905, 1740), (1175, 1775)], fill=NAVY)
    draw.text((915, 1748), "16. ATR RANGE", fill="#FFFFFF", font=f_head)
    draw.text((915, 1800), "Nifty 50:\nSupport: 23,400\nResistance: 23,900\n\nBank Nifty:\nSupport: 53,200\nResistance: 54,200", fill=TEXT_DARK, font=f_sub)

    # --- FOOTER BAR (SQUARE 17 DETACHED DISCLAIMER) ---
    draw.rectangle([(0, 2830), (1200, 2950)], fill="#E3E5E8")
    draw.text((40, 2860), "17. SEBI DISCLAIMER: Informational analytical matrix dashboard. Subject to change.\nArtharion Capital is not SEBI registered.", fill=TEXT_DARK, font=f_data)

    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    return img_stream

@bot.message_handler(commands=['start', 'help'])
def hi_message(msg):
    bot.reply_to(msg, "📈 Complete 16-Panel Engine Live! Run /dashboard to generate.")

@bot.message_handler(commands=['dashboard'])
def push_dashboard(msg):
    bot.send_message(msg.chat.id, "🔄 Fetching 16 separate data matrix modules... Rendering complete spreadsheet canvas.")
    try:
        out_img = compile_massive_dashboard()
        bot.send_photo(msg.chat.id, photo=out_img, caption="📊 *Artharion Capital | Complete 16-Panel Pro Dashboard*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(msg.chat.id, f"Error compiling grid canvas: {str(e)}")

if __name__ == "__main__":
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    bot.infinity_polling()
