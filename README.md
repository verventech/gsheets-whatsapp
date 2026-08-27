# Google Sheets & WhatsApp Automation

This project is a Python-based automation script that integrates Google Sheets with WhatsApp. It utilizes Google Cloud Service Account credentials to interact with Sheets and the PyWhatKit library to automate sending WhatsApp messages.

## 🚀 Features
* Read and process data directly from Google Sheets.
* Automate sending WhatsApp messages via `pywhatkit`.
* Secure handling of Google Cloud credentials.

## 📋 Prerequisites
Before you begin, ensure you have the following installed and set up:
* **Python 3.8+** installed on your machine.
* A **Google Cloud Project** with the Google Sheets API and Google Drive API enabled.
* A **Service Account** with a generated JSON key.
* **WhatsApp Web** logged in on your default web browser (required for PyWhatKit).

## 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone git@github.com:verventech/gsheets-whatsapp.git
cd gsheets-whatsapp
```

**2. Set up the Virtual Environment**
It is highly recommended to use a virtual environment to manage dependencies.
```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Activate the virtual environment (Mac/Linux)
source .venv/bin/activate
```

**3. Install Dependencies**
*(Note: Ensure you have a `requirements.txt` file. If not, install `pywhatkit`, `gspread`, and `google-auth` manually).*
```bash
pip install -r requirements.txt
```

## 🔒 Configuration (Credentials)

This project requires a Google Service Account key to access Google Sheets. 

1. Obtain your `credentials.json` file from your Google Cloud Console.
2. Place the `credentials.json` file in the **root directory** of this project.
3. Share your target Google Sheet with the `client_email` found inside your `credentials.json` file (give it Editor access).

> **⚠️ Security Warning:** NEVER commit `credentials.json` to version control. It is already added to the `.gitignore` file to prevent accidental uploads.

## 💻 Usage

Make sure your virtual environment is active and your default browser has an active WhatsApp Web session.

Run the main script:
```bash
python lab-tacker-whatsapp.py
```

## 📂 File Structure
* `lab-tacker-whatsapp.py`: The main execution script.
* `credentials.json`: **[Local Only]** Google Cloud Service Account key.
* `PyWhatKit_DB.txt`: Auto-generated log file by the PyWhatKit library containing message history.
* `.venv/`: **[Local Only]** Python virtual environment.
* `.gitignore`: Ensures secrets and local environments are not pushed to GitHub.

## 📝 Troubleshooting
* **Script opens browser but doesn't send message:** Ensure your browser is completely logged into WhatsApp Web before running the script. PyWhatKit relies on web automation.
* **Google Sheets API Error:** Double-check that you shared the specific Google Sheet with the service account email address.
