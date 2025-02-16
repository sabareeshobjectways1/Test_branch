from scrapegraphai import ScrapeGraphAI
import json

# Initialize ScrapeGraphAI with your API key
api_key = "AIzaSyCRjKocESVskmlfPfwXwSh9vvEBxKoVzLI"
scraper = ScrapeGraphAI(api_key)

# Amazon deals URL
url = "https://www.amazon.in/deals/?_encoding=UTF8&ref_=in_cat_halo_mweb_bau_deals"

# Define the prompt for extraction
prompt = """
Extract all deals from this Amazon page. For each product, get:
1. Product name
2. Current price
3. Original price (if available)
4. Discount percentage
5. Rating (if available)
Please format the data in a clean, structured way.
"""

def scrape_amazon_deals():
    try:
        # Use ScrapeGraphAI to extract information
        response = scraper.scrape(
            url=url,
            prompt=prompt,
            enable_javascript=True,  # Enable JS for dynamic content
            wait_for_selector=".DealGridItem-module__dealItem_2JkjZ"  # Wait for deals to load
        )
        
        # Parse the response
        if response.success:
            # Save the extracted data to a JSON file
            with open('amazon_deals.json', 'w', encoding='utf-8') as f:
                json.dump(response.data, f, indent=2, ensure_ascii=False)
            
            print("Successfully scraped deals!")
            print("\nExtracted Deals:")
            print(json.dumps(response.data, indent=2))
            
            return response.data
        else:
            print(f"Error: {response.error}")
            return None
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def analyze_deals(deals_data):
    if not deals_data:
        return
        
    # Use ScrapeGraphAI's analysis capabilities
    analysis_prompt = """
    Analyze these Amazon deals and provide:
    1. Top 3 biggest discounts
    2. Price range summary
    3. Most common product categories
    4. Recommendations for best value deals
    """
    
    try:
        analysis = scraper.analyze(
            data=deals_data,
            prompt=analysis_prompt
        )
        
        print("\nDeals Analysis:")
        print(analysis.result)
        
    except Exception as e:
        print(f"Analysis error: {str(e)}")

if __name__ == "__main__":
    print("Starting Amazon deals scraping...")
    deals = scrape_amazon_deals()
    if deals:
        analyze_deals(deals)
