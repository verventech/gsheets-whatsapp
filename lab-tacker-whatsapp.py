import gspread
import requests
import re
import os
import pywhatkit
from google.oauth2.service_account import Credentials

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'credentials.json' 
SHEET_NAME = 'Lab Tracker' 
WHATSAPP_GROUP_ID = 'GGOTLD1l76BK0P7ydFJovf' 
#http://chat.whatsapp.com/GGOTLD1l76BK0P7ydFJovf?s=hd&p=i&mlu=4

# Fetch the GitHub token from your Windows environment variable
GITHUB_TOKEN = os.getenv('GH_LAB_TRK_TKN') 

# --- Authentication ---
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open("CopyLabTracker").sheet1

def check_github_for_lab(github_url, repo_name, lab_number):
    """Checks the student's GitHub repo for a file starting with the lab number."""
    if not github_url or str(github_url).lower() == "nan" or not repo_name:
        return False
        
    username = github_url.rstrip('/').split('/')[-1]
    
    # GitHub's API is naturally case-insensitive for repo names.
    # We strip spaces just to be safe.
    clean_repo_name = repo_name.strip()
    api_url = f"https://api.github.com/repos/{username}/{clean_repo_name}/contents/"
    
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        files = response.json()
        
        # Regex Explanation:
        # ^ -> starts with
        # re.escape(str(lab_number)) -> the lab number exactly
        # (?!\d) -> NOT followed by another digit (so Lab "1" won't match "10.py")
        # re.IGNORECASE -> makes any following letters case-insensitive
        pattern = re.compile(rf"^{re.escape(str(lab_number))}(?!\d)", re.IGNORECASE)
        
        for file in files:
            if file['type'] == 'file' and pattern.match(file['name']):
                return True
    return False

# --- Formatting Rules ---
format_green = {
    "backgroundColor": {"red": 0.85, "green": 0.93, "blue": 0.82},
    "textFormat": {"foregroundColor": {"red": 0.0, "green": 0.5, "blue": 0.0}}
}
format_red = {
    "backgroundColor": {"red": 0.96, "green": 0.8, "blue": 0.8},
    "textFormat": {"foregroundColor": {"red": 0.7, "green": 0.0, "blue": 0.0}}
}

def main():
    print("Fetching data from Google Sheets...")
    all_values = sheet.get_all_values()
    
    # Row 1 (Index 0) has GitHub URLs, Row 4 (Index 3) has Student Names
    github_urls = all_values[0][3:]
    student_names = all_values[3][3:]
    
    # Initialize scorecard
    scorecard = {}
    for i, name in enumerate(student_names):
        if name and str(name).lower() != "nan":
            scorecard[i] = {"name": name.strip(), "completed": 0}
    
    cells_to_update = []
    formats_to_apply = []
    total_labs = 0  
    
    # Iterate through lab assignments (Starts at Row 6 in the sheet, Index 5)
    for row_idx in range(5, len(all_values)):
        row = all_values[row_idx]
        if not row:
            continue
            
        lab_number = row[0].strip()
        repo_name = row[2].strip()
        
        if not lab_number or not repo_name:
            continue

        total_labs += 1
        print(f"Checking Lab {lab_number} in repo '{repo_name}' for all students...")

        for col_offset, url in enumerate(github_urls):
            if not url or str(url).lower() == "nan":
                continue
                
            student_col_idx = 3 + col_offset
            excel_row = row_idx + 1      
            excel_col = student_col_idx + 1 
            
            is_done = check_github_for_lab(url, repo_name, lab_number)
            
            if is_done and col_offset in scorecard:
                scorecard[col_offset]["completed"] += 1
            
            cell_value = "Yes" if is_done else "No"
            cell_format = format_green if is_done else format_red
            
            cells_to_update.append(gspread.Cell(row=excel_row, col=excel_col, value=cell_value))
            cell_address = gspread.utils.rowcol_to_a1(excel_row, excel_col)
            formats_to_apply.append({"range": cell_address, "format": cell_format})

    if cells_to_update:
        print("\nPushing all 'Yes/No' values to Google Sheets...")
        sheet.update_cells(cells_to_update)
        
    if formats_to_apply:
        print("Pushing all color formatting to Google Sheets...")
        sheet.batch_format(formats_to_apply)

    print("\n✅ Lab tracking update complete!")

    # --- 4. Send WhatsApp Notification ---
    print("Preparing to send WhatsApp group message...")
    
    message = (
        f"🤖 *Automated Lab Tracker Update*\n\n"
        f"The GitHub lab checker script has just finished running.\n"
        f"✅ Google Sheets has been updated with the latest completion statuses.\n\n"
        f"*📊 Scorecard (Out of {total_labs} Labs):*\n"
    )
    
    for col_offset, data in scorecard.items():
        message += f"• {data['name']} - Labs done: {data['completed']}/{total_labs}\n"
        
    print(f"\n--- Preview of WhatsApp Message ---\n{message}\n-----------------------------------")
    
    try:
        # Opens default Windows browser to send the message
        pywhatkit.sendwhatmsg_to_group_instantly(WHATSAPP_GROUP_ID, message, wait_time=15, tab_close=True)
        print("WhatsApp message sent successfully!")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")

if __name__ == "__main__":
    main()