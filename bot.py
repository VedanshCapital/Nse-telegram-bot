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
    return "Vedansh Capital Engine Running"

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

# Safe row drawing helper with broad column tracking to prevent overlap
def draw_table_row(draw, x_base, y, label, val, chg, pct, is_pos, font, text_color, g_color, r_color):
    c_color = g_color if is_pos else r_color
    # Evenly space components across the width of the card panel
    draw.text((x_base, y), label, fill=text_color, font=font)
    draw.text((x_base + 150, y), val, fill=text_color, font=font)
    if chg:
        draw.text((x_base + 260, y), chg, fill=c_color, font=font)
    draw.text((x_base + 340, y), pct, fill=c_color, font=font)

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
    img = Image.new("RGB", (1400, 3100), "#F4F6F9")
    draw = ImageDraw.Draw(img)
    
    try:
        f_title = ImageFont.truetype("arial.ttf", 52)
        f_head = ImageFont.truetype("arial.ttf", 22)
        f_data = ImageFont.truetype("arial.ttf", 18)
        f_sub = ImageFont.truetype("arial.ttf", 16)
    except:
        f_title = f_head = f_data = f_sub = ImageFont.load_default()

    # Brand Colors
    NAVY = "#0B1A30"       # High contrast header blocks
    GREEN = "#00875A"      # Clean positive indicator green
    RED = "#DE350B"        # Clean negative indicator red
    TEXT_DARK = "#172B4D"  # Main text color for white cards
    BORDER_CLR = "#DCDFE4" # Subdued boundaries
    MUTED = "#5E6C84"

    # --- BRAND CORRECTION HEADER ---
    draw.rectangle([(0, 0), (1400, 150)], fill="#FFFFFF")
    draw.text((40, 25), "VEDANSH CAPITAL", fill=NAVY, font=f_title)
    draw.text((45, 95), "DECODE MARKET", fill=GREEN, font=f_head)
    current_date = datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")
    draw.text((1020, 60), current_date, fill=TEXT_DARK, font=f_head)
    draw.line([(0, 150), (1400, 150)], fill=NAVY, width=4)

    # --- ROW 1: CARDS 1, 2, 3 ---
    # 1. MARKET SNAPSHOT
    draw.rectangle([(25, 170), (460, 740)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 170), (460, 215)], fill=NAVY)
    draw.text((40, 182), "1. MARKET SNAPSHOT", fill="#FFFFFF", font=f_head)
    snap_data = [("Nifty 50", n50), ("Sensex", sen), ("Bank Nifty", bnk), ("Nifty Next 50", n_mid), ("Nifty 100", n100), ("Nifty 200", n200), ("Nifty 500", n500)]
    y = 240
    for name, metric in snap_data:
        draw_table_row(draw, 40, y, name, metric[0], metric[1], metric[2], metric[3], f_data, TEXT_DARK, GREEN, RED)
        y += 46
        
    # Volatility and Breadth (Aligned carefully inside Snapshot block)
    draw.rectangle([(25, 575), (460, 615)], fill=NAVY)
    draw.text((40, 585), "VOLATILITY & BREADTH", fill="#FFFFFF", font=f_sub)
    draw.text((40, 640), "India VIX\n18.79 (+0.97%)", fill=TEXT_DARK, font=f_sub)
    draw.text((190, 640), "Advances\n177", fill=GREEN, font=f_sub)
    draw.text((280, 640), "Declines\n322", fill=RED, font=f_sub)
    draw.text((370, 640), "A/D\n0.55", fill=TEXT_DARK, font=f_sub)

    # 2. SECTOR PERFORMANCE
    draw.rectangle([(480, 170), (915, 740)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(480, 170), (915, 215)], fill=NAVY)
    draw.text((495, 182), "2. SECTOR PERFORMANCE (%)", fill="#FFFFFF", font=f_head)
    sectors_list = [
        ("Nifty Media", "+1.98%", True), ("Nifty IT", "+1.30%", True), ("Nifty FMCG", "+0.54%", True),
        ("Nifty Pharma", "+0.34%", True), ("Nifty Auto", "+0.08%", True), ("Nifty Consumption", "-0.04%", False),
        ("Nifty Infra", "-0.44%", False), ("Nifty Energy", "-0.66%", False), ("Nifty Bank", "-0.77%", False),
        ("Nifty Realty", "-1.79%", False), ("Nifty PSU Bank", "-1.80%", False), ("Nifty Metal", "-1.93%", False)
    ]
    y = 235
    for name, pct, pos in sectors_list:
        draw.text((495, y), name, fill=TEXT_DARK, font=f_data)
        draw.text((820, y), pct, fill=GREEN if pos else RED, font=f_data)
        y += 41

    # 3. GLOBAL MARKETS
    draw.rectangle([(935, 170), (1375, 740)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(935, 170), (1375, 215)], fill=NAVY)
    draw.text((950, 182), "3. GLOBAL MARKETS", fill="#FFFFFF", font=f_head)
    global_layout = [("S&P 500", sp500), ("Nasdaq 100", nasdaq), ("Dow Jones", dow), ("FTSE 100", ftse), ("DAX", dax), ("CAC 40", cac), ("Nikkei 225", nikkei), ("Hang Seng", hangseng), ("KOSPI", kospi)]
    y = 240
    for name, metric in global_layout:
        draw.text((950, y), name, fill=TEXT_DARK, font=f_data)
        draw.text((1240, y), metric[2], fill=GREEN if metric[3] else RED, font=f_data)
        y += 53

    # --- ROW 2: CARDS 4, 5, 6, 7 ---
    # 4. TOP GAINERS
    draw.rectangle([(25, 760), (340, 1100)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 760), (340, 800)], fill=NAVY)
    draw.text((35, 772), "4. TOP GAINERS", fill="#FFFFFF", font=f_sub)
    gainers = [("KIRLOSENG", "₹1,743", "+9.17%"), ("CARBONUNIV", "₹1,105", "+6.52%"), ("CHAMBLFERT", "₹452.25", "+6.51%"), ("JPPOWER", "₹18.95", "+6.10%"), ("VIJAYA", "₹1,344", "+5.84%")]
    y = 820
    for stock, val, chg in gainers:
        draw.text((35, y), f"{stock:<12} {val:>8}  {chg:>7}", fill=GREEN, font=f_sub)
        y += 54

    # 5. TOP LOSERS
    draw.rectangle([(360, 760), (675, 1100)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(360, 760), (675, 800)], fill=NAVY)
    draw.text((370, 772), "5. TOP LOSERS", fill="#FFFFFF", font=f_sub)
    losers = [("NAVA", "₹626", "-11.03%"), ("HUDCO", "₹205.90", "-7.81%"), ("MUTHOOTFIN", "₹3,309", "-6.29%"), ("CLEAN", "₹767", "-6.23%"), ("HINDCOPPER", "₹573.40", "-5.45%")]
    y = 820
    for stock, val, chg in losers:
        draw.text((370, y), f"{stock:<12} {val:>8}  {chg:>7}", fill=RED, font=f_sub)
        y += 54

    # 6. MOMENTUM RADAR
    draw.rectangle([(695, 760), (1010, 1100)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(695, 760), (1010, 800)], fill=NAVY)
    draw.text((705, 772), "6. MOMENTUM RADAR", fill="#FFFFFF", font=f_sub)
    radar = [("OIL", "₹518.80", "+14.24%"), ("BIOCON", "₹430.40", "+12.99%")]
    y = 820
    for stock, val, chg in radar:
        draw.text((705, y), f"{stock:<12} {val:>8}  {chg:>7}", fill=GREEN, font=f_sub)
        y += 58

    # 7. SECTORS TO WATCH
    draw.rectangle([(1030, 760), (1375, 1100)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(1030, 760), (1375, 800)], fill=NAVY)
    draw.text((1040, 772), "7. SECTORS TO WATCH", fill="#FFFFFF", font=f_sub)
    draw.text((1040, 820), "POSITIVE:\n• Pharma, Media\n• Defence, Oil & Gas", fill=GREEN, font=f_sub)
    draw.text((1040, 935), "NEGATIVE:\n• Metals, PSU Banks\n• IT, Realty", fill=RED, font=f_sub)

    # --- ROW 3: CARDS 8, 9, 10 ---
    # 8. COMMODITIES
    draw.rectangle([(25, 1120), (460, 1430)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1120), (460, 1160)], fill=NAVY)
    draw.text((40, 1132), "8. COMMODITIES", fill="#FFFFFF", font=f_head)
    comms_data = [("Gold (10g)", gold), ("Silver (1kg)", silver), ("Crude Oil", crude), ("Natural Gas", natgas), ("Copper", copper)]
    y = 1180
    for name, metric in comms_data:
        draw_table_row(draw, 40, y, name, metric[0], metric[1], metric[2], metric[3], f_sub, TEXT_DARK, GREEN, RED)
        y += 48

    # 9. CURRENCY & BONDS
    draw.rectangle([(480, 1120), (915, 1430)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(480, 1120), (915, 1160)], fill=NAVY)
    draw.text((495, 1132), "9. CURRENCY & BONDS", fill="#FFFFFF", font=f_head)
    draw.text((495, 1180), f"USD/INR: {usdinr[0]} ({usdinr[2]})", fill=TEXT_DARK, font=f_data)
    draw.text((495, 1225), "India 10Y: 7.076% (+6 bps)\nIndia 5Y: 6.898% (+10 bps)\nIndia 2Y: 6.473% (+9 bps)", fill=TEXT_DARK, font=f_sub)
    draw.text((495, 1330), "US 10Y: 4.470% (+1 bps) | US 2Y: 4.000% (+2 bps)", fill=MUTED, font=f_sub)

    # 10. FII / DII FLOWS
    draw.rectangle([(935, 1120), (1375, 1430)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(935, 1120), (1375, 1160)], fill=NAVY)
    draw.text((950, 1132), "10. FII / DII FLOWS (Cr)", fill="#FFFFFF", font=f_head)
    draw.text((950, 1185), "FII Net Session: +187 Cr\nDII Net Session: +684 Cr\n\nCOMBINED SESSION FLOW:\n+872 Cr", fill=GREEN, font=f_head)

    # --- ROW 4: CARDS 11, 12, 13 ---
    # 11. OI DATA (NIFTY)
    draw.rectangle([(25, 1450), (460, 1830)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1450), (460, 1490)], fill=NAVY)
    draw.text((40, 1462), "11. OI DATA (NIFTY)", fill="#FFFFFF", font=f_head)
    draw.text((40, 1515), "RESISTANCE (CALL OI):\n• 24,000 (65.80 L)\n• 23,800 (48.30 L)", fill=RED, font=f_sub)
    draw.text((40, 1635), "SUPPORT (PUT OI):\n• 23,500 (62.40 L)\n• 23,400 (45.10 L)", fill=GREEN, font=f_sub)
    draw.text((40, 1765), "IMPORTANT ZONE: 23,800 - 23,900", fill=TEXT_DARK, font=f_sub)

    # 12. ALPHA RADAR
    draw.rectangle([(480, 1450), (915, 1830)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(480, 1450), (915, 1490)], fill=NAVY)
    draw.text((495, 1462), "12. ALPHA RADAR", fill="#FFFFFF", font=f_head)
    draw.text((495, 1515), "BULLISH THEMES:\n• Pharma: Defensive buying continues\n• Media: Strong sector momentum\n• Defence: UAE investment boost", fill=GREEN, font=f_sub)
    draw.text((495, 1665), "WEAK THEMES:\n• Metals: Profit booking after rally\n• PSU Banks: Weakness continues\n• IT: Sector under pressure", fill=RED, font=f_sub)

    # 13. HEAT MAP MATRIX
    draw.rectangle([(935, 1450), (1375, 1830)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(935, 1450), (1375, 1490)], fill=NAVY)
    draw.text((950, 1462), "13. HEAT MAP MATRIX", fill="#FFFFFF", font=f_head)
    
    draw.rectangle([(950, 1515), (1140, 1615)], fill="#E8F5E9")
    draw.text((965, 1545), "OIL\n+2.93%", fill=GREEN, font=f_sub)
    draw.rectangle([(1165, 1515), (1355, 1615)], fill="#E8F5E9")
    draw.text((1180, 1545), "BIOCON\n+2.72%", fill=GREEN, font=f_sub)
    draw.rectangle([(950, 1640), (1140, 1740)], fill="#FFEBEE")
    draw.text((965, 1670), "NAVA\n-11.03%", fill=RED, font=f_sub)
    draw.rectangle([(1165, 1640), (1355, 1740)], fill="#E3F2FD")
    draw.text((1180, 1670), "IT CLUSTER\n+1.30%", fill=TEXT_DARK, font=f_sub)

    # --- ROW 5: CARDS 14, 15, 16 ---
    # 14. MAJOR NEWS
    draw.rectangle([(25, 1850), (520, 2270)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(25, 1850), (520, 1885)], fill=NAVY)
    draw.text((40, 1858), "14. MAJOR NEWS", fill="#FFFFFF", font=f_head)
    draw.text((40, 1910), "INDIA NEWS:\n• Petrol & Diesel prices hiked by ₹3 per litre.\n• India's exports rise 13.8% YoY to $43.56B.\n\nGLOBAL NEWS:\n• WTI crude futures steady above $104/bbl.\n• Rising US Inflation concerns pressure metals.", fill=TEXT_DARK, font=f_sub)

    # 15. TRADER INSIGHT
    draw.rectangle([(540, 1850), (940, 2270)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(540, 1850), (940, 1885)], fill=NAVY)
    draw.text((550, 1858), "15. TRADER INSIGHT", fill="#FFFFFF", font=f_head)
    draw.text((550, 1910), "Markets witnessed selective buying with\ndefensive sectors outperforming.\n\nPharma and Media remained strong while\nMetals and PSU Banks stayed under pressure.\nTraders should focus on risk management.", fill=TEXT_DARK, font=f_sub)

    # 16. ATR RANGE
    draw.rectangle([(960, 1850), (1375, 2270)], fill="#FFFFFF", outline=BORDER_CLR, width=2)
    draw.rectangle([(960, 1850), (1375, 1885)], fill=NAVY)
    draw.text((970, 1858), "16. ATR RANGE", fill="#FFFFFF", font=f_head)
    draw.text((970, 1910), "Nifty 50:\nSupport: 23,400\nResistance: 23,900\n\nBank Nifty:\nSupport: 53,200\nResistance: 54,200", fill=TEXT_DARK, font=f_sub)

    # --- SEBI DISCLAIMER FOOTER ---
    draw.rectangle([(0, 2980), (1400, 3100)], fill="#E3E5E8")
    draw.text((40, 3015), "17. SEBI DISCLAIMER: Informational analytical matrix dashboard. Subject to change.\nVedansh Capital is not SEBI registered.", fill=TEXT_DARK, font=f_data)

    img_stream = io.BytesIO()
    img.save(img_stream, format='PNG')
    img_stream.seek(0)
    return img_stream

@bot.message_handler(commands=['start', 'help'])
def hi_message(msg):
    bot.reply_to(msg, "📈 Vedansh Capital Pro Engine Live! Run /dashboard to generate.")

@bot.message_handler(commands=['dashboard'])
def push_dashboard(msg):
    bot.send_message(msg.chat.id, "🔄 Connecting to data matrix modules... Formatting high-readability layout sheet.")
    try:
        out_img = compile_massive_dashboard()
        bot.send_photo(msg.chat.id, photo=out_img, caption="📊 *Vedansh Capital | Market Pro Dashboard*", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(msg.chat.id, f"Error compiling grid canvas: {str(e)}")

if __name__ == "__main__":
    t = threading.Thread(target=run_web_server)
    t.daemon = True
    t.start()
    bot.infinity_polling()
