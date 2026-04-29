"""
Email Parser - Monitors Gmail accounts for important financial emails
Checks both zaccmunuhe7@gmail.com and sph3232142025@students.uonbi.ac.ke
"""

import imaplib
import email
import logging
from datetime import datetime, timedelta
from email.header import decode_header
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailParser:
    """Parses emails for important financial and food-related notifications"""
    
    def __init__(self):
        self.results = []
        
    def parse_email(self, email_msg):
        """Parse a single email message"""
        subject = ""
        sender = ""
        date = ""
        
        # Get subject
        if email_msg["Subject"]:
            subject = email_msg["Subject"]
        
        # Get sender
        if email_msg["From"]:
            sender = email_msg["From"]
        
        # Get date
        if email_msg["Date"]:
            date = email_msg["Date"]
        
        return {
            'subject': subject,
            'sender': sender,
            'date': date,
            'preview': subject[:100]
        }
    
    def check_gmail(self, email_address, app_password):
        """Check Gmail account for important emails"""
        important_emails = []
        
        if not app_password:
            logger.info(f"No password configured for {email_address}")
            return important_emails
        
        try:
            # Connect to Gmail
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_address, app_password)
            
            # Select inbox
            mail.select('INBOX')
            
            # Search for emails from last 7 days
            from_date = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
            typ, msg_ids = mail.search(None, f'SINCE {from_date}')
            
            email_ids = msg_ids[0].split()
            
            # Keywords to search for
            money_keywords = [
                'allowance', 'stipend', 'payment', 'refund', 'salary',
                'bank transfer', 'mpesa', 'money', 'funds', 'bursary',
                'scholarship award', 'financial support', 'grant',
                'transaction', 'deposit', 'withdrawal', 'balance'
            ]
            
            food_keywords = [
                'meal', 'food', 'canteen', 'lunch', 'breakfast', 'dinner',
                'catering', 'refreshment', 'snack', 'cafe', 'mess'
            ]
            
            important_keywords = money_keywords + food_keywords
            
            # Check last 50 emails
            for email_id in email_ids[-50:]:
                typ, msg_data = mail.fetch(email_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg['Subject'] or ""
                        sender = msg['From'] or ""
                        
                        # Check for important keywords
                        subject_lower = subject.lower()
                        for kw in important_keywords:
                            if kw.lower() in subject_lower:
                                important_emails.append({
                                    'account': email_address,
                                    'subject': subject,
                                    'sender': sender,
                                    'date': msg['Date'],
                                    'keyword': kw
                                })
                                break
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            logger.info(f"Error checking {email_address}: {e}")
        
        return important_emails
    
    def get_static_alerts(self):
        """Return static important email reminders"""
        return [
            {
                'account': 'zaccmunuhe7@gmail.com',
                'subject': '💡 REMINDER: Check your Gmail regularly',
                'sender': 'System',
                'date': datetime.now().strftime("%Y-%m-%d"),
                'keyword': 'reminder',
                'note': 'Check inbox for: bank statements, M-Pesa transactions, scholarship updates, allowance notifications'
            },
            {
                'account': 'sph3232142025@students.uonbi.ac.ke',
                'subject': '💡 REMINDER: Check student email regularly',
                'sender': 'System',
                'date': datetime.now().strftime("%Y-%m-%d"),
                'keyword': 'reminder',
                'note': 'Check student email for: exam timetables, fee statements, allowance updates, attachment placements, graduation info'
            }
        ]
    
    def find_all(self, gmail_password="", student_password=""):
        """Find all important emails"""
        logger.info("Checking emails for important notifications...")
        
        all_emails = []
        
        # Add static reminders
        all_emails.extend(self.get_static_alerts())
        
        # Check personal Gmail
        if gmail_password:
            try:
                emails = self.check_gmail("zaccmunuhe7@gmail.com", gmail_password)
                all_emails.extend(emails)
            except Exception as e:
                logger.info(f"Gmail check error: {e}")
        
        # Check student email
        if student_password:
            try:
                emails = self.check_gmail("sph3232142025@students.uonbi.ac.ke", student_password)
                all_emails.extend(emails)
            except Exception as e:
                logger.info(f"Student email check error: {e}")
        
        self.results = all_emails
        return all_emails
    
    def format_for_whatsapp(self):
        """Format results for WhatsApp message"""
        if not self.results:
            return "📧 *IMPORTANT EMAILS*\n\nNo new important emails found."
        
        message = "📧 *IMPORTANT EMAIL ALERTS*\n\n"
        
        # Group by account
        personal = [e for e in self.results if 'zaccmunuhe7' in e.get('account', '')]
        student = [e for e in self.results if 'students.uonbi' in e.get('account', '')]
        
        if personal:
            message += "📱 *Personal Gmail (zaccmunuhe7@gmail.com)*\n"
            for e in personal[:5]:
                message += f"  • {e['subject'][:60]}...\n"
            message += "\n"
        
        if student:
            message += "🎓 *Student Email (sph3232142025@students.uonbi.ac.ke)*\n"
            for e in student[:5]:
                message += f"  • {e['subject'][:60]}...\n"
            message += "\n"
        
        message += "_💡 Tip: Enable 2FA and use App Password for email access_"
        return message


if __name__ == "__main__":
    parser = EmailParser()
    # Note: You need to set up App Passwords in Gmail
    results = parser.find_all()
    print(f"Found {len(results)} important emails")
    print(parser.format_for_whatsapp())