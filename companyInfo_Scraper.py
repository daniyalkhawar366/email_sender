import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re

def debug_csv_file(filename):
    """Debug the CSV file to see its structure"""
    print(f"🔍 DEBUGGING: {filename}")
    print("=" * 50)
    
    try:
        # Try with pandas first
        df = pd.read_csv(filename)
        print(f"✅ Pandas successfully read {len(df)} rows")
        print(f"📊 Columns found: {list(df.columns)}")
        print(f"📋 Column count: {len(df.columns)}")
        
        # Show first few rows
        print(f"\n📄 First 3 rows:")
        for i, row in df.head(3).iterrows():
            print(f"  Row {i+1}: {dict(row)}")
        
        # Check for empty values
        print(f"\n🔍 Empty value check:")
        for col in df.columns:
            empty_count = df[col].isna().sum() + (df[col] == '').sum()
            print(f"  {col}: {empty_count} empty values")
        
        return df.columns.tolist(), len(df)
        
    except Exception as e:
        print(f"❌ Pandas failed: {e}")
        
        # Try with regular CSV reader
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                columns = reader.fieldnames
                rows = list(reader)
                
            print(f"✅ CSV reader got {len(rows)} rows")
            print(f"📊 Columns: {columns}")
            
            # Show first few rows
            print(f"\n📄 First 3 rows:")
            for i, row in enumerate(rows[:3]):
                print(f"  Row {i+1}: {row}")
            
            return columns, len(rows)
            
        except Exception as e2:
            print(f"❌ CSV reader also failed: {e2}")
            return None, 0

class FixedCompanyScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def extract_domain_from_email(self, email):
        """Extract domain and create website URLs to try"""
        if not email or '@' not in email:
            return []
            
        try:
            domain = email.split('@')[1].lower().strip()
            
            # Skip common email providers
            skip_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
            if domain in skip_domains:
                return []
            
            urls_to_try = [
                f"https://www.{domain}",
                f"https://{domain}",
                f"http://www.{domain}",
                f"http://{domain}"
            ]
            return urls_to_try
        except:
            return []

    def test_url(self, url, timeout=8):
        """Test if URL is accessible"""
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            if response.status_code == 200 and len(response.content) > 1000:
                return response.url
        except:
            pass
        return None

    def scrape_basic_info(self, url, company_name):
        """Scrape basic company info"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                meta_desc = soup.find('meta', attrs={'property': 'og:description'})
            description = meta_desc.get('content', '').strip() if meta_desc else ""
            
            # Get some body text
            body_text = self.extract_relevant_text(soup, company_name)
            
            # Combine info
            info_parts = []
            if description:
                info_parts.append(description)
            if body_text:
                info_parts.append(body_text)
            
            combined = " ".join(info_parts)
            cleaned = self.clean_text(combined)
            
            return {
                'website': url,
                'about': cleaned[:600],
                'found_info': len(cleaned) > 30
            }
            
        except Exception as e:
            print(f"    Error scraping {url}: {e}")
            return None

    def extract_relevant_text(self, soup, company_name):
        """Extract relevant text from page"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Look for content with relevant keywords
        relevant_keywords = [
            'remodel', 'renovation', 'construction', 'contractor', 'builder',
            'kitchen', 'bathroom', 'flooring', 'roofing', 'painting',
            'residential', 'commercial', 'houston', 'texas'
        ]
        
        # Get paragraphs and divs with relevant content
        relevant_text = []
        
        for element in soup.find_all(['p', 'div', 'section'], limit=20):
            text = element.get_text().strip()
            if (len(text) > 30 and 
                any(keyword in text.lower() for keyword in relevant_keywords)):
                relevant_text.append(text)
                if len(" ".join(relevant_text)) > 400:
                    break
        
        return " ".join(relevant_text)[:400]

    def clean_text(self, text):
        """Clean text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.,!?()-]', '', text)
        return text.strip()

    def create_fallback_info(self, company_name, email):
        """Create fallback when scraping fails"""
        if not company_name or company_name == 'Unknown Company':
            # Try to extract company name from email
            if email and '@' in email:
                domain = email.split('@')[1]
                company_name = domain.split('.')[0].title()
        
        # Determine business type from name
        name_lower = (company_name or '').lower()
        if any(word in name_lower for word in ['kitchen', 'bath', 'cabinet']):
            business_type = "kitchen and bathroom remodeling"
        elif 'roof' in name_lower:
            business_type = "roofing services"
        elif 'floor' in name_lower:
            business_type = "flooring services"
        elif 'paint' in name_lower:
            business_type = "painting services"
        else:
            business_type = "home remodeling and construction"
        
        return f"{company_name} is a {business_type} company serving the Houston area. They provide quality residential and commercial services to local customers."

def smart_scrape_companies(input_csv, output_csv):
    """Improved company scraping with better CSV handling"""
    
    print("🚀 FIXED COMPANY SCRAPER")
    print("=" * 50)
    
    # First, debug the CSV
    columns, row_count = debug_csv_file(input_csv)
    if not columns:
        print("❌ Cannot read CSV file!")
        return
    
    # Try to identify the correct column names
    name_col = None
    email_col = None
    
    # Common variations for name column
    name_variations = ['name', 'company', 'company name', 'business name', 'Name', 'Company']
    for var in name_variations:
        if var in columns:
            name_col = var
            break
    
    # Common variations for email column  
    email_variations = ['email', 'Email', 'email address', 'Email Address', 'e-mail', 'E-mail']
    for var in email_variations:
        if var in columns:
            email_col = var
            break
    
    print(f"\n🎯 COLUMN MAPPING:")
    print(f"  Name column: {name_col}")
    print(f"  Email column: {email_col}")
    
    if not name_col and not email_col:
        print("❌ Could not identify name or email columns!")
        print("Available columns:", columns)
        
        # Let user specify
        name_col = input(f"Enter the name column (from {columns}): ").strip()
        email_col = input(f"Enter the email column (from {columns}): ").strip()
    
    # Read and process the data
    try:
        df = pd.read_csv(input_csv)
        print(f"\n📊 Processing {len(df)} companies...")
        
        scraper = FixedCompanyScraper()
        results = []
        successful_scrapes = 0
        
        for i, row in df.iterrows():
            company_name = str(row.get(name_col, 'Unknown Company')).strip()
            email = str(row.get(email_col, '')).strip()
            
            # Skip if both are empty/invalid
            if (not company_name or company_name == 'Unknown Company' or company_name == 'nan') and not email:
                continue
                
            print(f"\n{i+1}/{len(df)}: {company_name}")
            print(f"  📧 {email}")
            
            # Try to scrape website
            about_info = ""
            website_url = ""
            
            if email and '@' in email:
                urls_to_try = scraper.extract_domain_from_email(email)
                
                for url in urls_to_try:
                    print(f"  🔍 Testing: {url}")
                    working_url = scraper.test_url(url)
                    
                    if working_url:
                        print(f"  ✅ Found: {working_url}")
                        website_url = working_url
                        
                        # Try to scrape
                        scrape_result = scraper.scrape_basic_info(working_url, company_name)
                        if scrape_result and scrape_result['found_info']:
                            about_info = scrape_result['about']
                            successful_scrapes += 1
                            print(f"  📄 Got info: {about_info[:80]}...")
                        break
            
            # Use fallback if no info found
            if not about_info:
                about_info = scraper.create_fallback_info(company_name, email)
                print(f"  ⚠️ Using fallback info")
            
            # Create result
            result = {
                'Name': company_name,
                'Email': email,
                'Website': website_url,
                'About': about_info
            }
            
            # Add any other columns from original
            for col in df.columns:
                if col not in result and col in [name_col, email_col]:
                    continue
                result[col] = row.get(col, '')
            
            results.append(result)
            
            # Respectful delay
            time.sleep(random.uniform(1.5, 3))
        
        # Save results
        if results:
            results_df = pd.DataFrame(results)
            results_df.to_csv(output_csv, index=False)
            
            print(f"\n🎉 SCRAPING COMPLETE!")
            print(f"📊 Processed: {len(results)} companies")
            print(f"✅ Found website info: {successful_scrapes}")
            print(f"💾 Saved to: {output_csv}")
            
            # Show sample
            if len(results) > 0:
                print(f"\n📄 SAMPLE RESULT:")
                sample = results[0]
                for key, value in sample.items():
                    print(f"  {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
        else:
            print("❌ No results to save!")
            
    except Exception as e:
        print(f"❌ Error processing: {e}")

if __name__ == "__main__":
    input_file = "houston_remodeling_contacts.csv"
    output_file = "houston_remodeling_contacts_with_info.csv"
    
    smart_scrape_companies(input_file, output_file)