import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_SHEET_ID

def get_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
    client = gspread.authorize(creds)
    return client.open_by_key(GOOGLE_SHEET_ID).sheet1

def search_sheet_for_entity(entity_id):
    sheet = get_google_sheet()
    data = sheet.get_all_records()

    for row in data:
        if row.get("ID", "").upper() == entity_id.upper():
            return row
    return None