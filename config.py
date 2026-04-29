"""
Configuration for AI Notification Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# WhatsApp Configuration
WHATSAPP_NUMBER = "+254798581825"  # 0798581825 (with country code)

# Email Configuration
GMAIL_ACCOUNTS = [
    {"email": "zaccmunuhe7@gmail.com", "app_password": os.getenv("GMAIL_APP_PASSWORD", "")},
    {"email": "sph3232142025@students.uonbi.ac.ke", "app_password": os.getenv("STUDENT_EMAIL_PASSWORD", "")}
]

# Twilio Configuration (Free Trial)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio sandbox number

# Location Focus
COUNTY_FOCUS = ["Nakuru", "Gilgil", "Nakuru County", "Gilgil Sub-county"]
SCHOOL_FOCUS = ["bursary", "scholarship", "financial aid", "CDF", "county scholarship"]

# UON URLs
UON_CAREERS_URL = "https://careers.uonbi.ac.ke"
UON_STUDENT_PORTAL = "https://student.uonbi.ac.ke"

# Investment URLs
CBK_TREASURY_URL = "https://www.centralbank.go.ke/treasury-bills/"
NSE_URL = "https://www.nse.co.ke"

# Tender URLs
KENYA_TENDERS = [
    "https://tenders.go.ke",
    "https://www.eprocurement.go.ke",
    "https://supplier.treasury.go.ke"
]

# Keywords for email filtering
MONEY_KEYWORDS = [
    "allowance", "stipend", "payment", "refund", "salary", 
    "bank transfer", "mpesa", "money", "funds", "bursary",
    "scholarship award", "financial support", "grant"
]

FOOD_KEYWORDS = [
    "meal", "food", "canteen", "lunch", "breakfast", "dinner",
    "catering", "refreshment", "snack", "cafe"
]

# Schedule times
MORNING_DIGEST = "06:00"
EVENING_DIGEST = "18:00"

# File paths
DATA_DIR = "data"
LOG_FILE = "agent.log"