import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import json
from datetime import datetime

def setup_gemini():
    """Initialize Gemini API"""
    api_key = "AIzaSyCRjKocESVskmlfPfwXwSh9vvEBxKoVzLI"
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_amazon_data(url):
    """Fetch data from Amazon with proper headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def parse_deals(html_content):
    """Parse Amazon deals from HTML content"""
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    deals = []
    
    # Look for deal containers
    deal_items = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for item in deal_items:
        try:
            # Extract product details
            title = item.find('h2', {'class': 'a-size-mini'})
            price = item.find('span', {'class': 'a-price-whole'})
            original_price = item.find('span', {'class': 'a-text-price'})
            rating = item.find('span', {'class': 'a-icon-alt'})
            
            deal = {
                'title': title.text.strip() if title else 'N/A',
                'current_price': price.text.strip() if price else 'N/A',
                'original_price': original_price.text.strip() if original_price else 'N/A',
                'rating': rating.text.strip() if rating else 'N/A',
                'url': f"https://www.amazon.in{item.find('a')['href']}" if item.find('a') else 'N/A'
            }
            deals.append(deal)
        except Exception as e:
            print(f"Error parsing deal: {e}")
            continue
    
    return deals

def analyze_with_gemini(deals, model):
    """Analyze deals using Gemini AI"""
    if not deals:
        return "No deals to analyze"
    
    analysis_prompt = f"""
    Analyze these Amazon deals and provide:
    1. Best value deals
    2. Highest discounts
    3. Price range summary
    4. Popular categories
    
    Deals data:
    {json.dumps(deals, indent=2)}
    """
    
    try:
        response = model.generate_content(analysis_prompt)
        return response.text
    except Exception as e:
        return f"Analysis error: {e}"

def save_results(deals, analysis):
    """Save results to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"amazon_deals_{timestamp}.json"
    
    output = {
        'timestamp': timestamp,
        'deals': deals,
        'analysis': analysis
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    return filename

def main():
    # Setup
    print("Initializing...")
    model = setup_gemini()
    
    # Amazon deals URL
    url = "https://www.amazon.in/deals/?_encoding=UTF8&ref_=in_cat_halo_mweb_bau_deals"
    
    # Fetch and parse data
    print("Fetching deals...")
    html_content = get_amazon_data(url)
    if not html_content:
        print("Failed to fetch data from Amazon")
        return
    
    # Parse deals
    print("Parsing deals...")
    deals = parse_deals(html_content)
    if not deals:
        print("No deals found")
        return
    
    # Analyze deals
    print("Analyzing deals...")
    analysis = analyze_with_gemini(deals, model)
    
    # Save results
    filename = save_results(deals, analysis)
    
    # Print summary
    print(f"\nFound {len(deals)} deals")
    print(f"Results saved to {filename}")
    print("\nAnalysis:")
    print(analysis)

if __name__ == "__main__":
    main()
