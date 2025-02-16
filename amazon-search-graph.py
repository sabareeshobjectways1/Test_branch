import os
from dotenv import load_dotenv
from scrapegraphai.graphs import SearchGraph
from scrapegraphai.utils import convert_to_csv, convert_to_json, prettify_exec_info

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
4. Categorize products by type
5. Highlight any special offers or lightning deals
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
        
        # Get execution info
        graph_exec_info = search_graph.get_execution_info()
        print("\nExecution Information:")
        print(prettify_exec_info(graph_exec_info))
        
        # Save results
        print("\nSaving results...")
        convert_to_csv(result, "amazon_deals")
        convert_to_json(result, "amazon_deals")
        
        print("\nResults have been saved to 'amazon_deals.csv' and 'amazon_deals.json'")
        
        # Print results
        print("\nSearch Results:")
        print(result)
        
        return result
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "__main__":
    scrape_amazon_deals()
