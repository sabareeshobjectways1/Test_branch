import os
from scrapegraphai.graphs import SearchGraph

# Configuration setup
gemini_key = "AIzaSyCRjKocESVskmlfPfwXwSh9vvEBxKoVzLI"

graph_config = {
    "llm": {
        "api_key": gemini_key,
        "model": "google_genai/gemini-pro",
    },
}

# Create prompt for Amazon deals
amazon_prompt = """
Search and analyze deals from Amazon India (https://www.amazon.in/deals/) with the following requirements:
1. List all available deals
2. For each product include:
   - Product name
   - Current price
   - Original price
   - Discount percentage
   - Rating (if available)
3. Identify the best deals based on discount percentage
"""

def scrape_amazon_deals():
    try:
        # Create SearchGraph instance
        search_graph = SearchGraph(
            prompt=amazon_prompt,
            config=graph_config
        )

        # Run the search
        print("Searching for Amazon deals...")
        result = search_graph.run()
        
        # Print results
        print("\nSearch Results:")
        print(result)
        
        return result
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    scrape_amazon_deals()
