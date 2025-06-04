import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("API_KEY not found in environment variables")

# Initialize the FirecrawlApp with the API key
app = FirecrawlApp(api_key=api_key)

def scrape_website(url):
    """
    Scrape a website using Firecrawl
    Args:
        url (str): The URL to scrape
    Returns:
        dict: The scraping results in markdown and HTML formats
    """
    try:
        scrape_result = app.scrape_url(url, formats=['markdown', 'html'])
        return scrape_result
    except Exception as e:
        print(f"Error scraping website: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    target_url = "https://firecrawl.dev"
    result = scrape_website(target_url)
    if result:
        print("Scraping Results:")
        print(result)
