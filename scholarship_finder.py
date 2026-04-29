"""
Scholarship & Bursary Finder for Nakuru County & Gilgil Sub-county
Scrapes education portals, NGO websites, and government bursary programs
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScholarshipFinder:
    """Finds scholarships and bursaries in Nakuru and Gilgil area"""
    
    def __init__(self):
        self.results = []
        self.keywords = [
            "bursary", "scholarship", "financial aid", "grant", 
            "CDF scholarship", "county bursary", "education fund"
        ]
        self.location_keywords = ["Nakuru", "Gilgil", "Nakuru County", "Rongai", "Naivasha", "Molo"]
        
    def search_nakuru_education(self):
        """Search Nakuru County Education Portal"""
        opportunities = []
        
        # Nakuru County Government - Education Department
        urls_to_try = [
            "https://nakuru.go.ke/education",
            "https://www.nakuru.go.ke/services/education-bursary",
        ]
        
        for url in urls_to_try:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    # Extract scholarship info
                    text = soup.get_text()
                    for keyword in self.keywords:
                        if keyword.lower() in text.lower():
                            opportunities.append({
                                'source': 'Nakuru County Government',
                                'url': url,
                                'type': 'Bursary/Scholarship',
                                'found': datetime.now().strftime("%Y-%m-%d")
                            })
            except Exception as e:
                logger.info(f"Could not access {url}: {e}")
                
        return opportunities
    
    def search_cdf_portals(self):
        """Search CDF bursary opportunities"""
        opportunities = []
        
        # CDF offices in Nakuru sub-counties
        cdf_locations = [
            ("Gilgil CDF", "https://gilgil.cdf.go.ke"),
            ("Nakuru Town West CDF", "https://nakuruwest.cdf.go.ke"),
            ("Nakuru Town East CDF", "https://nakurueast.cdf.go.ke"),
            ("Rongai CDF", "https://rongai.cdf.go.ke"),
            ("Naivasha CDF", "https://naivasha.cdf.go.ke"),
        ]
        
        for name, url in cdf_locations:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    opportunities.append({
                        'source': name,
                        'url': url,
                        'type': 'CDF Bursary',
                        'found': datetime.now().strftime("%Y-%m-%d")
                    })
            except:
                pass
                
        return opportunities
    
    def search_ngos(self):
        """Search for NGO bursaries in Nakuru region"""
        opportunities = []
        
        # Common NGOs offering bursaries
        ngo_urls = [
            ("JFFoS - Jobs for Youth", "https://www.labour.go.ke"),
            ("Kenya Red Cross - Nakuru", "https://www.redcross.or.ke"),
            ("World Vision - Nakuru", "https://www.wvi.org/kenya"),
        ]
        
        for name, url in ngo_urls:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    opportunities.append({
                        'source': name,
                        'url': url,
                        'type': 'NGO Bursary',
                        'found': datetime.now().strftime("%Y-%m-%d")
                    })
            except:
                pass
                
        return opportunities
    
    def get_static_opportunities(self):
        """Return known static bursary opportunities"""
        return [
            {
                'source': 'Nakuru County Government - Education',
                'url': 'https://nakuru.go.ke',
                'type': 'County Bursary',
                'description': 'Annual bursary for Nakuru residents - Check County Government website during application periods (usually Jan-March)',
                'eligibility': 'Nakuru County residents, students in secondary/university'
            },
            {
                'source': 'Gilgil CDF',
                'url': 'https://gilgil.go.ke',
                'type': 'CDF Bursary',
                'description': 'Gilgil Constituency Development Fund bursaries for local students',
                'eligibility': 'Gilgil residents, students in need'
            },
            {
                'source': 'KUCCPS - Government Bursary',
                'url': 'https://www.kuccps.net',
                'type': 'Government Bursary',
                'description': 'Government-sponsored students can apply for bursary through KUCCPS',
                'eligibility': 'Government-sponsored students'
            },
            {
                'source': 'HELB - Higher Education Loans Board',
                'url': 'https://www.helb.co.ke',
                'type': 'Student Loan/Bursary',
                'description': 'Loans and bursaries for Kenyan university students',
                'eligibility': 'Kenyan students in recognized institutions'
            },
            {
                'source': 'Nakuru MCK - Church Bursaries',
                'url': 'https://www.mck.or.ke',
                'type': 'Church Bursary',
                'description': 'Methodist Church Kenya offers bursaries through local churches',
                'eligibility': 'Church members, students in need'
            }
        ]
    
    def find_all(self):
        """Find all scholarship opportunities"""
        logger.info("Searching for scholarships and bursaries...")
        
        all_opportunities = []
        
        # Add static opportunities
        all_opportunities.extend(self.get_static_opportunities())
        
        # Try dynamic searches
        try:
            all_opportunities.extend(self.search_nakuru_education())
        except Exception as e:
            logger.info(f"Dynamic search error: {e}")
        
        try:
            all_opportunities.extend(self.search_cdf_portals())
        except Exception as e:
            logger.info(f"CDF search error: {e}")
        
        self.results = all_opportunities
        return all_opportunities
    
    def format_for_whatsapp(self):
        """Format results for WhatsApp message"""
        if not self.results:
            return "📚 *SCHOLARSHIPS & BURSARIES*\n\nNo new opportunities found. Check HELB (helb.co.ke) and KUCCPS regularly."
        
        message = "📚 *SCHOLARSHIPS & BURSARIES*\n\n"
        for i, opp in enumerate(self.results[:10], 1):  # Limit to 10
            message += f"{i}. *{opp['source']}*\n"
            message += f"   📍 Type: {opp['type']}\n"
            message += f"   🔗 {opp['url']}\n"
            if 'description' in opp:
                message += f"   📝 {opp['description'][:80]}...\n"
            message += "\n"
        
        message += "_Check these links regularly for application deadlines_"
        return message


if __name__ == "__main__":
    finder = ScholarshipFinder()
    results = finder.find_all()
    print(f"Found {len(results)} opportunities")
    print(finder.format_for_whatsapp())