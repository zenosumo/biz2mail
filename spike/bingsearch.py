import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Bing API key from environment variables
bing_api_key = os.getenv('BING_API_KEY')

def bing_search(search_term, api_key):
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
    }
    params = {
        'q': search_term,
        'textDecorations': True,
        'textFormat': 'HTML',
        'count': 10
    }
    try:
        response = requests.get('https://api.bing.microsoft.com/v7.0/search', headers=headers, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"An HTTP error occurred: {err}")
        return {}

def main():
    search_term = "Google official site"
    results = bing_search(search_term, bing_api_key)
    
    if 'webPages' in results:
        print("Top 10 results:")
        for i, result in enumerate(results['webPages']['value']):
            print(f"{i + 1}. {result['name']}")
            print(f"   URL: {result['url']}")
            print()
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
