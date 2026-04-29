"""
AI Notification Agent - Main Orchestrator
Runs all modules and sends WhatsApp digests
Schedule: 6AM and 6PM daily
"""

import schedule
import time
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Import all modules
from scholarship_finder import ScholarshipFinder
from uon_monitor import UONMonitor
from email_parser import EmailParser
from tender_finder import TenderFinder
from investment_advisor import InvestmentAdvisor
from whatsapp_sender import WhatsAppSender
import config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AINotificationAgent:
    """Main agent that coordinates all notification modules"""
    
    def __init__(self):
        self.whatsapp_number = config.WHATSAPP_NUMBER
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        
        # Initialize all modules
        self.scholarship_finder = ScholarshipFinder()
        self.uon_monitor = UONMonitor()
        self.email_parser = EmailParser()
        self.tender_finder = TenderFinder()
        self.investment_advisor = InvestmentAdvisor()
        self.whatsapp_sender = WhatsAppSender(
            self.twilio_sid,
            self.twilio_token
        )
        
    def run_daily_digest(self):
        """Run the complete daily digest"""
        logger.info("=" * 50)
        logger.info("Starting daily digest...")
        logger.info("=" * 50)
        
        try:
            # 1. Get scholarships
            logger.info("Fetching scholarships...")
            scholarships = self.scholarship_finder.find_all()
            scholarship_msg = self.scholarship_finder.format_for_whatsapp()
            logger.info(f"Found {len(scholarships)} scholarship opportunities")
            
            # 2. Get UON jobs
            logger.info("Fetching UON jobs...")
            jobs = self.uon_monitor.find_all()
            job_msg = self.uon_monitor.format_for_whatsapp()
            logger.info(f"Found {len(jobs)} job opportunities")
            
            # 3. Get important emails
            logger.info("Checking emails...")
            gmail_pass = os.getenv("GMAIL_APP_PASSWORD", "")
            student_pass = os.getenv("STUDENT_EMAIL_PASSWORD", "")
            emails = self.email_parser.find_all(gmail_pass, student_pass)
            email_msg = self.email_parser.format_for_whatsapp()
            logger.info(f"Found {len(emails)} important emails")
            
            # 4. Get tenders
            logger.info("Fetching tenders...")
            tenders = self.tender_finder.find_all()
            tender_msg = self.tender_finder.format_for_whatsapp()
            logger.info(f"Found {len(tenders)} tender opportunities")
            
            # 5. Get investment insights
            logger.info("Fetching investment insights...")
            investments = self.investment_advisor.find_all()
            investment_msg = self.investment_advisor.format_for_whatsapp()
            logger.info(f"Found {len(investments)} investment insights")
            
            # Send to WhatsApp
            logger.info("Sending WhatsApp digest...")
            result = self.whatsapp_sender.send_digest(
                self.whatsapp_number,
                scholarship_msg,
                job_msg,
                email_msg,
                tender_msg,
                investment_msg
            )
            
            if result.get("success"):
                logger.info("✅ Daily digest sent successfully!")
            else:
                logger.info(f"❌ Failed to send: {result}")
                
        except Exception as e:
            logger.error(f"Error in daily digest: {e}")
    
    def run_scheduled(self):
        """Run the agent on schedule"""
        # Schedule morning digest
        schedule.every().day.at(config.MORNING_DIGEST).do(self.run_daily_digest)
        
        # Schedule evening digest
        schedule.every().day.at(config.EVENING_DIGEST).do(self.run_daily_digest)
        
        logger.info(f"📅 Scheduled digests at {config.MORNING_DIGEST} and {config.EVENING_DIGEST}")
        logger.info("Press Ctrl+C to stop")
        
        # Run once immediately for testing
        logger.info("\n" + "=" * 50)
        logger.info("Running initial digest for testing...")
        logger.info("=" * 50 + "\n")
        self.run_daily_digest()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║       AI NOTIFICATION AGENT - SCHEDULER                  ║
    ╠══════════════════════════════════════════════════════════╣
    ║  📚 Scholarships/Bursaries (Nakuru/Gilgil)               ║
    ║  💼 UON Jobs & Internships                                ║
    ║  📧 Email Alerts (Money/Food)                            ║
    ║  🏗️ Government Tenders                                   ║
    ║  📈 Investment Opportunities                             ║
    ╠══════════════════════════════════════════════════════════╣
    ║  WhatsApp: 0798581825                                    ║
    ║  Schedule: 6AM & 6PM daily                               ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    agent = AINotificationAgent()
    
    # Check if running in scheduled mode or single run
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        # Run once and exit
        agent.run_daily_digest()
    else:
        # Run on schedule
        agent.run_scheduled()


if __name__ == "__main__":
    main()