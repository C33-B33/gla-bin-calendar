import streamlit as st
import os
import random

# --- CLOUD BINARY AUTO-INSTALLER ---
@st.cache_resource
def install_browser_dependencies():
    with st.spinner("🛸 Materializing cybernetic browser sub-routines..."):
        os.system("playwright install chromium")

install_browser_dependencies()

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# Hide default Streamlit developer chrome (hamburger menu and footer)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Define Visual App Styles
BIN_STYLES = {
    "Green Bin": {"icon": "🟩", "color": "#28A745"},
    "Brown Bin": {"icon": "🟫", "color": "#8B4513"},
    "Grey Bin": {"icon": "🩶", "color": "#6C757D"},
    "Purple Bin": {"icon": "🟪", "color": "#6F42C1"},
    "Blue Bin": {"icon": "🟦", "color": "#007BFF"}
}

# Curated pool of iconic real Glasgow postcodes across different areas
GLASGOW_EXAMPLES = [
    "G1 1HL",   # George Square / City Centre
    "G12 8QQ",  # West End / University
    "G40 1PT",  # Bridgeton / London Road
    "G41 2PE",  # Shawlands / Southside
    "G51 1EA",  # Govan
    "G3 8AZ",   # Finnieston
    "G73 1AB"   # Rutherglen
]

# Authentic Glasgow/Cybernetic local loading phrases
SCIFI_PHRASES = [
    "Haud on a wee sec, hacking into the George Square database...",
    "Rummaging through the council's mainframe hard drive...",
    "Chasing down the virtual bin lorry for the live telemetry datastream...",
    "Waking up the council's legacy servers (they've clearly had a heavy night)...",
    "Intercepting the cleansing department's secret encryption frequencies...",
    "Decrypting the local tenement close matrix quadrant configurations...",
    "Gie's a minute, the dial-up connection in the city chambers is pure crawling..."
]

# Initialize Session Memory States
if 'collections' not in st.session_state:
    st.session_state['collections'] = None
if 'saved_address' not in st.session_state:
    st.session_state['saved_address'] = None
if 'example_postcode' not in st.session_state:
    st.session_state['example_postcode'] = random.choice(GLASGOW_EXAMPLES)

BASE_URL = "https://onlineservices.glasgow.gov.uk/forms/refuseandrecyclingcalendar/"

# --- HIGH-PERFORMANCE CACHED SCRAPER ---
@st.cache_data(ttl=21600)
def fetch_live_calendar_html(uprn):
    target_url = f"{BASE_URL}CollectionsCalendar.aspx?UPRN={uprn}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url)
        page.wait_for_timeout(3000) 
        html_content = page.content()
        browser.close()
    return html_content

def parse_calendar_text(html):
    soup = BeautifulSoup(html, "html.parser")
    full_page_text = " ".join(soup.get_text().split())
    extracted_collections = []
    
    for bin_name in BIN_STYLES.keys():
        pattern = rf"Your next {re.escape(bin_name)} day is ([A-Za-z]+ \d{{1,2}}(?:st|nd|rd|th)? [A-Za-z]+ \d{{4}})"
        match = re.search(pattern, full_page_text)
        
        if match:
            raw_date_text = match.group(1)
            clean_date_text = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', raw_date_text)
            try:
                parsed_date = datetime.strptime(clean_date_text, "%A %d %B %Y").date()
                extracted_collections.append({"type": bin_name, "date": parsed_date})
            except:
                pass
    return extracted_collections

# --- NATIVE PLAYWRIGHT PDF PRINT GENERATOR ---
def generate_fridge_magnet_pdf(collections_list, address_label, uprn_label):
    sorted_data = sorted(collections_list, key=lambda x: x['date'])
    date_map = {item['type']: item['date'].strftime('%A, %d %B %Y') for item in sorted_data}
    
    html_markup = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 15mm 12mm; }}
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1e293b; margin: 0; padding: 0; font-size: 10pt; line-height: 1.4; }}
            .header-title {{ text-align: center; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #e2e8f0; }}
            .header-title h1 {{ margin: 0; font-size: 18pt; color: #0f172a; font-weight: 800; }}
            .header-title p {{ margin: 4px 0 0 0; font-size: 10pt; color: #64748b; }}
            .magnet-card {{ border: 2px dashed #94a3b8; border-radius: 14px; padding: 20px; margin-bottom: 30px; background-color: #ffffff; page-break-inside: avoid; position: relative; }}
            .magnet-label {{ position: absolute; top: -10px; left: 20px; background-color: #334155; color: #ffffff; font-size: 7.5pt; font-weight: 700; padding: 2px 10px; border-radius: 20px; text-transform: uppercase; }}
            .magnet-header {{ margin-bottom: 12px; border-bottom: 1px solid #f1f5f9; padding-bottom: 8px; }}
            .magnet-header h2 {{ margin: 0; font-size: 12pt; color: #0f172a; }}
            .magnet-header p {{ margin: 2px 0 0 0; font-size: 8.5pt; color: #64748b; }}
            .basic-item {{ display: table; width: 100%; margin-bottom: 8px; padding: 8px; border-radius: 8px; border: 1px solid #e2e8f0; background-color: #f8fafc; }}
            .basic-color-bar {{ display: table-cell; width: 6px; border-radius: 4px; }}
            .basic-content {{ display: table-cell; padding-left: 10px; vertical-align: middle; }}
            .basic-name {{ font-size: 10pt; font-weight: 700; color: #0f172a; }}
            .basic-frequency {{ font-size: 8.5pt; color: #64748b; }}
            .basic-write-in {{ display: table-cell; width: 45%; vertical-align: middle; text-align: right; font-size: 9pt; font-weight: 700; color: #1e3a8a; padding-right: 5px; }}
            .matrix-table {{ display: table; width: 100%; border-collapse: collapse; margin-bottom: 12px; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; }}
            .matrix-row {{ display: table-row; }}
            .matrix-header-cell {{ display: table-cell; padding: 6px 10px; font-size: 10pt; font-weight: 700; color: #ffffff; }}
            .matrix-body-row {{ display: table-row; background-color: #ffffff; }}
            .matrix-cell-yes {{ display: table-cell; width: 50%; padding: 10px; vertical-align: top; border-right: 1px solid #f1f5f9; font-size: 8.5pt; }}
            .matrix-cell-no {{ display: table-cell; width: 50%; padding: 10px; vertical-align: top; font-size: 8.5pt; }}
            .list-title-yes {{ color: #16a34a; font-weight: 700; margin-bottom: 4px; font-size: 9pt; }}
            .list-title-no {{ color: #dc2626; font-weight: 700; margin-bottom: 4px; font-size: 9pt; }}
            ul.matrix-list {{ margin: 0; padding-left: 14px; color: #334155; }}
            ul.matrix-list li {{ margin-bottom: 2px; }}
            .page-break {{ page-break-before: always; }}
            .magnet-notes {{ margin-top: 12px; border: 1px solid #e2e8f0; background-color: #fafafa; padding: 8px; border-radius: 6px; font-size: 8.5pt; }}
        </style>
    </head>
    <body>
        <div class="header-title">
            <h1>Glasgow Kerbside Collection Guide</h1>
            <p>Live Pre-Populated Fridge Magnet Reference Sheets</p>
        </div>
        <div class="magnet-card">
            <div class="magnet-label">Option 1: Quick Reference Timeline</div>
            <div class="magnet-header">
                <h2>Refuse Collection Schedule</h2>
                <p>📍 Linked Profile: {address_label} | UPRN: {uprn_label}</p>
            </div>
            <div class="basic-item">
                <div class="basic-color-bar" style="background-color: #28A745;"></div>
                <div class="basic-content"><div class="basic-name">🟩 Green Bin</div><div class="basic-frequency">General Waste & Non-Recyclable Rubbish (Every 21 Days)</div></div>
                <div class="basic-write-in">Due: {date_map.get('Green Bin', 'Check App')}</div>
            </div>
            <div class="basic-item">
                <div class="basic-color-bar" style="background-color: #8B4513;"></div>
                <div class="basic-content"><div class="basic-name">🟫 Brown Bin</div><div class="basic-frequency">Food Waste & Organic Garden Material (Every 14 Days)</div></div>
                <div class="basic-write-in">Due: {date_map.get('Brown Bin', 'Check App')}</div>
            </div>
            <div class="basic-item">
                <div class="basic-color-bar" style="background-color: #007BFF;"></div>
                <div class="basic-content"><div class="basic-name">🟦 Blue Bin</div><div class="basic-frequency">Paper, Cardboard & Dry Clean Fiber Packaging (Every 28 Days)</div></div>
                <div class="basic-write-in">Due: {date_map.get('Blue Bin', 'Check App')}</div>
            </div>
            <div class="basic-item">
                <div class="basic-color-bar" style="background-color: #6C757D;"></div>
                <div class="basic-content"><div class="basic-name">🩶 Grey Bin</div><div class="basic-frequency">Mixed Recycling (Plastics, Metals & Cartons) (Every 28 Days)</div></div>
                <div class="basic-write-in">Due: {date_map.get('Grey Bin', 'Check App')}</div>
            </div>
            <div class="basic-item">
                <div class="basic-color-bar" style="background-color: #6F42C1;"></div>
                <div class="basic-content"><div class="basic-name">🟪 Purple Bin</div><div class="basic-frequency">Glass Bottles & Product Jars Only (Every 56 Days)</div></div>
                <div class="basic-write-in">Due: {date_map.get('Purple Bin', 'Check App')}</div>
            </div>
        </div>

        <div class="page-break"></div>
        <div class="header-title">
            <h1>Glasgow Waste Sorting Matrix</h1>
            <p>Enhanced Household Recycling Cheat Sheet</p>
        </div>
        <div class="magnet-card">
            <div class="magnet-label">Option 2: Comprehensive Sorting Guide</div>
            <div class="matrix-table">
                <div class="matrix-row"><div class="matrix-header-cell" style="background-color: #28A745;">🟩 GREEN BIN — General Waste (Non-Recyclable)</div></div>
                <div class="matrix-body-row">
                    <div class="matrix-cell-yes"><div class="list-title-yes">✅ YES:</div><ul class="matrix-list"><li>Disposable nappies & wipes</li><li>Pet waste & soiled litter</li><li>Polystyrene & bubble wrap</li><li>Tissues & paper towels</li></ul></div>
                    <div class="matrix-cell-no"><div class="list-title-no">❌ NO:</div><ul class="matrix-list"><li>Standard dry recyclables</li><li>Electrical items & cables</li><li>Batteries (Fire risk)</li><li>Soil, rubble or stones</li></ul></div>
                </div>
            </div>
            <div class="matrix-table">
                <div class="matrix-row"><div class="matrix-header-cell" style="background-color: #007BFF;">🟦 BLUE BIN — Paper & Cardboard Recycling</div></div>
                <div class="matrix-body-row">
                    <div class="matrix-cell-yes"><div class="list-title-yes">✅ YES (LOOSE ONLY):</div><ul class="matrix-list"><li>Newspapers & magazines</li><li>Envelopes (with or without plastic windows)</li><li>Cardboard packs & boxes</li><li>Clean pizza boxes & egg cartons</li></ul></div>
                    <div class="matrix-cell-no"><div class="list-title-no">❌ NO:</div><ul class="matrix-list"><li>Plastic bags or wrapping films</li><li>Items with food or liquids</li><li>Shredded paper (confetti size)</li><li>Disposable coffee cups</li></ul></div>
                </div>
            </div>
            <div class="matrix-table">
                <div class="matrix-row"><div class="matrix-header-cell" style="background-color: #6C757D;">🩶 GREY BIN — Mixed Recycling (Plastics & Metals)</div></div>
                <div class="matrix-body-row">
                    <div class="matrix-cell-yes"><div class="list-title-yes">✅ YES (RINSED CLEAN):</div><ul class="matrix-list"><li>Plastic bottles, pots, tubs & trays</li><li>Food tins & drink cans</li><li>Aluminium foil & clean trays</li><li>Food cartons (Tetra Pak)</li></ul></div>
                    <div class="matrix-cell-no"><div class="list-title-no">❌ NO:</div><ul class="matrix-list"><li>Glass bottles or jars</li><li>Polystyrene inserts</li><li>Soft plastics, shopping bags, or wrappers</li><li>Metal cooking pots or pans</li></ul></div>
                </div>
            </div>
            <div class="matrix-table">
                <div class="matrix-row"><div class="matrix-header-cell" style="background-color: #8B4513;">🟫 BROWN BIN — Organic Food & Garden Waste</div></div>
                <div class="matrix-body-row">
                    <div class="matrix-cell-yes"><div class="list-title-yes">✅ YES:</div><ul class="matrix-list"><li>Grass, leaves & cut weeds</li><li>Flowers, plants & small twigs</li><li>Meat, fish, bones & dairy</li><li>Bread, pastries, fruit & veg</li></ul></div>
                    <div class="matrix-cell-no"><div class="list-title-no">❌ NO:</div><ul class="matrix-list"><li>Plastic trash sacks or liners</li><li>Soil, turf, stones or gravel</li><li>Animal waste or cat litter</li><li>Japanese Knotweed or Ragwort</li></ul></div>
                </div>
            </div>
            <div class="matrix-table">
                <div class="matrix-row"><div class="matrix-header-cell" style="background-color: #6F42C1;">🟪 PURPLE BIN — Glass Container Recycling</div></div>
                <div class="matrix-body-row">
                    <div class="matrix-cell-yes"><div class="list-title-yes">✅ YES:</div><ul class="matrix-list"><li>Wine & beer bottles</li><li>Spirit & liquor bottles</li><li>Glass jars (Jam, coffee, sauces)</li><li>Note: Screw caps can stay on</li></ul></div>
                    <div class="matrix-cell-no"><div class="list-title-no">❌ NO:</div><ul class="matrix-list"><li>Light bulbs or fluorescent tubes</li><li>Drinking glasses or ceramic mugs</li><li>Pyrex oven cookware glass</li><li>Window panes or mirrors</li></ul></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_markup)
        pdf_raw_bytes = page.pdf(format="A4", print_background=True)
        browser.close()
    return pdf_raw_bytes

# --- ROUTING ENGINE ---
query_uprn = st.query_params.get("uprn")
query_address = st.query_params.get("address")

# --- VIEW A: THE PERMANENT BOOKMARKED DASHBOARD ---
if query_uprn and query_address:
    st.title("Pure Brilliant Bin Finder 🏴󠁧󠁢󠁳󠁣󠁴󠁿")
    st.success(f"📍 **Household Profile Permanently Locked:** {query_address}")
    
    # DYNAMIC OFFICIAL COUNCIL LINK
    council_url = f"{BASE_URL}CollectionsCalendar.aspx?UPRN={query_uprn}"
    st.markdown(
        f"""
        <div style="margin-top: -10px; margin-bottom: 25px; font-size: 14px;">
            🌐 <a href="{council_url}" target="_blank" style="color: #2563EB; font-weight: 600; text-decoration: none;">
                View official Glasgow City Council web page for this address →
            </a>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("""
    Magic. Your specific address token is officially locked into the dashboard matrix. Make sure to **bookmark this exact web address right now** on your phone or laptop. That way, you can bypass the setup screens entirely and jump straight to your live dates whenever you visit.
    
    Now that we've sidestepped the council's maze, here are your pure brilliant tools to make sure you never miss a collection deadline again:
    """)
    
    with st.spinner(f"🌀 {random.choice(SCIFI_PHRASES)}"):
        try:
            calendar_html = fetch_live_calendar_html(query_uprn)
            collections = parse_calendar_text(calendar_html)
            
            if collections:
                st.markdown("""
                    <style>
                    .stButton>button, .stDownloadButton>button {
                        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
                        color: white !important;
                        border-radius: 14px !important;
                        border: none !important;
                        padding: 14px 28px !important;
                        font-weight: 600 !important;
                        letter-spacing: -0.3px !important;
                        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
                        transition: all 0.2s ease-in-out !important;
                        width: 100% !important;
                    }
                    .stButton>button:hover, .stDownloadButton>button:hover {
                        transform: translateY(-2px) !important;
                        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3) !important;
                    }
                    .stSelectbox div[data-baseweb="select"] {
                        border-radius: 12px !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                sorted_collections = sorted(collections, key=lambda x: x['date'])
                today = datetime.now().date()
                
                closest_date = sorted_collections[0]['date']
                hero_items = [item for item in sorted_collections if item['date'] == closest_date]
                future_bins = [item for item in sorted_collections if item['date'] > closest_date]
                
                hero_days = (closest_date - today).days
                
                if hero_days == 0:
                    hero_time = "🚨 GET THEM OOT RIGHT NOW! It's bin day! If you hear the lorry grinding down the street, you're already late!"
                    hero_bg = "linear-gradient(135deg, #FFFDF5 0%, #FFF9E6 100%)"
                    hero_border = "2px solid #F59E0B"
                elif hero_days == 1:
                    hero_time = "⏰ Get them dragged to the kerb tonight for tomorrow morning. Don't forget!"
                    hero_bg = "#F8FAFC"
                    hero_border = "1px solid #E2E8F0"
                else:
                    hero_time = f"📅 {closest_date.strftime('%A, %d %b')} ({hero_days} days away)"
                    hero_bg = "#FFFFFF"
                    hero_border = "1px solid #E2E8F0"

                bins_html = ""
                for idx, item in enumerate(hero_items):
                    style = BIN_STYLES.get(item['type'], {"icon": "🗑️", "color": "#333333"})
                    divider = '<hr style="border:0; border-top:1px dashed #E2E8F0; margin:14px 0;">' if idx > 0 else ""
                    bins_html += f'{divider}<div style="display: flex; align-items: center; margin-top: 8px;"><span style="font-size: 32px; margin-right: 14px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.05));">{style["icon"]}</span><div><h2 style="margin: 0; color: #1E293B; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;"><span style="color: {style["color"]};">{item["type"]}</span></h2></div></div>'

                primary_color = BIN_STYLES.get(hero_items[0]['type'], {"color": "#475569"})["color"]

                st.markdown(f'<div style="padding: 24px; border-left: 10px solid {primary_color}; border-top: {hero_border}; border-right: {hero_border}; border-bottom: {hero_border}; background: {hero_bg}; border-radius: 16px; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.03), 0 8px 10px -6px rgba(0,0,0,0.03);"><span style="font-size: 11px; font-weight: 800; color: #64748B; letter-spacing: 1.5px; text-transform: uppercase;">Next Collection Day</span><p style="margin: 4px 0 16px 0; font-size: 16px; font-weight: 700; color: #334155;">{hero_time}</p>{bins_html}</div>', unsafe_allow_html=True)
                
                if future_bins:
                    st.markdown("### 🗓️ Following Schedule")
                    col1, col2 = st.columns(2)
                    
                    for idx, item in enumerate(future_bins):
                        days_away = (item['date'] - today).days
                        style = BIN_STYLES.get(item['type'], {"icon": "🗑️", "color": "#333333"})
                        time_text = f"{item['date'].strftime('%a, %d %b')} ({days_away}d)"
                        target_col = col1 if idx % 2 == 0 else col2
                        
                        with target_col:
                            st.markdown(f'<div style="padding: 16px; border-left: 6px solid {style["color"]}; background-color: #FFFFFF; border-radius: 12px; margin-bottom: 14px; border-top: 1px solid #F1F5F9; border-right: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02);"><h4 style="margin: 0; color: #1E293B; font-size: 15px; font-weight: 700; letter-spacing: -0.3px;">{style["icon"]} {item["type"].split(" ")[0]} Bin</h4><p style="margin: 6px 0 0 0; font-size: 13px; font-weight: 500; color: #64748B;">{time_text}</p></div>', unsafe_allow_html=True)
                
                # --- DYNAMIC FEATURE: SOGGY RAIN CLIMATE WARNING ---
                st.info("🌧️ **Glasgow Weather Advisory:** It's absolutely tipping it down outside (standard Tuesday behavior). Make sure your bin lids are clicked shut tight. If your blue recycling bin fills up with rain and turns your cardboard into a soggy paper-mâché porridge, the collection crew will walk right past it.")

                # --- PHASE 3: COUNCIL WASTE CHEAT SHEET MATRIX ---
                st.divider()
                st.markdown("### 📋 What Goes in Which Bin?")
                
                # NATIVE LIVE GCC COMPLIANCE DISCLAIMER SHIELD
                st.warning(
                    "⚠️ **The 'Council Likes To Change Its Mind' Disclaimer:** Look, the big wigs at George Square "
                    "love to shift the recycling rules almost as often as the Glasgow weather changes. While this cheat sheet "
                    "is tracking the latest rules for the new Grey Bin rollout and Blue Paper tracks, the machinery at the processing "
                    "plant gets updated all the time. To save yourself from getting a red 'sticker of shame' slapped onto your bin lid "
                    "by a grumpy collection crew, double-check the absolute live source criteria here: "
                    "[Official Glasgow City Council Bin Sorting Guidelines](https://www.glasgow.gov.uk/article/13729/What-goes-in-your-bin)"
                )
                
                tab_green, tab_blue, tab_grey, tab_brown, tab_purple = st.tabs([
                    "🟩 Manky Stuff", "🟦 Clean Paper", "🩶 Mixed Plastics", "🟫 Leftover Scran", "🟪 Ginger Bottles"
                ])
                
                with tab_green:
                    st.markdown('<div style="background-color: #FFFFFF; color: #1E293B; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0;"><h4 style="color: #28A745; margin-top:0;">🟩 Manky Stuff: General Waste (Non-Recyclable)</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Disposable nappies & wipes</li><li>Pet waste & cat litter</li><li>Polystyrene & bubble wrap</li><li>Tissues & used kitchen towels</li><li>Wallpaper & grease-stained card</li><li>**Shredded paper** & packaging soft film plastics</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Standard clean recyclables</li><li>Electrical gear & cables</li><li>Batteries (Severe fire risk!)</li><li>Soil, bricks, rubble or stones</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_blue:
                    st.markdown('<div style="background-color: #FFFFFF; color: #1E293B; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0;"><h4 style="color: #007BFF; margin-top:0;">🟦 Clean Paper & Cardboard</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A;">✅ YES (Loose, no plastic bags):</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Newspapers, magazines & junk mail</li><li>Envelopes with or without plastic windows</li><li>Cardboard delivery packages & cereal boxes</li><li>Clean pizza boxes & egg cartons</li><li>Paperback books & wrapping sheets</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Items caked in old takeaway grease or liquids</li><li>Plastic box liners or wrappers</li><li>**Shredded paper** (Confetti escapes the sorter belts!)</li><li>Paper coffee cups & tissues</li><li>Hardback books</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_grey:
                    st.markdown('<div style="background-color: #FFFFFF; color: #1E293B; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0;"><h4 style="color: #6C757D; margin-top:0;">🩶 Mixed Plastics & Tins</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Plastic bottles, pots, tubs & food trays</li><li>Food tins, drink cans & empty aerosols</li><li>Clean aluminium foil packaging sheets</li><li>Juice/milk cartons (Tetra Pak)</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Glass bottles or product jars</li><li>Polystyrene blocks</li><li>Batteries or electronic elements</li><li>**Soft plastics** (Carrier bags, film wraps clog spinning hubs!)</li><li>Nappies</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_brown:
                    st.markdown('<div style="background-color: #FFFFFF; color: #1E293B; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0;"><h4 style="color: #8B4513; margin-top:0;">🟫 Leftover Scran & Garden Waste</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Grass clippings, wild weeds & leaves</li><li>Flowers, small branches & twigs</li><li>Meat, fish, bones, dairy & eggs</li><li>Bread, old pastries, fruit & veg scran</li><li>Tea bags & coffee filter grounds</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Standard plastic trash bags or sacks</li><li>Heavy soil, mud, turf, stones or gravel</li><li>Animal waste or cat litter sheets</li><li>Invasive Japanese Knotweed or Ragwort</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_purple:
                    st.markdown('<div style="background-color: #FFFFFF; color: #1E293B; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0;"><h4 style="color: #6F42C1; margin-top:0;">🟪 Ginger Bottles (Glass Only)</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Wine, beer & spirit bottles</li><li>Glass cheques / empty Irn-Bru glass</li><li>Glass food jars (Jam, sauce, coffee)</li><li>*Note: Metal screw caps can stay on, don\'t be daft!*</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569;"><li>Light bulbs or tubes</li><li>Drinking glasses, dinner plates or ceramic mugs</li><li>Pyrex oven cookware bake glass</li><li>Window panes or mirrors</li></ul></div></div></div>', unsafe_allow_html=True)

                # --- INTERACTIVE QUIZ SHUFFLER: AM I GLAIKIT? ---
                st.write("")
                with st.expander("🧠 The Great Glaswegian Recycling Exam: Am I Glaikit?"):
                    st.write("Test your wits against the trickiest traps in the city chambers. 3 random questions from our massive item bank—let's see if you're an absolute expert or a melt.")
                    
                    QUIZ_POOL = [
                        {
                            "question": "Where does a greasy, half-eaten takeaway pizza box belong?",
                            "options": ["🟩 Green Bin (The grease ruined it)", "🟦 Blue Bin (It's cardboard, innit)"],
                            "correct": "🟩 Green Bin (The grease ruined it)",
                            "explanation": "Takeaway grease breaks down the paper recycling pulp matrix. Manky cardboard goes straight to the general trash!"
                        },
                        {
                            "question": "What about an empty crisp packet or biscuit wrapper?",
                            "options": ["🟩 Green Bin (It's a dirty composite)", "🩶 Grey Bin (Looks plastic/foilly)"],
                            "correct": "🟩 Green Bin (It's a dirty composite)",
                            "explanation": "Crisp packets are a metallized plastic composite that can't be separated easily. If it fails the 'scrunch test' and pops back open, it's green bin material."
                        },
                        {
                            "question": "Where are you chucking a standard disposable takeaway coffee cup?",
                            "options": ["🟩 Green Bin (It's secretly lined with plastic)", "🟦 Blue Bin (It feels like paper)"],
                            "correct": "🟩 Green Bin (It's secretly lined with plastic)",
                            "explanation": "Takeaway cups are bonded with a waterproof polyethylene lining. Standard paper mills can't shred them, so they're destined for the bin fire."
                        },
                        {
                            "question": "Where do clean plastic grocery bags and bread wrappers go in Glasgow?",
                            "options": ["🟩 Green Bin (Soft films clog up the mechanical sorting rollers)", "🩶 Grey Bin (They're clean plastic containers)"],
                            "correct": "🟩 Green Bin (Soft films clog up the mechanical sorting rollers)",
                            "explanation": "Unlike some parts of the UK, Glasgow explicitly bans soft plastic films from the grey bin. They wrap around spinning mechanical rotors and bring the facility to a dead stop!"
                        },
                        {
                            "question": "An empty hairspray or deodorant aerosol can?",
                            "options": ["🩶 Grey Bin (It's metal packaging)", "🟩 Green Bin (Looks dangerous)"],
                            "correct": "🩶 Grey Bin (It's metal packaging)",
                            "explanation": "As long as it's completely empty and you've popped the plastic lid off, aerosols go right into the grey mixed recycling stream."
                        },
                        {
                            "question": "Where should you chuck an old AA battery from a dead TV remote?",
                            "options": ["🚫 NEITHER! (Fire hazard, take to a local shop drop)", "🟩 Green Bin (Just bury it in the trash)"],
                            "correct": "🚫 NEITHER! (Fire hazard, take to a local shop drop)",
                            "explanation": "Batteries spark huge fires inside the collection lorries and sorting centres. Never throw them in household wheelies—take them to a supermarket or tip drop-box."
                        },
                        {
                            "question": "A smashed Pyrex casserole dish after a total cooking disaster?",
                            "options": ["🟩 Green Bin (Pyrex melts at a different temperature)", "🟪 Purple Bin (It's glass, right?)"],
                            "correct": "🟩 Green Bin (Pyrex melts at a different temperature)",
                            "explanation": "Pyrex is specially treated to withstand heat, meaning it won't melt properly in standard container glass furnaces. Keep it far away from the purple bin!"
                        },
                        {
                            "question": "An envelope from the taxman with the clear little plastic window?",
                            "options": ["🟦 Blue Bin (The council accepts the windows now)", "🟩 Green Bin (You must rip the plastic out first)"],
                            "correct": "🟦 Blue Bin (The council accepts the windows now)",
                            "explanation": "Glasgow's mill screen systems can strain out minor window adhesives automatically. Throw the whole envelope straight into your blue slot."
                        },
                        {
                            "question": "What's the play with plastic bottle tops on clean milk jugs?",
                            "options": ["🩶 Leave them screwed on tightly", "🚫 Rip them off and toss them loosely"],
                            "correct": "🩶 Leave them screwed on tightly",
                            "explanation": "Loose caps are too small for the sorting belts and fall through the cracks into the refuse track. Squash the bottle, screw the cap back on, and throw it in the grey."
                        },
                        {
                            "question": "Where does a cardboard juice or milk carton (Tetra Pak) go?",
                            "options": ["🩶 Grey Bin (It's classed as a mixed container)", "🟦 Blue Bin (It feels like cardboard)"],
                            "correct": "🩶 Grey Bin (It's classed as a mixed container)",
                            "explanation": "Tetra Paks are lined with hidden layers of aluminum and plastic film. Because of this mix, Glasgow processes them alongside plastic and tin containers in the grey bin."
                        },
                        {
                            "question": "A rolls-and-sausage wrapper that's soaking wet with grease from the bakery?",
                            "options": ["🟩 Green Bin (Contaminated with food oil)", "🟦 Blue Bin (It's raw brown paper)"],
                            "correct": "🟩 Green Bin (Contaminated with food oil)",
                            "explanation": "Paper soaked in grease or engine oils cannot be cleaned during processing and ruins the fresh batch of pulp. Put it in the general waste."
                        },
                        {
                            "question": "Where do you get rid of old wallpaper after stripping the spare bedroom?",
                            "options": ["🟩 Green Bin (The glues and coatings ruin recycling)", "🟦 Blue Bin (It's pure paper rolls)"],
                            "correct": "🟩 Green Bin (The glues and coatings ruin recycling)",
                            "explanation": "Wallpaper is covered in synthetic adhesives, water-resistant coatings, and ancient paste. It cannot be converted back into clean paper, so it's general trash."
                        },
                        {
                            "question": "You've finished a foil container of takeaway curry. Where does it go?",
                            "options": ["🩶 Grey Bin (Only if you've rinsed the sauce out!)", "🟩 Green Bin (Takeaway containers are banned)"],
                            "correct": "🩶 Grey Bin (Only if you've rinsed the sauce out!)",
                            "explanation": "Aluminum trays are highly valuable recyclables, but they must be clean. Give it a quick wash—if it's caked in tikka masala, it belongs in the green general waste."
                        },
                        {
                            "question": "Where should shredded paper from a home office document destroyer go in Glasgow?",
                            "options": ["🟩 Green Bin (or your home compost heap)", "🟦 Blue Bin (It's paper pulp confetti)"],
                            "correct": "🟩 Green Bin (or your home compost heap)",
                            "explanation": "Because the paper fibers are shredded so small, mechanical screens at the recycling center can't catch them. They blow around like snow and ruin other batches. Keep them out of the blue bin!"
                        },
                        {
                            "question": "Where does a foil pet food pouch go after feeding the cat?",
                            "options": ["🟩 Green Bin (It's a fused composite layer)", "🩶 Grey Bin (It feels like metal foil)"],
                            "correct": "🟩 Green Bin (It's a fused composite layer)",
                            "explanation": "Pet pouches are plastic and aluminum melted together into a permanent shield. They cannot be split up by local sorting tracks, so toss them in the green general pile."
                        },
                        {
                            "question": "Where do you dispose of a broken glass mirror or light bulb?",
                            "options": ["🟩 Green Bin (Bury it safely) or the local tip", "🟪 Purple Bin (It's standard glass)"],
                            "correct": "🟩 Green Bin (Bury it safely) or the local tip",
                            "explanation": "Purple bins are exclusively for product *containers* (bottles and jars). Mirrors, window panes, and bulbs contain chemicals and lead that contaminate the batch."
                        },
                        {
                            "question": "A plastic yogurt pot with a foil lid—what's the protocol?",
                            "options": ["🩶 Grey Bin (Rip the foil lid off completely first)", "🩶 Grey Bin (Leave them attached)"],
                            "correct": "🩶 Grey Bin (Rip the foil lid off completely first)",
                            "explanation": "Both parts are recyclable in the grey track, but if the aluminum lid stays attached, the optical scanners read the whole thing as metal and route it incorrectly. Separate them!"
                        },
                        {
                            "question": "Where do you drop off a bundle of dead garden weeds and hedge cuttings?",
                            "options": ["🟫 Brown Bin (Organic material)", "🟩 Green Bin (Garden soil is trash)"],
                            "correct": "🟫 Brown Bin (Organic material)",
                            "explanation": "Hedge twigs, leaves, grass, and pulled weeds are ideal fodder for the city's organic composting facility. Pack them into the brown wheelie."
                        },
                        {
                            "question": "An old tin box that used to hold shortbread or biscuits?",
                            "options": ["🩶 Grey Bin (It's standard metal storage packaging)", "🟦 Blue Bin (It's for dry storage goods)"],
                            "correct": "🩶 Grey Bin (It's standard metal storage packaging)",
                            "explanation": "Metal biscuit tins and sweet tubs are treated exactly like food cans. Make sure it's empty and toss it right into your grey track."
                        },
                        {
                            "question": "Where does bubble wrap from an online delivery parcel go?",
                            "options": ["🟩 Green Bin (Stretchy low-density packaging film)", "🩶 Grey Bin (It's clear clean plastic)"],
                            "correct": "🟩 Green Bin (Stretchy low-density packaging film)",
                            "explanation": "While soft packaging wraps are highly debated, heavy bubble wrap is too stringy and clogs up the rotating gears at Blochairn. Keep it in the general trash."
                        }
                    ]
                    
                    if 'quiz_set' not in st.session_state:
                        st.session_state['quiz_set'] = random.sample(QUIZ_POOL, 3)
                        st.session_state['quiz_evaluated'] = False

                    user_answers = {}
                    for idx, q in enumerate(st.session_state['quiz_set']):
                        st.markdown(f"**Q{idx+1}: {q['question']}**")
                        user_answers[idx] = st.radio(
                            f"Choose for Q{idx+1}", 
                            q['options'], 
                            key=f"quiz_q_{idx}",
                            label_visibility="collapsed"
                        )
                        st.write("")

                    if not st.session_state['quiz_evaluated']:
                        if st.button("Submit My Exam Paper 📝"):
                            st.session_state['quiz_evaluated'] = True
                            st.rerun()
                    else:
                        score = 0
                        for idx, q in enumerate(st.session_state['quiz_set']):
                            if user_answers[idx] == q['correct']:
                                score += 1
                        
                        st.divider()
                        st.markdown(f"### Your Score: **{score} / 3**")
                        
                        if score == 3:
                            st.success("👑 **Verdict: Pure Brilliant!** You're a Cleansing Department prodigy. The bin men probably wave at you when they roll down your street. You ken exactly what's what.")
                        elif score == 2:
                            st.info("😏 **Verdict: No Bad.** You mostly know your stuff, but you've thrown a wee curveball in there. Room for improvement before you get an honorary high-vis jacket from the Lord Provost.")
                        elif score == 1:
                            st.warning("🤨 **Verdict: A Wee Bit Glaikit.** You're trying, bless you, but your back alley must be an absolute tactical disaster area. Give the cheat sheet tabs another read.")
                        else:
                            st.error("💀 **Verdict: Absolute Melt.** Total shambles. You're the exact reason the whole close gets a red warning tag slapped on the bin lids. Step away from the path until you've studied the sorting matrix!")
                        
                        with st.expander("👀 See the breakdown of answers"):
                            for idx, q in enumerate(st.session_state['quiz_set']):
                                is_correct = user_answers[idx] == q['correct']
                                status_symbol = "✅" if is_correct else "❌"
                                st.markdown(f"**Q{idx+1}:** {q['question']}")
                                st.write(f"{status_symbol} Your pick: {user_answers[idx]}")
                                st.caption(f"💡 *Why:* {q['explanation']}")
                                st.write("")

                        if st.button("🔄 Try a Fresh Set of Questions"):
                            del st.session_state['quiz_set']
                            del st.session_state['quiz_evaluated']
                            st.rerun()

                # --- UTILITY PANELS: MISSED BINS & BULK UPLIFTS ---
                st.write("")
                col_missed, col_bulk = st.columns(2)
                with col_missed:
                    st.error("🚨 Lorry Missed Your Street?")
                    st.write("If it is past 7:00 PM on collection day and your bin is still sitting full, you've officially been missed by the crew.")
                    st.markdown('<a href="https://www.glasgow.gov.uk/missedbincollection" target="_blank"><button style="width:100%; border-radius:10px; border:1px solid #DC2626; padding:8px; color:#DC2626; font-weight:600; background:transparent; cursor:pointer;">Report a Missed Bin Collection →</button></a>', unsafe_allow_html=True)
                with col_bulk:
                    st.info("🛋️ Got Heavy Junk or Furniture?")
                    st.write("Don't leave old mattresses or broken couches dumped out in the common tenement close area—book a bulk extraction.")
                    st.markdown('<a href="https://www.glasgow.gov.uk/bulkuplift" target="_blank"><button style="width:100%; border-radius:10px; border:1px solid #2563EB; padding:8px; color:#2563EB; font-weight:600; background:transparent; cursor:pointer;">Book an Official Bulk Uplift →</button></a>', unsafe_allow_html=True)

                # --- PHASE 4: ENHANCED PRINTABLE FRIDGE MAGNET PDF EXPORTER ---
                st.divider()
                st.markdown("### 🖨️ Printable Fridge Magnet Generator")
                st.write("Compile a high-contrast, printer-friendly PDF vector sheet containing your exact schedule timeline and full recycling cheat sheets.")
                
                pdf_scifi = random.choice(SCIFI_PHRASES)
                if st.button("🖨️ Compile & Format Fridge Magnet PDF Sheets"):
                    with st.spinner(f" 🛸 {pdf_scifi}"):
                        try:
                            pdf_bytes = generate_fridge_magnet_pdf(collections, query_address, query_uprn)
                            st.success("PDF Compiled successfully! Download button unlocked below.")
                            st.download_button(
                                label="📥 Download Fridge Magnet Printouts (.pdf)",
                                data=pdf_bytes,
                                file_name=f"fridge_magnets_{query_uprn}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        except Exception as pdf_err:
                            st.error(f"Failed compiling document vector layouts: {pdf_err}")

                # --- PHASE 5: DIGITAL CALENDAR EXPORT UTILITY ---
                st.divider()
                st.write("### 📅 Export to Your Phone Calendar")
                st.warning("⚠️ **Festive Shambles Warning:** Look, we all know the council loves to do things on the fly when Christmas and New Year roll around. If a collection lands on a bank holiday, they\'ll cancel it entirely or shift it completely without bothering to update their automated online calendar. This means while this digital export stays completely static doing the regular math, the real-world bin lorry is likely nowhere to be seen. If your phone calendar claims they\'re rocking up on Boxing Day, the internet is pure giein it laldy with the lies. Make sure to check back on the live dashboard on your phone during festive week before you drag your bins out for nothing!")
                
                duration_months = st.selectbox("Select export timeframe:", options=[1, 3, 6, 12], format_func=lambda x: f"Next {x} Month{'s' if x > 1 else ''}")
                
                intervals = {"Green Bin": 21, "Brown Bin": 14, "Grey Bin": 28, "Purple Bin": 56, "Blue Bin": 28}
                ics_lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Glasgow Bin Finder//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH"]
                end_date = today + timedelta(days=duration_months * 30)
                
                for item in collections:
                    bin_type = item['type']
                    current_date = item['date']
                    cycle_days = intervals.get(bin_type, 14)
                    style = BIN_STYLES.get(bin_type, {"icon": "🗑️"})
                    
                    while current_date <= end_date:
                        is_festive_week = (current_date.month == 12 and current_date.day >= 20) or (current_date.month == 1 and current_date.day <= 5)
                        title_prefix = "🎄 [Holiday Shift Check] " if is_festive_week else ""
                        event_summary = f"{title_prefix}{style['icon']} Glasgow {bin_type} Collection"
                        
                        ics_lines.extend([
                            "BEGIN:VEVENT",
                            f"SUMMARY:{event_summary}",
                            f"DTSTART;VALUE=DATE:{current_date.strftime('%Y%m%d')}",
                            f"DTEND;VALUE=DATE:{(current_date + timedelta(days=1)).strftime('%Y%m%d')}",
                            f"DESCRIPTION:Time to put your official {bin_type} out. Note: If this lands on festive week, verify the live app dashboard for holiday adjustments.",
                            "STATUS:CONFIRMED",
                            "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:Bin Reminder", "TRIGGER:-PT12H", "END:VALARM",
                            "END:VEVENT"
                        ])
                        current_date += timedelta(days=cycle_days)
                        
                ics_lines.append("END:VCALENDAR")
                st.download_button(label="📥 Download Calendar Reminders (.ics)", data="\n".join(ics_lines), file_name=f"bins_{query_uprn}.ics", mime="text/calendar", use_container_width=True)
                
            else:
                st.error("Could not read schedule data from the calendar view layout configuration.")
        except Exception as e:
            st.error(f"Error executing profile lookup: {e}")
            
    st.divider()
    if st.button("🔄 Wrong House? Clear it and start again"):
        st.query_params.clear()
        st.session_state.clear()
        st.session_state['example_postcode'] = random.choice(GLASGOW_EXAMPLES)
        st.rerun()

# --- VIEW B: THE INITIAL SETUP PORTAL ---
else:
    st.title("Pure Brilliant Bin Finder 🏴󠁧󠁢󠁳󠁣󠁴󠁿")
    st.markdown("""
    Tired of peeking out the window at midnight to see which color bins the neighbors have dragged to the kerb? Drop your postcode below **one single time**, pick your exact door, and you're set. 
    
    No logging in every month, no chasing dead council links—once you lock it in, just **bookmark your custom dashboard page** and your schedule is sorted for life.
    """)
    
    random_placeholder = st.session_state['example_postcode']
    postcode_input = st.text_input("Stick your postcode in here:", value=random_placeholder).upper().strip()
    
    if postcode_input:
        if 'last_postcode' not in st.session_state or st.session_state.get('last_postcode') != postcode_input:
            phrases = random.sample(SCIFI_PHRASES, 3)
            status_box = st.empty()
            
            try:
                status_box.info(f"🚀 {phrases[0]}")
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.goto(BASE_URL)
                    
                    status_box.info(f"⚡ {phrases[1]}")
                    page.fill("#Application_Addresses_Search", postcode_input)
                    page.click("#Application_Addresses_ImageButton")
                    
                    status_box.info(f"🛸 {phrases[2]}")
                    page.wait_for_timeout(2500)
                    html_content = page.content()
                    browser.close()
                
                status_box.empty()
                soup = BeautifulSoup(html_content, "html.parser")
                blocks_map = {}
                direct_address_map = {}
                
                for row in soup.find_all("tr"):
                    row_text = row.get_text().strip()
                    expand_img = row.find("input", id=re.compile(r"Expand\d+"))
                    if expand_img:
                        title_attr = expand_img.get("title", "Complex Block")
                        clean_address = row_text.strip()
                        clean_address = " ".join(clean_address.split())
                        display_name = f"🏢 {clean_address} ({title_attr})"
                        blocks_map[display_name] = f"#{expand_img.get('id')}"
                    elif "Select" in row_text:
                        link_tag = row.find("a", id=re.compile(r"Select\d+"))
                        if link_tag:
                            clean_address = row_text.replace("Select", "").strip()
                            clean_address = " ".join(clean_address.split())
                            direct_address_map[clean_address] = f"#{link_tag.get('id')}"
                
                st.session_state['blocks_map'] = blocks_map if blocks_map else None
                st.session_state['direct_map'] = direct_address_map if direct_address_map else None
                st.session_state['expanded_flats_map'] = None  
                st.session_state['last_postcode'] = postcode_input
            except Exception as e:
                st.empty()
                st.error(f"Failed to extract lookup array grid: {e}")

        # --- CONDITION A: THE POSTCODE CONTAINS APARTMENT BLOCKS ---
        if st.session_state.get('blocks_map'):
            st.info("🏢 Aye, that's a tenement or a big block of flats. Pick your close/building first:")
            selected_block = st.selectbox("Select Building Block", list(st.session_state['blocks_map'].keys()))
            
            if st.button("Reveal Flats inside Block 👇"):
                target_expand_id = st.session_state['blocks_map'][selected_block]
                st.session_state['active_expand_id'] = target_expand_id
                phrases = random.sample(SCIFI_PHRASES, 3)
                status_box = st.empty()
                
                try:
                    status_box.info(f"🚀 {phrases[0]}")
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        page.goto(BASE_URL)
                        page.fill("#Application_Addresses_Search", postcode_input)
                        page.click("#Application_Addresses_ImageButton")
                        page.wait_for_timeout(2000)
                        status_box.info(f"⚡ {phrases[1]}")
                        page.click(target_expand_id)
                        status_box.info(f"🛸 {phrases[2]}")
                        page.wait_for_timeout(2500)
                        expanded_html = page.content()
                        browser.close()
                    
                    status_box.empty()
                    sub_soup = BeautifulSoup(expanded_html, "html.parser")
                    flats_map = {}
                    for row in sub_soup.find_all("tr"):
                        row_text = row.get_text().strip()
                        if "Select" in row_text:
                            link_tag = row.find("a", id=re.compile(r"Select\d+"))
                            if link_tag:
                                clean_flat = row_text.replace("Select", "").strip()
                                clean_flat = " ".join(clean_flat.split())
                                flats_map[clean_flat] = f"#{link_tag.get('id')}"
                    
                    if flats_map:
                        st.session_state['expanded_flats_map'] = flats_map
                    else:
                        st.error("Clicked expand, but couldn't parse the subsequent flat profile grid elements.")
                except Exception as e:
                    st.empty()
                    st.error(f"Flat expansion workflow timed out: {e}")
            
            if st.session_state.get('expanded_flats_map'):
                selected_flat = st.selectbox("Select Your Exact Flat / Door Number", list(st.session_state['expanded_flats_map'].keys()))
                
                if st.button("Gie's Ma Schedule! 🚀"):
                    target_select_id = st.session_state['expanded_flats_map'][selected_flat]
                    target_expand_id = st.session_state.get('active_expand_id')
                    phrases = random.sample(SCIFI_PHRASES, 3)
                    status_box = st.empty()
                    
                    try:
                        status_box.info(f"🚀 {phrases[0]}")
                        with sync_playwright() as p:
                            browser = p.chromium.launch(headless=True)
                            page = browser.new_page()
                            page.goto(BASE_URL)
                            page.fill("#Application_Addresses_Search", postcode_input)
                            page.click("#Application_Addresses_ImageButton")
                            page.wait_for_timeout(2000)
                            status_box.info(f"⚡ {phrases[1]}")
                            page.click(target_expand_id)
                            page.wait_for_timeout(2000)
                            page.click(target_select_id)
                            status_box.info(f"🛸 {phrases[2]}")
                            page.wait_for_timeout(4000)
                            final_url = page.url
                            browser.close()
                        
                        status_box.empty()
                        uprn_match = re.search(r"UPRN=(\d+)", final_url)
                        if uprn_match:
                            st.query_params["uprn"] = uprn_match.group(1)
                            st.query_params["address"] = selected_flat
                            st.rerun()
                        else:
                            st.error("Failed to parse UPRN configuration parameter state from URL bar.")
                    except Exception as e:
                        st.empty()
                        st.error(f"Failed loading final selection link state: {e}")

        # --- CONDITION B: THE POSTCODE CONTAINS DIRECT STANDARD HOUSES ---
        elif st.session_state.get('direct_map'):
            selected_address = st.selectbox("Select your exact address", list(st.session_state['direct_map'].keys()))
            
            if st.button("Gie's Ma Schedule! 🚀"):
                target_element_id = st.session_state['direct_map'][selected_address]
                phrases = random.sample(SCIFI_PHRASES, 3)
                status_box = st.empty()
                
                try:
                    status_box.info(f"🚀 {phrases[0]}")
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True)
                        page = browser.new_page()
                        page.goto(BASE_URL)
                        page.fill("#Application_Addresses_Search", postcode_input)
                        page.click("#Application_Addresses_ImageButton")
                        page.wait_for_timeout(2000)
                        status_box.info(f"⚡ {phrases[1]}")
                        page.click(target_element_id)
                        status_box.info(f"🛸 {phrases[2]}")
                        page.wait_for_timeout(4000)
                        final_url = page.url
                        browser.close()
                    
                    status_box.empty()
                    uprn_match = re.search(r"UPRN=(\d+)", final_url)
                    if uprn_match:
                        st.query_params["uprn"] = uprn_match.group(1)
                        st.query_params["address"] = selected_address
                        st.rerun()
                    else:
                        st.error("Failed to parse system profile token from final URL context.")
                except Exception as e:
                    st.empty()
                    st.error(f"System configuration execution failure: {e}")
        
        elif st.session_state.get('last_postcode') == postcode_input:
            st.warning("⚠️ No addresses found. Verify the postcode formatting or check if the server query timed out.")
