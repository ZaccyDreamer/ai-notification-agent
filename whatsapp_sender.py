"""
WhatsApp Message Sender - Uses Twilio to send notifications
Sends all gathered information to user's WhatsApp
"""

import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppSender:
    """Sends WhatsApp messages via Twilio"""
    
    def __init__(self, account_sid="", auth_token="", from_number="whatsapp:+14155238886"):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.client = None
        
        if account_sid and auth_token:
            try:
                from twilio.rest import Client
                self.client = Client(account_sid, auth_token)
                logger.info("Twilio client initialized")
            except ImportError:
                logger.info("Twilio not installed - will use mock mode")
        else:
            logger.info("Twilio credentials not configured - using mock mode")
    
    def send_message(self, to_number, message):
        """Send a WhatsApp message - splits if too long"""
        # Format number (remove leading 0, add +254)
        if to_number.startswith("0"):
            to_number = "+254" + to_number[1:]
        elif not to_number.startswith("+"):
            to_number = "+254" + to_number
        
        to_whatsapp = f"whatsapp:{to_number}"
        
        if self.client:
            try:
                # Split message if too long (Twilio limit is 1600 chars for concatenated)
                max_length = 1500  # Safe limit
                if len(message) > max_length:
                    # Split into parts
                    parts = []
                    for i in range(0, len(message), max_length):
                        parts.append(message[i:i+max_length])
                    
                    for idx, part in enumerate(parts):
                        if idx > 0:
                            part = f"[{idx+1}/{len(parts)}] " + part
                        twilio_message = self.client.messages.create(
                            from_=self.from_number,
                            body=part,
                            to=to_whatsapp
                        )
                        logger.info(f"Message part {idx+1} sent: {twilio_message.sid}")
                    return {"success": True, "parts": len(parts)}
                else:
                    twilio_message = self.client.messages.create(
                        from_=self.from_number,
                        body=message,
                        to=to_whatsapp
                    )
                    logger.info(f"Message sent: {twilio_message.sid}")
                    return {"success": True, "sid": twilio_message.sid}
            except Exception as e:
                logger.info(f"Twilio error: {e}")
                return {"success": False, "error": str(e)}
        else:
            # Mock mode - just print the message
            logger.info(f"MOCK MODE - Would send to {to_whatsapp}:")
            logger.info(f"Message: {message[:200]}...")
            return {"success": True, "mode": "mock", "note": "Install twilio and add credentials to .env to send real messages"}
    
    def send_digest(self, to_number, scholarship_msg, job_msg, email_msg, tender_msg, investment_msg):
        """Send a complete daily digest"""
        
        digest = f"""🤖 *AI NOTIFICATION AGENT - DAILY DIGEST*
━━━━━━━━━━━━━━━━━━━━━━
📅 {datetime.now().strftime("%A, %d %B %Y")}

{scholarship_msg}

━━━━━━━━━━━━━━━━━━━━━━

{job_msg}

━━━━━━━━━━━━━━━━━━━━━━

{email_msg}

━━━━━━━━━━━━━━━━━━━━━━

{tender_msg}

━━━━━━━━━━━━━━━━━━━━━━

{investment_msg}

━━━━━━━━━━━━━━━━━━━━━━
💬 Reply HELP for assistance
📝 Reply STOP to unsubscribe
"""
        
        return self.send_message(to_number, digest)
    
    def send_test(self, to_number):
        """Send a test message"""
        test_msg = f"""✅ *AI Notification Agent - TEST*

Hello! This is a test message from your AI Notification Agent.

If you receive this, WhatsApp integration is working!

📋 *What I'll notify you about:*
• Scholarships & Bursaries (Nakuru/Gilgil)
• UON Jobs & Internships
• Important Emails (money/food related)
• Government Tenders
• Investment Opportunities

⏰ I'll send updates twice daily (6AM & 6PM)

Stay tuned for your first daily digest!"""
        
        return self.send_message(to_number, test_msg)


def send_whatsapp_message(to_number, message, account_sid="", auth_token=""):
    """Helper function to send a WhatsApp message"""
    sender = WhatsAppSender(account_sid, auth_token)
    return sender.send_message(to_number, message)


if __name__ == "__main__":
    # Test without credentials (mock mode)
    sender = WhatsAppSender()
    result = sender.send_test("0798581825")
    print(f"Result: {result}")