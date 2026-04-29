"""
Investment Advisor - Monitors treasury bills, bonds, and investment trends
Provides investment insights for Kenya
"""

import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import re
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvestmentAdvisor:
    """Monitors investment opportunities and market trends"""
    
    def __init__(self):
        self.results = []
        
    def get_treasury_rates(self):
        """Get current Treasury Bill rates from CBK"""
        rates = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(
                'https://www.centralbank.go.ke/treasury-bills/',
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                text = soup.get_text()
                
                # Look for rate information
                if 'treasury' in text.lower() or 'rate' in text.lower():
                    rates.append({
                        'source': 'Central Bank of Kenya',
                        'url': 'https://www.centralbank.go.ke/treasury-bills/',
                        'type': 'Treasury Bills',
                        'description': 'Check CBK website for current Treasury Bill and Bond rates',
                        'note': 'Rates change weekly - visit CBK for latest rates'
                    })
                    
        except Exception as e:
            logger.info(f"CBK error: {e}")
        
        return rates
    
    def get_nse_trends(self):
        """Get NSE market trends"""
        trends = []
        
        urls = [
            ("NSE - Nairobi Securities Exchange", "https://www.nse.co.ke"),
            ("NSE - Market Data", "https://www.nse.co.ke/market-data"),
        ]
        
        for name, url in urls:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    trends.append({
                        'source': name,
                        'url': url,
                        'type': 'Stock Market',
                        'description': 'Nairobi Securities Exchange - equities, bonds, and derivatives',
                        'note': 'Check for listed companies and market performance'
                    })
            except:
                pass
                
        return trends
    
    def get_investment_platforms(self):
        """Get popular investment platforms in Kenya"""
        platforms = []
        
        investment_sources = [
            ("Cytonn Investments", "https://cytonn.com/investments"),
            ("Britam Investments", "https://www.britam.com/investments"),
            ("Old Mutual", "https://www.oldmutual.co.ke/investments"),
            ("Stanbic Investments", "https://www.stanbicbank.com/ke/investments"),
            ("Sidian Bank", "https://www.sidianbank.co.ke/investments"),
            ("Co-op Trust", "https://www.cooptrust.co.ke"),
            ("APA Pensions", "https://www.apapensions.com"),
            ("Britam Pensions", "https://www.britampensions.com"),
        ]
        
        for name, url in investment_sources:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    platforms.append({
                        'source': name,
                        'url': url,
                        'type': 'Investment Platform',
                        'description': f'Investment and wealth management services',
                        'note': 'Contact for current returns and minimum investment'
                    })
            except:
                pass
                
        return platforms
    
    def get_static_insights(self):
        """Return static investment insights"""
        return [
            {
                'source': 'Treasury Bills - CBK',
                'url': 'https://www.centralbank.go.ke/treasury-bills/',
                'type': 'Fixed Income',
                'description': 'Government securities with rates typically 10-15% p.a.',
                'rates_info': '91-day: ~10.5%, 182-day: ~11.5%, 364-day: ~12.5% (varies weekly)',
                'tips': 'Minimum investment KSh 100,000 through primary dealers'
            },
            {
                'source': 'Treasury Bonds',
                'url': 'https://www.centralbank.go.ke/treasury-bonds/',
                'type': 'Fixed Income',
                'description': 'Longer-term government bonds (2-30 years)',
                'rates_info': '2-year: ~11%, 5-year: ~12%, 10-year: ~13% (varies)',
                'tips': 'Good for long-term investors seeking stable returns'
            },
            {
                'source': 'NSE - Nairobi Securities Exchange',
                'url': 'https://www.nse.co.ke',
                'type': 'Equities',
                'description': 'Stock market - buy shares in listed companies',
                'popular_stocks': 'KCB, Safaricom, Equity, Kenya Power, EABL, BAT',
                'tips': 'Start with blue-chip stocks, use a licensed stockbroker'
            },
            {
                'source': 'Money Market Funds',
                'url': 'https://www.cytonn.com/investments',
                'type': 'Collective Investment',
                'description': 'Low-risk fund investments (like Cytonn, Old Mutual)',
                'returns': 'Typically 8-12% p.a.',
                'tips': 'Low minimum investment (from KSh 5,000), easy to access'
            },
            {
                'source': 'SACCOs',
                'url': 'https://www.sacco.go.ke',
                'type': 'Cooperative Investment',
                'description': 'Savings and Credit Cooperative societies',
                'tips': 'Join a reputable SACCO for dividends and loans'
            },
            {
                'source': 'Real Estate',
                'url': 'https://property24.co.ke',
                'type': 'Property Investment',
                'description': 'Land and rental property investments',
                'tips': 'Your existing land business (Peniel Prizac) is in this sector!'
            },
            {
                'source': 'Pension Funds',
                'url': 'https://www.rba.go.ke',
                'type': 'Retirement Investment',
                'description': 'Retirement savings through NSSF or private pension',
                'tips': 'Maximize contributions for tax benefits'
            },
            {
                'source': 'Government Bonds for Retail',
                'url': 'https://www.treasury.go.ke',
                'type': 'Retail Fixed Income',
                'description': 'Infrastructure bonds and savings bonds',
                'tips': 'Check for periodic infrastructure bond offerings'
            }
        ]
    
    def find_all(self):
        """Find all investment opportunities"""
        logger.info("Searching for investment insights...")
        
        all_insights = []
        
        # Add static insights
        all_insights.extend(self.get_static_insights())
        
        # Try dynamic searches
        try:
            all_insights.extend(self.get_treasury_rates())
        except Exception as e:
            logger.info(f"Treasury search error: {e}")
        
        try:
            all_insights.extend(self.get_nse_trends())
        except Exception as e:
            logger.info(f"NSE search error: {e}")
        
        try:
            all_insights.extend(self.get_investment_platforms())
        except Exception as e:
            logger.info(f"Platform search error: {e}")
        
        # Remove duplicates based on source
        seen = set()
        unique = []
        for ins in all_insights:
            if ins['source'] not in seen:
                seen.add(ins['source'])
                unique.append(ins)
        
        self.results = unique
        return unique
    
    def format_for_whatsapp(self):
        """Format results for WhatsApp message"""
        if not self.results:
            return "📈 *INVESTMENT OPPORTUNITIES*\n\nNo investment data available."
        
        message = "📈 *INVESTMENT & MARKET INSIGHTS*\n\n"
        
        # Treasury rates section
        message += "💰 *TREASURY & BONDS*\n"
        treasury = [r for r in self.results if 'Treasury' in r.get('source', '') or 'Bond' in r.get('source', '')]
        for t in treasury[:3]:
            message += f"  • {t['source']}: {t.get('description', '')[:60]}...\n"
        message += "\n"
        
        # Stock market section
        message += "📊 *STOCK MARKET (NSE)*\n"
        nse = [r for r in self.results if 'NSE' in r.get('source', '') or 'Securities' in r.get('source', '')]
        for n in nse[:2]:
            message += f"  • {n['source']}: {n.get('description', '')[:60]}...\n"
        message += "\n"
        
        # Other investments
        message += "🏦 *OTHER INVESTMENTS*\n"
        other = [r for r in self.results if 'Treasury' not in r.get('source', '') and 'NSE' not in r.get('source', '') and 'Bond' not in r.get('source', '')][:5]
        for o in other:
            message += f"  • {o['source']}: {o.get('description', '')[:50]}...\n"
        
        message += "\n_💡 Tip: Diversify across asset classes for best returns_"
        return message


if __name__ == "__main__":
    advisor = InvestmentAdvisor()
    results = advisor.find_all()
    print(f"Found {len(results)} investment insights")
    print(advisor.format_for_whatsapp())