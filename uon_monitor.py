"""
UON (University of Nairobi) Job & Internship Monitor
Scrapes Chiromo/Main Campus career portal and student portal
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UONMonitor:
    """Monitors UON career portal for jobs and internships"""
    
    def __init__(self):
        self.results = []
        self.base_url = "https://careers.uonbi.ac.ke"
        
    def search_careers(self):
        """Search UON Careers Portal"""
        opportunities = []
        
        urls_to_try = [
            ("Jobs", f"{self.base_url}/jobs"),
            ("Internships", f"{self.base_url}/internships"),
            ("Careers", self.base_url),
        ]
        
        for name, url in urls_to_try:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    
                    # Look for job/internship listings
                    # Common patterns in UON career sites
                    job_cards = soup.find_all(['div', 'article', 'li'], class_=re.compile(r'job|career|position|listing', re.I))
                    
                    for card in job_cards[:5]:  # Limit results
                        title = card.get_text(strip=True)[:100]
                        if title and len(title) > 10:
                            opportunities.append({
                                'source': 'UON Careers',
                                'title': title,
                                'url': url,
                                'type': name,
                                'found': datetime.now().strftime("%Y-%m-%d")
                            })
                            
            except Exception as e:
                logger.info(f"Error accessing {url}: {e}")
        
        return opportunities
    
    def search_student_portal(self):
        """Search UON Student Portal for announcements"""
        opportunities = []
        
        # Student portal URLs (may require login)
        urls = [
            ("Student Portal", "https://student.uonbi.ac.ke"),
            ("UON Main Website", "https://uonbi.ac.ke"),
            ("Career Services", "https://careers.uonbi.ac.ke"),
        ]
        
        for name, url in urls:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    text = soup.get_text().lower()
                    
                    # Look for relevant keywords
                    keywords = ['internship', 'job', 'career fair', 'vacancy', 'employment', 'attachment']
                    for kw in keywords:
                        if kw in text:
                            opportunities.append({
                                'source': 'UON ' + name,
                                'url': url,
                                'type': 'Announcements',
                                'found': datetime.now().strftime("%Y-%m-%d")
                            })
                            break
                            
            except Exception as e:
                logger.info(f"Error accessing {url}: {e}")
        
        return opportunities
    
    def get_known_opportunities(self):
        """Return known UON opportunities"""
        return [
            {
                'source': 'UON Careers Portal',
                'url': 'https://careers.uonbi.ac.ke',
                'type': 'Jobs & Internships',
                'description': 'Check regularly for job postings and internship opportunities from corporate partners',
                'tips': 'Create profile on portal to get notifications'
            },
            {
                'source': 'UON Student Portal',
                'url': 'https://student.uonbi.ac.ke',
                'type': 'Student Announcements',
                'description': 'Login to check for career fairs, attachment opportunities, and university announcements',
                'tips': 'Check your student email regularly'
            },
            {
                'source': 'Chiromo Campus Career Office',
                'url': 'https://chiromo.uonbi.ac.ke',
                'type': 'Campus Career Services',
                'description': 'Visit Chiromo Campus career office for internship placements and job leads',
                'tips': 'Visit in person during office hours'
            },
            {
                'source': 'LinkedIn - UON Alumni',
                'url': 'https://linkedin.com',
                'type': 'Networking',
                'description': 'Join UON alumni groups on LinkedIn for job opportunities',
                'tips': 'Update your profile and connect with alumni'
            },
            {
                'source': 'Brighter Monday',
                'url': 'https://www.brightermonday.com',
                'type': 'Job Board',
                'description': 'Popular Kenyan job board with many entry-level opportunities',
                'tips': 'Set up job alerts for your field'
            },
            {
                'source': 'MyJobMag',
                'url': 'https://www.myjobmag.co.ke',
                'type': 'Job Board',
                'description': 'Kenyan job aggregation site with daily updates',
                'tips': 'Check daily for new postings'
            }
        ]
    
    def find_all(self):
        """Find all UON opportunities"""
        logger.info("Searching UON careers and jobs...")
        
        all_opportunities = []
        
        # Add known opportunities
        all_opportunities.extend(self.get_known_opportunities())
        
        # Try dynamic searches
        try:
            all_opportunities.extend(self.search_careers())
        except Exception as e:
            logger.info(f"Careers search error: {e}")
        
        try:
            all_opportunities.extend(self.search_student_portal())
        except Exception as e:
            logger.info(f"Student portal error: {e}")
        
        # Remove duplicates based on URL
        seen = set()
        unique_opportunities = []
        for opp in all_opportunities:
            if opp['url'] not in seen:
                seen.add(opp['url'])
                unique_opportunities.append(opp)
        
        self.results = unique_opportunities
        return unique_opportunities
    
    def format_for_whatsapp(self):
        """Format results for WhatsApp message"""
        if not self.results:
            return "💼 *UON JOBS & INTERNSHIPS*\n\nNo new opportunities found. Check careers.uonbi.ac.ke regularly."
        
        message = "💼 *UON JOBS & INTERNSHIPS*\n\n"
        for i, opp in enumerate(self.results[:10], 1):
            message += f"{i}. *{opp['source']}*\n"
            message += f"   📍 Type: {opp['type']}\n"
            message += f"   🔗 {opp['url']}\n"
            if 'description' in opp:
                message += f"   📝 {opp['description'][:80]}...\n"
            if 'tips' in opp:
                message += f"   💡 {opp['tips']}\n"
            message += "\n"
        
        message += "_Visit these portals regularly for new opportunities_"
        return message


if __name__ == "__main__":
    monitor = UONMonitor()
    results = monitor.find_all()
    print(f"Found {len(results)} opportunities")
    print(monitor.format_for_whatsapp())