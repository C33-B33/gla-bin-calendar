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
            .basic-color-bar {{ display: table-cell; width:
