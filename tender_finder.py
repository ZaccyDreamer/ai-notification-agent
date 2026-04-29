"""
Tender Finder - Scans government and parastatal tender portals
Finds available tenders in Kenya
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TenderFinder:
    """Finds government and parastatal tenders"""
    
    def __init__(self):
        self.results = []
        
    def search_kenya_tenders(self):
        """Search Kenya Government Tender Portal"""
        opportunities = []
        
        urls_to_try = [
            ("e-Procurement", "https://www.eprocurement.go.ke"),
            ("Treasury Tenders", "https://www.treasury.go.ke"),
            ("PPOA", "https://www.ppoa.go.ke"),
            ("State Department", "https://www.statehouse.go.ke/tenders"),
        ]
        
        for name, url in urls_to_try:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    text = soup.get_text().lower()
                    
                    # Check for tender-related content
                    if any(kw in text for kw in ['tender', 'procurement', 'rfq', 'quotation', 'bid']):
                        opportunities.append({
                            'source': name,
                            'url': url,
                            'type': 'Government Tender',
                            'found': datetime.now().strftime("%Y-%m-%d")
                        })
                        
            except Exception as e:
                logger.info(f"Error accessing {url}: {e}")
        
        return opportunities
    
    def search_parastatals(self):
        """Search parastatal tender portals"""
        opportunities = []
        
        parastatals = [
            ("KPLC", "https://www.kplc.co.ke/tenders"),
            ("KenPower", "https://www.kenpower.co.ke/procurement"),
            ("KenAir", "https://www.kenya-airways.com/procurement"),
            ("KRA", "https://www.kra.go.ke/tenders"),
            ("NSSF", "https://www.nssf.or.ke/tenders"),
            ("NHIF", "https://www.nhif.or.ke/tenders"),
            ("KUERC", "https://www.kuerc.go.ke/tenders"),
            ("KEMSA", "https://www.kemsa.co.ke/tenders"),
            ("KMC", "https://www.kmc.co.ke/tenders"),
            ("Nairobi Water", "https://www.nairobiwater.go.ke/tenders"),
        ]
        
        for name, url in parastatals:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    opportunities.append({
                        'source': name,
                        'url': url,
                        'type': 'Parastatal Tender',
                        'found': datetime.now().strftime("%Y-%m-%d")
                    })
            except:
                pass
                
        return opportunities
    
    def get_static_opportunities(self):
        """Return known tender portals"""
        return [
            {
                'source': 'e-Procurement Portal',
                'url': 'https://www.eprocurement.go.ke',
                'type': 'Government Tenders',
                'description': 'Official government procurement portal - all ministries and state departments',
                'tips': 'Register for free to access tender documents'
            },
            {
                'source': 'Public Procurement Authority',
                'url': 'https://www.ppoa.go.ke',
                'type': 'Procurement Regulator',
                'description': 'Regulates public procurement - has tender alerts and guidelines',
                'tips': 'Check alerts section regularly'
            },
            {
                'source': 'Treasury - GMS',
                'url': 'https://supplier.treasury.go.ke',
                'type': 'Treasury Suppliers Portal',
                'description': 'Government Supplier Management System - tender opportunities',
                'tips': 'Create supplier account for notifications'
            },
            {
                'source': 'Kenya Revenue Authority',
                'url': 'https://www.kra.go.ke/tenders',
                'type': 'KRA Tenders',
                'description': 'Tax authority tenders - often for services and IT',
                'tips': 'Check weekly for new postings'
            },
            {
                'source': 'Kenya Power',
                'url': 'https://www.kplc.co.ke/tenders',
                'type': 'KPLC Tenders',
                'description': 'Electricity utility tenders - infrastructure and services',
                'tips': 'Pre-qualify for common categories'
            },
            {
                'source': 'NHIF Tenders',
                'url': 'https://www.nhif.or.ke/tenders',
                'type': 'Health Fund Tenders',
                'description': 'National Health Insurance Fund procurement',
                'tips': 'Healthcare companies should monitor'
            },
            {
                'source': 'NSSF Tenders',
                'url': 'https://www.nssf.or.ke/tenders',
                'type': 'Pension Fund Tenders',
                'description': 'National Social Security Fund tenders',
                'tips': 'Check for construction and IT tenders'
            },
            {
                'source': 'County Tenders - Nakuru',
                'url': 'https://nakuru.go.ke/tenders',
                'type': 'County Tenders',
                'description': 'Nakuru County Government tender portal',
                'tips': 'Local businesses should register'
            }
        ]
    
    def find_all(self):
        """Find all tender opportunities"""
        logger.info("Searching for tenders...")
        
        all_opportunities = []
        
        # Add static opportunities
        all_opportunities.extend(self.get_static_opportunities())
        
        # Try dynamic searches
        try:
            all_opportunities.extend(self.search_kenya_tenders())
        except Exception as e:
            logger.info(f"Tender search error: {e}")
        
        try:
            all_opportunities.extend(self.search_parastatals())
        except Exception as e:
            logger.info(f"Parastatal search error: {e}")
        
        # Remove duplicates
        seen = set()
        unique = []
        for opp in all_opportunities:
            if opp['url'] not in seen:
                seen.add(opp['url'])
                unique.append(opp)
        
        self.results = unique
        return unique
    
    def format_for_whatsapp(self):
        """Format results for WhatsApp message"""
        if not self.results:
            return "🏗️ *TENDERS & PROCUREMENT*\n\nNo tender portals accessible currently."
        
        message = "🏗️ *TENDERS & PROCUREMENT*\n\n"
        for i, opp in enumerate(self.results[:10], 1):
            message += f"{i}. *{opp['source']}*\n"
            message += f"   📍 Type: {opp['type']}\n"
            message += f"   🔗 {opp['url']}\n"
            if 'description' in opp:
                message += f"   📝 {opp['description'][:70]}...\n"
            if 'tips' in opp:
                message += f"   💡 {opp['tips']}\n"
            message += "\n"
        
        message += "_Register on these portals for tender alerts_"
        return message


if __name__ == "__main__":
    finder = TenderFinder()
    results = finder.find_all()
    print(f"Found {len(results)} tender opportunities")
    print(finder.format_for_whatsapp())