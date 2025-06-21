import requests
from bs4 import BeautifulSoup, Tag
import sqlite3
import time
import re
import json

BASE_URL = "https://www.sixt.com/php/terms/view"

SECTION_MAP = {
    'General Rental Information': 'rental_information',
    'Tariff information': 'payment_information',
    'Protection conditions': 'protection_conditions',
    'Cross Border Rentals & Territorial Restrictions': 'authorized_driving_areas',
    'Extras': 'extras',
    'Other Fees and Taxes': 'other_charges_and_taxes',
    'VAT': 'vat',
    # You can add more mappings if you want to capture more sections
}

ALL_COLUMNS = [
    'country', 'vehicle_type',
    'rental_information', 'payment_information', 'protection_conditions',
    'authorized_driving_areas', 'extras', 'other_charges_and_taxes', 'vat'
]

def init_db(db_path='sixt_terms.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS rental_terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT,
            vehicle_type TEXT,
            rental_information TEXT,
            payment_information TEXT,
            protection_conditions TEXT,
            authorized_driving_areas TEXT,
            extras TEXT,
            other_charges_and_taxes TEXT,
            vat TEXT
        )
    ''')
    conn.commit()
    return conn

def save_terms_row(conn, row):
    c = conn.cursor()
    placeholders = ','.join(['?'] * len(ALL_COLUMNS))
    c.execute(f'''
        INSERT INTO rental_terms ({','.join(ALL_COLUMNS)})
        VALUES ({placeholders})
    ''', [row.get(col) for col in ALL_COLUMNS])
    conn.commit()

def get_countries_and_vehicle_types():
    resp = requests.get(BASE_URL, params={
        'language': 'en_US',
        'liso': 'US',
        'rtar': '000',
        'view': 'EPP',
        'tlang': 'en_GB',
        'style': 'typo3'
    })
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Country codes
    country_select = soup.find('select', {'name': 'select_country'})
    countries = []
    usa_code = None
    if isinstance(country_select, Tag):
        for opt in country_select.find_all('option'):
            if not isinstance(opt, Tag):
                continue
            code = opt.get('value')
            name = opt.text.strip()
            if code:
                countries.append((code, name))
                if name.lower() == 'usa' or (isinstance(code, str) and code.startswith('US')):
                    usa_code = code
    # Parse avail_ctype from JS
    avail_ctype = {}
    for script in soup.find_all('script'):
        if 'var avail_ctype' in script.text:
            m = re.search(r'var avail_ctype\s*=\s*(\{.*?\});', script.text, re.DOTALL)
            if m:
                avail_ctype = json.loads(m.group(1).replace("'", '"'))
    # Hardcode ctype_map since it uses JS variables
    ctype_map = {'EPP': 'Passenger vehicle', 'EPL': 'Truck', 'IP': 'Passenger vehicle', 'IL': 'Truck'}
    # Only get vehicle types for USA
    vehicle_types = []
    if usa_code and usa_code in avail_ctype:
        for vcode in avail_ctype[usa_code]:
            vname = ctype_map.get(vcode, vcode)
            vehicle_types.append((vcode, vname))
    # Only return USA
    usa = [c for c in countries if c[0] == usa_code]
    return usa, vehicle_types

def scrape_terms_for(conn, country_code, country_name, vehicle_code, vehicle_name):
    params = {
        'language': 'en_US',
        'liso': country_code,
        'rtar': vehicle_code,
        'view': 'EPP',
        'tlang': 'en_GB',
        'style': 'typo3'
    }
    resp = requests.get(BASE_URL, params=params)
    if resp.status_code != 200:
        print(f"Failed to fetch {country_name} - {vehicle_name}: HTTP {resp.status_code}")
        return
    soup = BeautifulSoup(resp.text, 'html.parser')
    row = {'country': country_name, 'vehicle_type': vehicle_name}
    current_col = None
    content_acc = []
    for el in soup.find_all(['h2', 'h3', 'p', 'ul', 'ol']):
        if getattr(el, 'name', None) == 'h2':
            section_title = el.get_text(strip=True)
            print(f"Found section: '{section_title}'")  # Debug print
            if current_col:
                row[current_col] = '\n'.join(content_acc).strip()
            current_col = SECTION_MAP.get(section_title)
            content_acc = []
        elif current_col:
            content_acc.append(el.get_text(" ", strip=True))
    if current_col:
        row[current_col] = '\n'.join(content_acc).strip()
    # Only save if at least one section has data
    print(row)  # Debug print
    if any(row.get(col) for col in ALL_COLUMNS[2:]):
        save_terms_row(conn, row)

def scrape_all_terms(conn):
    countries, vehicle_types = get_countries_and_vehicle_types()
    # Only process USA
    if not countries:
        print('USA not found in country list.')
        return
    country_code, country_name = countries[0]
    # Only process the first vehicle type for now
    if not vehicle_types:
        print('No vehicle types found.')
        return
    vehicle_code, vehicle_name = vehicle_types[0]
    print(f"Scraping {country_name} - {vehicle_name}...")
    try:
        scrape_terms_for(conn, country_code, country_name, vehicle_code, vehicle_name)
        time.sleep(0.5)
    except Exception as e:
        print(f"Failed for {country_name} - {vehicle_name}: {e}")

if __name__ == "__main__":
    conn = init_db()
    scrape_all_terms(conn)
    print("Scraping complete. Data saved to sixt_terms.db.")
    conn.close() 