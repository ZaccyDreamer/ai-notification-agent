# 🤖 AI Notification Agent

Automated agent that sends scholarships, jobs, tenders, investment insights, and email alerts to your WhatsApp.

## 📋 What It Does

| Module | Description |
|--------|-------------|
| 📚 **Scholarship Finder** | Searches Nakuru County & Gilgil Sub-county bursaries |
| 💼 **UON Monitor** | Monitors University of Nairobi careers portal |
| 📧 **Email Parser** | Checks Gmail for money/food related emails |
| 🏗️ **Tender Finder** | Finds government & parastatal tenders |
| 📈 **Investment Advisor** | Treasury bills, bonds, NSE trends |

## 📱 WhatsApp Delivery

- **Number:** 0798581825
- **Schedule:** 6AM & 6PM daily digest

---

## 🚀 Quick Setup

### 1. Install Python Dependencies

```bash
cd ai-notification-agent
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` file with your credentials:

#### Option A: WhatsApp (Twilio) - Recommended
1. Go to [twilio.com](https://www.twilio.com) and create free trial account
2. Get Account SID and Auth Token from Twilio Console
3. Verify your WhatsApp number with Twilio
4. Add to `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_sid_here
   TWILIO_AUTH_TOKEN=your_token_here
   ```

#### Option B: Email Alerts (Gmail)
1. Enable 2-Factor Authentication on Gmail
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a 16-character password
4. Add to `.env`:
   ```
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ```

### 3. Test the Agent

```bash
# Run once to test
python main.py --once
```

### 4. Run on Schedule

```bash
# Runs continuously at 6AM & 6PM
python main.py
```

---

## 📁 Project Structure

```
ai-notification-agent/
├── config.py              # Configuration settings
├── main.py                # Main scheduler
├── scholarship_finder.py  # Nakuru/Gilgil bursaries
├── uon_monitor.py         # UON jobs & internships
├── email_parser.py        # Gmail important alerts
├── tender_finder.py       # Government tenders
├── investment_advisor.py  # Treasury, bonds, NSE
├── whatsapp_sender.py    # Twilio WhatsApp integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

---

## ⚠️ Important Notes

1. **Free Options Available:**
   - Twilio offers free trial (KSh 1,000+ credits)
   - Gmail App Password is free
   - All Python libraries are free

2. **Email Setup Required:**
   - For email alerts, you MUST set up Gmail App Password
   - Without it, email module will show reminders only

3. **WhatsApp Setup:**
   - Twilio trial requires WhatsApp sandbox setup
   - Follow Twilio's WhatsApp onboarding

4. **Existing Projects:**
   - This agent is in separate folder (`ai-notification-agent/`)
   - Does NOT affect your `peniel_web/` or `embedded_systems/` projects

---

## 🔧 Troubleshooting

### "Twilio not installed"
```bash
pip install twilio
```

### "Invalid credentials"
- Check your `.env` file has correct values
- Verify Twilio account is active

### "Email login failed"
- Ensure App Password is correct (16 characters with spaces)
- Check 2FA is enabled on Gmail

### "Module not found"
```bash
pip install -r requirements.txt
```

---

## 📞 Support

For issues or questions, check:
- Twilio Console: console.twilio.com
- Gmail Security: myaccount.google.com/security
- CBK Treasury: centralbank.go.ke/treasury-bills/

---

**Agent Created:** April 2026
**Target WhatsApp:** 0798581825