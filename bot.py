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
    return "High-Readability 16-Panel Engine Running"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# --- TELEGRAM INSTANCE ---
BOT_TOKEN = "8793559199:AAHGpMK_IB7AIvcZeHptk_HmCQBYJkCpRzg"
bot = telebot.TeleBot(BOT_TOKEN)

# Stable financial data fallback scraper
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

# Safe row drawing helper with proper vertical spacing and readable colors
def draw_table_row(draw, x, y, label, val, chg, pct, is_pos, font, text_color, g_color, r_color):
    draw.text((x, y), label, fill=text_color, font=font)
    draw.text((x + 160, y), val, fill=text_color, font=font)
    c_color = g_color if is_pos else r_color
    if chg:
        draw.text((x + 280, y), chg, fill=c_color, font=font)
    draw.text((x + 370, y), pct, fill=c_color, font=font)

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

    # High-contrast canvas layout (Large dimensions prevent text overlapping)
    img = Image.new("RGB", (1300, 3100), "#F4F6F9")
    draw = ImageDraw.Draw(img)
    
    try:
        f_title = ImageFont.truetype("arial.ttf", 46)
        f_head = ImageFont.truetype("arial.ttf", 20)
        f_data = ImageFont.truetype("arial.ttf", 17)
        f_sub = ImageFont.truetype("arial.ttf", 15)
    except:
        f_title = f_head = f_data = f_sub = ImageFont.load_default()

    # Exact Color Palette from Reference Image
    NAVY = "#0B1A30"       # High contrast header blocks
    GREEN = "#00875A"      # Clean positive indicator green
    RED = "#DE350B"        # Clean negative indicator red
    TEXT_DARK = "#172B4D"  # Main text color for white cards
    BORDER_CLR = "#DCDFE4" # Subdued boundaries
    MUTED = "#5E6C84"

    # --- MAIN ENGINE TOP HEADER ---
    draw.rectangle([(0, 0), (1300, 150)], fill="#FFFFFF")
    draw.text((40, 25), "ARTHARION CAPITAL", fill=NAVY, font=f_title)
    draw.text((45, 90), "DECODE MARKET", fill=GREEN, font=f_head)
    current_date = datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")
    draw.text((950, 60), current_date, fill=TEXT_DARK, font=f_head)
    draw.line([(0, 150), (1300, 150)], fill=NAVY, width=4)

    # --- ROW 1: CARDS 1, 2, 3 ---
    # 1. MARKET SNAPSHOT
    draw.rectangle([(25, 170), (430, 720)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 170), (430, 210)], fill=NAVY)
    draw.text((40, 180), "1. MARKET SNAPSHOT", fill="#FFFFFF", font=f_head)
    snap_data = [("Nifty 50", n50), ("Sensex", sen), ("Bank Nifty", bnk), ("Nifty Next 50", n_mid), ("Nifty 100", n100), ("Nifty 200", n200), ("Nifty 500", n500)]
    y = 230
    for name, metric in snap_data:
        draw_table_row(draw, 40, y, name, metric[0], metric[1], metric[2], metric[3], f_data, TEXT_DARK, GREEN, RED)
        y += 45
        
    # Volatility and Breadth (Embedded inside Snapshot block)
    draw.rectangle([(25, 550), (430, 585)], fill=NAVY)
    draw.text((40, 558), "VOLATILITY & BREADTH", fill="#FFFFFF", font=f_sub)
    draw.text((40, 605), "India VIX\n18.79 (+0.97%)", fill=TEXT_DARK, font=f_sub)
    draw.text((180, 605), "Advances\n177", fill=GREEN, font=f_sub)
    draw.text((270, 605), "Declines\n322", fill=RED, font=f_sub)
    draw.text((360, 605), "A/D\n0.55", fill=TEXT_DARK, font=f_sub)

    # 2. SECTOR PERFORMANCE
    draw.rectangle([(450, 170), (850, 720)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(450, 170), (850, 210)], fill=NAVY)
    draw.text((465, 180), "2. SECTOR PERFORMANCE (%)", fill="#FFFFFF", font=f_head)
    sectors_list = [
        ("Nifty Media", "+1.98%", True), ("Nifty IT", "+1.30%", True), ("Nifty FMCG", "+0.54%", True),
        ("Nifty Pharma", "+0.34%", True), ("Nifty Auto", "+0.08%", True), ("Nifty Consumption", "-0.04%", False),
        ("Nifty Infra", "-0.44%", False), ("Nifty Energy", "-0.66%", False), ("Nifty Bank", "-0.77%", False),
        ("Nifty Realty", "-1.79%", False), ("Nifty PSU Bank", "-1.80%", False), ("Nifty Metal", "-1.93%", False)
    ]
    y = 225
    for name, pct, pos in sectors_list:
        draw.text((465, y), name, fill=TEXT_DARK, font=f_data)
        draw.text((750, y), pct, fill=GREEN if pos else RED, font=f_data)
        y += 40

    # 3. GLOBAL MARKETS
    draw.rectangle([(870, 170), (1275, 720)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(870, 170), (1275, 210)], fill=NAVY)
    draw.text((885, 180), "3. GLOBAL MARKETS", fill="#FFFFFF", font=f_head)
    global_layout = [("S&P 500", sp500), ("Nasdaq 100", nasdaq), ("Dow Jones", dow), ("FTSE 100", ftse), ("DAX", dax), ("CAC 40", cac), ("Nikkei 225", nikkei), ("Hang Seng", hangseng), ("KOSPI", kospi)]
    y = 230
    for name, metric in global_layout:
        draw.text((885, y), name, fill=TEXT_DARK, font=f_data)
        draw.text((1160, y), metric[2], fill=GREEN if metric[3] else RED, font=f_data)
        y += 52

    # --- ROW 2: CARDS 4, 5, 6, 7 ---
    # 4. TOP GAINERS
    draw.rectangle([(25, 740), (320, 1070)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 740), (320, 775)], fill=NAVY)
    draw.text((35, 748), "4. TOP GAINERS", fill="#FFFFFF", font=f_sub)
    gainers = [("KIRLOSENG", "₹1,743", "+9.17%"), ("CARBONUNIV", "₹1,105", "+6.52%"), ("CHAMBLFERT", "₹452.25", "+6.51%"), ("JPPOWER", "₹18.95", "+6.10%"), ("VIJAYA", "₹1,344", "+5.84%")]
    y = 790
    for stock, val, chg in gainers:
        draw.text((35, y), f"{stock}\n{val} ({chg})", fill=GREEN, font=f_sub)
        y += 52

    # 5. TOP LOSERS
    draw.rectangle([(340, 740), (635, 1070)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(340, 740), (635, 775)], fill=NAVY)
    draw.text((350, 748), "5. TOP LOSERS", fill="#FFFFFF", font=f_sub)
    losers = [("NAVA", "₹626", "-11.03%"), ("HUDCO", "₹205.90", "-7.81%"), ("MUTHOOTFIN", "₹3,309", "-6.29%"), ("CLEAN", "₹767", "-6.23%"), ("HINDCOPPER", "₹573.40", "-5.45%")]
    y = 790
    for stock, val, chg in losers:
        draw.text((350, y), f"{stock}\n{val} ({chg})", fill=RED, font=f_sub)
        y += 52

    # 6. MOMENTUM RADAR
    draw.rectangle([(655, 740), (950, 1070)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(655, 740), (950, 775)], fill=NAVY)
    draw.text((665, 748), "6. MOMENTUM RADAR", fill="#FFFFFF", font=f_sub)
    radar = [("OIL", "₹518.80", "+14.24%"), ("BIOCON", "₹430.40", "+12.99%")]
    y = 790
    for stock, val, chg in radar:
        draw.text((665, y), f"{stock}\n{val} ({chg})", fill=GREEN, font=f_sub)
        y += 55

    # 7. SECTORS TO WATCH
    draw.rectangle([(970, 740), (1275, 1070)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(970, 740), (1275, 775)], fill=NAVY)
    draw.text((980, 748), "7. SECTORS TO WATCH", fill="#FFFFFF", font=f_sub)
    draw.text((980, 790), "POSITIVE:\n• Pharma, Media\n• Defence, Oil & Gas", fill=GREEN, font=f_sub)
    draw.text((980, 895), "NEGATIVE:\n• Metals, PSU Banks\n• IT, Realty", fill=RED, font=f_sub)

    # --- ROW 3: CARDS 8, 9, 10 ---
    # 8. COMMODITIES
    draw.rectangle([(25, 1090), (430, 1390)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1090), (430, 1125)], fill=NAVY)
    draw.text((40, 1098), "8. COMMODITIES", fill="#FFFFFF", font=f_head)
    comms_data = [("Gold (10g)", gold), ("Silver (1kg)", silver), ("Crude Oil", crude), ("Natural Gas", natgas), ("Copper", copper)]
    y = 1145
    for name, metric in comms_data:
        draw_table_row(draw, 40, y, name, metric[0], metric[1], metric[2], metric[3], f_sub, TEXT_DARK, GREEN, RED)
        y += 46

    # 9. CURRENCY & BONDS
    draw.rectangle([(450, 1090), (850, 1390)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(450, 1090), (850, 1125)], fill=NAVY)
    draw.text((465, 1098), "9. CURRENCY & BONDS", fill="#FFFFFF", font=f_head)
    draw.text((465, 1145), f"USD/INR: {usdinr[0]} ({usdinr[2]})", fill=TEXT_DARK, font=f_data)
    draw.text((465, 1185), "India 10Y: 7.076% (+6 bps)\nIndia 5Y: 6.898% (+10 bps)\nIndia 2Y: 6.473% (+9 bps)", fill=TEXT_DARK, font=f_sub)
    draw.text((465, 1285), "US 10Y: 4.470% (+1 bps)\nUS 2Y: 4.000% (+2 bps)", fill=MUTED, font=f_sub)

    # 10. FII / DII FLOWS
    draw.rectangle([(870, 1090), (1275, 1390)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(870, 1090), (1275, 1125)], fill=NAVY)
    draw.text((885, 1098), "10. FII / DII FLOWS (Cr)", fill="#FFFFFF", font=f_head)
    draw.text((885, 1150), "FII Net Session: +187 Cr\nDII Net Session: +684 Cr\n\nCOMBINED SESSION FLOW:\n+872 Cr", fill=GREEN, font=f_head)

    # --- ROW 4: CARDS 11, 12, 13 ---
    # 11. OI DATA (NIFTY)
    draw.rectangle([(25, 1410), (430, 1780)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1410), (430, 1445)], fill=NAVY)
    draw.text((40, 1418), "11. OI DATA (NIFTY)", fill="#FFFFFF", font=f_head)
    draw.text((40, 1465), "RESISTANCE (CALL OI):\n• 24,000 (65.80 L)\n• 23,800 (48.30 L)", fill=RED, font=f_sub)
    draw.text((40, 1585), "SUPPORT (PUT OI):\n• 23,500 (62.40 L)\n• 23,400 (45.10 L)", fill=GREEN, font=f_sub)
    draw.text((40, 1715), "IMPORTANT ZONE: 23,800 - 23,900", fill=TEXT_DARK, font=f_sub)

    # 12. ALPHA RADAR
    draw.rectangle([(450, 1410), (850, 1780)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(450, 1410), (850, 1445)], fill=NAVY)
    draw.text((465, 1418), "12. ALPHA RADAR", fill="#FFFFFF", font=f_head)
    draw.text((465, 1465), "BULLISH THEMES:\n• Pharma: Defensive buying continues\n• Media: Strong sector momentum\n• Defence: UAE investment boost", fill=GREEN, font=f_sub)
    draw.text((465, 1615), "WEAK THEMES:\n• Metals: Profit booking after rally\n• PSU Banks: Weakness continues\n• IT: Sector under pressure", fill=RED, font=f_sub)

    # 13. HEAT MAP MATRIX
    draw.rectangle([(870, 1410), (1275, 1780)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(870, 1410), (1275, 1445)], fill=NAVY)
    draw.text((885, 1418), "13. HEAT MAP MATRIX", fill="#FFFFFF", font=f_head)
    
    # 4 distinct internal blocks with fallback border drawing instead of radius
    draw.rectangle([(885, 1465), (1060, 1565)], fill="#E8F5E9")
    draw.text((895, 1490), "OIL\n+2.93%", fill=GREEN, font=f_sub)
    draw.rectangle([(1080, 1465), (1255, 1565)], fill="#E8F5E9")
    draw.text((1090, 1490), "BIOCON\n+2.72%", fill=GREEN, font=f_sub)
    draw.rectangle([(885, 1585), (1060, 1685)], fill="#FFEBEE")
    draw.text((895, 1610), "NAVA\n-11.03%", fill=RED, font=f_sub)
    draw.rectangle([(1080, 1585), (1255, 1685)], fill="#E3F2FD")
    draw.text((1090, 1610), "IT CLUSTER\n+1.30%", fill=TEXT_DARK, font=f_sub)

    # --- ROW 5: CARDS 14, 15, 16 ---
    # 14. MAJOR NEWS
    draw.rectangle([(25, 1800), (520, 2220)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1800), (520, 1835)], fill=NAVY)
    draw.text((40, 1808), "14. MAJOR NEWS", fill="#FFFFFF", font=f_head)
    draw.text((40, 1855), "INDIA NEWS:\n• Petrol & Diesel prices hiked by ₹3 per litre.\n• India's exports rise 13.8% YoY to $43.56B.\n\nGLOBAL NEWS:\n• WTI crude futures steady above $104/bbl.\n• Rising US Inflation concerns pressure metals.", fill=TEXT_DARK, font=f_sub)

    # 15. TRADER INSIGHT
    draw.rectangle([(540, 1800), (920, 2220)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(540, 1800), (920, 1835)], fill=NAVY)
    draw.text((550, 1808), "15. TRADER INSIGHT", fill="#FFFFFF", font=f_head)
    draw.text((550, 1855), "Markets witnessed selective buying with\ndefensive sectors outperforming.\n\nPharma and Media remained strong while\nMetals and PSU Banks stayed under pressure.\nTraders should focus on risk management.", fill=TEXT_DARK, font=f_sub)

    # 16. ATR RANGE
    draw.rectangle([(940, 1800), (1275, 2220)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(940, 1800), (1275, 1835)], fill=NAVY)
    draw.text((950, 1808), "16. ATR RANGE", fill="#FFFFFF", font=f_head)
    draw.text((950, 1855), "Nifty 50:\nSupport: 23,400\nResistance: 23,900\n\nBank Nifty:\nSupport: 53,200\nResistance: 54,200", fill=TEXT_DARK, font=f_sub)

    # --- SEBI DISCLAIMER FOOTER ---
    draw.rectangle([(0, 2980), (1300, 3100)], fill="#E3E5E8")
    draw.text((40, 3010), "17. SEBI DISCLAIMER: Informational analytical matrix dashboard. Subject to change.\nArtharion Capital is not SEBI registered.", fill=TEXT_DARK, font=f_data)

    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    return img_stream

@bot.message_handler(commands=['start', 'help'])
def hi_message(msg):
    bot.reply_to(msg, "📈 High-Readability Engine is Live! Run /dashboard to generate your report.")

@bot.message_handler(commands=['dashboard'])
def push_dashboard(msg):
    bot.send_message(msg.chat.id, "🔄 Connecting to data matrix modules... Rendering legible canvas sheets.")
    try:
        out_img = compile_massive_dashboard()
        bot.send_photo(msg.chat.id, photo=out_img, caption="📊 *Artharion Capital | Market Pro Dashboard*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(msg.chat.id, f"Error compiling grid canvas: {str(e)}")

if __name__ == "__main__":
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    bot.infinity_polling()
