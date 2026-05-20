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

# Deep pool of sci-fi loading states
SCIFI_PHRASES = [
    "Initializing quantum tachyon scan on localized sectors...",
    "Bypassing municipal mainframe structural firewalls...",
    "Decrypting legacy ASP.NET sub-space data-streams...",
    "Charging anti-matter containment grids for timeline transit...",
    "Rerouting sub-space coordinates through the Glasgow grid...",
    "Warm booting cybernetic refuse detection arrays...",
    "Syncing multi-dimensional calendar arrays with reality...",
    "Engaging hyper-spatial sub-grid decompression protocols...",
    "Defragmenting multi-tier tenement structural sector arrays...",
    "Extracting high-density chronal matrix configurations...",
    "Aligning chronal destination vectors with local time arrays...",
    "Querying intergalactic registry for active UPRN signatures...",
    "Calibrating flux capacitors to match municipal collection cycles...",
    "Infiltrating local government data nodes via dark-matter proxy..."
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
            <p>Live Pre-Populated Fridge Magnet Sheets</p>
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
                    <div class="matrix-cell-yes"><div class="list-title-yes">✅ YES (LOOSE ONLY):</div><ul class="matrix-list"><li>Newspapers & magazines</li><li>Envelopes & shredded paper</li><li>Cardboard packs & boxes</li><li>Clean pizza boxes & egg cartons</li></ul></div>
                    <div class="matrix-cell-no"><div class="list-title-no">❌ NO:</div><ul class="matrix-list"><li>Plastic bags or wrapping films</li><li>Items with food or liquids</li><li>Padded Jiffy envelopes</li><li>Disposable coffee cups</li></ul></div>
                </div>
            </div>
            <div class="matrix-table">
                <div class="matrix-row"><div class="matrix-header-cell" style="background-color: #6C757D;">🩶 GREY BIN — Mixed Recycling (Plastics & Metals)</div></div>
                <div class="matrix-body-row">
                    <div class="matrix-cell-yes"><div class="list-title-yes">✅ YES (RINSED CLEAN):</div><ul class="matrix-list"><li>Plastic bottles, pots, tubs & trays</li><li>Food tins & drink cans</li><li>Aluminium foil & clean trays</li><li>Food cartons (Tetra Pak)</li></ul></div>
                    <div class="matrix-cell-no"><div class="list-title-no">❌ NO:</div><ul class="matrix-list"><li>Glass bottles or jars</li><li>Polystyrene inserts</li><li>Batteries or active device modules</li><li>Metal cooking pots or pans</li></ul></div>
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
    st.title("Your Bin Schedule 🚛")
    st.success(f"📍 **Live Profile Linked:** {query_address}")
    
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
                    hero_time = "🚨 TODAY! Get them out on the kerb side right now!"
                    hero_bg = "linear-gradient(135deg, #FFFDF5 0%, #FFF9E6 100%)"
                    hero_border = "2px solid #F59E0B"
                elif hero_days == 1:
                    hero_time = f"⏰ Tomorrow ({closest_date.strftime('%d %b')})"
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
                    st.markdown("<h3 style='font-size: 18px; font-weight: 700; color: #475569; margin-bottom: 14px;'>🗓️ Following Schedule</h3>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    
                    for idx, item in enumerate(future_bins):
                        days_away = (item['date'] - today).days
                        style = BIN_STYLES.get(item['type'], {"icon": "🗑️", "color": "#333333"})
                        time_text = f"{item['date'].strftime('%a, %d %b')} ({days_away}d)"
                        target_col = col1 if idx % 2 == 0 else col2
                        
                        with target_col:
                            st.markdown(f'<div style="padding: 16px; border-left: 6px solid {style["color"]}; background-color: #FFFFFF; border-radius: 12px; margin-bottom: 14px; border-top: 1px solid #F1F5F9; border-right: 1px solid #F1F5F9; border-bottom: 1px solid #F1F5F9; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02);"><h4 style="margin: 0; color: #1E293B; font-size: 15px; font-weight: 700; letter-spacing: -0.3px;">{style["icon"]} {item["type"].split(" ")[0]} Bin</h4><p style="margin: 6px 0 0 0; font-size: 13px; font-weight: 500; color: #64748B;">{time_text}</p></div>', unsafe_allow_html=True)
                
                # --- PHASE 3: COUNCIL WASTE CHEAT SHEET ---
                st.divider()
                st.markdown("<h3 style='font-size: 20px; font-weight: 800; color: #1E293B; margin-bottom: 4px;'>📋 What Goes in Which Bin?</h3>", unsafe_allow_html=True)
                st.write("Official material classification breakdown sourced from Glasgow City Council.")
                
                tab_green, tab_blue, tab_grey, tab_brown, tab_purple = st.tabs(["🟩 Green", "🟦 Blue", "🩶 Grey", "🟫 Brown", "🟪 Purple"])
                with tab_green:
                    st.markdown('<div style="background-color: #FFFFFF; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);"><h4 style="color: #28A745; margin-top:0; font-size:16px;">🟩 Green Bin: General Waste (Non-Recyclable)</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A; font-size:14px;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Disposable nappies & wipes</li><li>Pet waste & cat litter</li><li>Polystyrene & bubble wrap</li><li>Tissues, wet wipes & kitchen towels</li><li>Wallpaper & greasy food boxes</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626; font-size:14px;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Standard recyclables (Paper/Plastics)</li><li>Electrical equipment & cables</li><li>Batteries (Fire risk)</li><li>Soil, rubble, stones or bricks</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_blue:
                    st.markdown('<div style="background-color: #FFFFFF; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);"><h4 style="color: #007BFF; margin-top:0; font-size:16px;">🟦 Blue Bin: Paper & Cardboard</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A; font-size:14px;">✅ YES (Loose, no bags):</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Newspapers, magazines & junk mail</li><li>Envelopes & shredded paper</li><li>Cardboard packages & cereal boxes</li><li>Clean pizza boxes & egg cartons</li><li>Paperback books & wrapping paper</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626; font-size:14px;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Plastic bags, wrappers or liners</li><li>Items covered in food or liquids</li><li>Padded envelopes (Jiffy bags)</li><li>Paper towels, tissues or coffee cups</li><li>Hardback books</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_grey:
                    st.markdown('<div style="background-color: #FFFFFF; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);"><h4 style="color: #6C757D; margin-top:0; font-size:16px;">🩶 Grey Bin: Mixed Recycling (Plastics & Metals)</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A; font-size:14px;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Plastic bottles, pots, tubs & trays</li><li>Food tins, drink cans & empty aerosols</li><li>Clean aluminium foil & foil trays</li><li>Food and drink cartons (Tetra Pak)</li><li>Soft plastics (Carrier bags, film lids)</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626; font-size:14px;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Glass bottles or jars</li><li>Polystyrene inserts</li><li>Batteries or electronic elements</li><li>Metal pots, cooking pans or trays</li><li>Nappies</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_brown:
                    st.markdown('<div style="background-color: #FFFFFF; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);"><h4 style="color: #8B4513; margin-top:0; font-size:16px;">🟫 Brown Bin: Garden & Food Waste</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A; font-size:14px;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Grass clippings, leaves & weeds</li><li>Flowers, plants & small branches</li><li>Meat, fish, bones, dairy & eggs</li><li>Fruit, vegetables, bread & pastries</li><li>Tea bags & coffee grounds</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626; font-size:14px;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Plastic bags or standard trash sacks</li><li>Soil, mud, turf, stones or gravel</li><li>Animal waste material or pet bedding</li><li>Japanese Knotweed or Ragwort</li></ul></div></div></div>', unsafe_allow_html=True)
                with tab_purple:
                    st.markdown('<div style="background-color: #FFFFFF; padding: 18px; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);"><h4 style="color: #6F42C1; margin-top:0; font-size:16px;">🟪 Purple Bin: Glass Recycling</h4><div style="display: flex; flex-wrap: wrap; gap: 16px;"><div style="flex: 1; min-width: 200px;"><strong style="color: #16A34A; font-size:14px;">✅ YES:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Wine & beer bottles</li><li>Spirit & liquor bottles</li><li>Glass food jars (Jam, coffee, sauces)</li><li>Note: Screw lids/caps can be left on</li></ul></div><div style="flex: 1; min-width: 200px;"><strong style="color: #DC2626; font-size:14px;">❌ NO:</strong><ul style="font-size: 13px; padding-left: 20px; color: #475569; margin-top:6px;"><li>Light bulbs or fluorescent tubes</li><li>Drinking glasses, plates or ceramic cups</li><li>Pyrex cookware glass</li><li>Window panes or mirror pieces</li></ul></div></div></div>', unsafe_allow_html=True)

                # --- PHASE 4: ENHANCED PRINTABLE FRIDGE MAGNET PDF EXPORTER ---
                st.divider()
                st.markdown("<h3 style='font-size: 18px; font-weight: 700; color: #1E293B;'>🖨️ Printable Fridge Magnet Generator</h3>", unsafe_allow_html=True)
                st.write("Compile a high-contrast, printer-friendly PDF vector sheet containing your exact schedule timeline and full recycling cheat sheets.")
                
                pdf_scifi = random.choice(SCIFI_PHRASES)
                if st.button("🖨️ Compile & Format Fridge Magnet PDF Sheets"):
                    with st.spinner(f"🛸 {pdf_scifi}"):
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
                st.warning("⚠️ **Festive Schedule Note:** Glasgow City Council collections usually have a different arrangements around Christmas and New Year week. Because this digital export projects dates forward mathematically, please re-download your calendar file in January to ensure it's back up with the regular cycle.")
                
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
    if st.button("🔄 Unlink Address & Search Again"):
        st.query_params.clear()
        st.session_state.clear()
        st.session_state['example_postcode'] = random.choice(GLASGOW_EXAMPLES)
        st.rerun()

# --- VIEW B: THE INITIAL SETUP PORTAL ---
else:
    st.title("Glasgow Bin Finder 🤖")
    st.write("Enter your postcode to link your address and generate your customized tracking dashboard.")
    
    random_placeholder = st.session_state['example_postcode']
    postcode_input = st.text_input(f"Enter Postcode (e.g., {random_placeholder})").upper().strip()
    
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
            st.info("🏢 This area belongs to an apartment complex. Select your building block first:")
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
                
                if st.button("Lock Flat & Generate Dashboard 🚀"):
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
            
            if st.button("Lock Address & Generate Dashboard 🚀"):
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
