import os
import json
from datetime import datetime
from dotenv import load_dotenv
from firecrawl import FirecrawlApp, JsonConfig
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY not found in environment variables")

# Initialize FirecrawlApp
app = FirecrawlApp(api_key=api_key)

class ExtractSchema(BaseModel):
    """Simple schema for company information extraction"""
    company_mission: str = Field(description="The company's mission statement")
    supports_sso: bool = Field(description="Whether the company supports Single Sign-On")
    is_open_source: bool = Field(description="Whether the company's product is open source")
    is_in_yc: bool = Field(description="Whether the company is part of Y Combinator")

# Configure JSON extraction
json_config = JsonConfig(
    extractionSchema=ExtractSchema.model_json_schema(),
    mode="llm-extraction",
    pageOptions={"onlyMainContent": True}
)

# Single company to test with
company = {
    "name": "vercel",
    "url": "https://www.vercel.com"
}

def save_data(filename, data):
    """Save data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return filename

try:
    print(f"\nProcessing {company['name'].upper()}...")
    print("=" * 50)
    
    # Get the response
    response = app.scrape_url(
        company['url'],
        formats=["json"],
        json_options=json_config
    )
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Prepare the data to save
    all_data = {
        "company": company['name'],
        "timestamp": timestamp,
        "url": company['url'],
        "success": response.success if hasattr(response, 'success') else None,
        "metadata": response.metadata if hasattr(response, 'metadata') else None
    }
    
    # Try to get the extracted data
    if response.success and hasattr(response, 'extract') and response.extract:
        try:
            extracted = response.extract
            if hasattr(extracted, 'model_dump'):
                all_data["extracted_data"] = extracted.model_dump()
            elif hasattr(extracted, 'dict'):
                all_data["extracted_data"] = extracted.dict()
            else:
                all_data["extracted_data"] = extracted
        except Exception as e:
            all_data["extraction_error"] = str(e)
    
    # Save all data to a single file
    filename = f"{company['name']}_data_{timestamp}.json"
    save_data(filename, all_data)
    print(f"\nAll data saved to {filename}")
    
    # Print the data that was saved
    print("\nSaved Data Summary:")
    print("-" * 30)
    print(f"Company: {all_data['company']}")
    print(f"URL: {all_data['url']}")
    print(f"Success: {all_data['success']}")
    
    if all_data.get('metadata'):
        print("\nMetadata available:")
        for key, value in all_data['metadata'].items():
            print(f"{key}: {value}")
    
    if all_data.get('extracted_data'):
        print("\nExtracted Data:")
        for key, value in all_data['extracted_data'].items():
            print(f"{key}: {value}")
    
    if all_data.get('extraction_error'):
        print(f"\nExtraction Error: {all_data['extraction_error']}")
            
except Exception as e:
    print(f"\nError during scraping: {str(e)}")
    error_data = {
        "company": company['name'],
        "timestamp": timestamp,
        "url": company['url'],
        "error": str(e)
    }
    error_file = save_data(f"{company['name']}_error_{timestamp}.json", error_data)
    print(f"Error details saved to {error_file}")

print("\nProcessing completed!")