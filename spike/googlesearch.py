import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
load_dotenv()

# Your API key and search engine ID
api_key = os.getenv('GOOGLE_API_KEY')
cse_id = os.getenv('CSE_ID')


def google_search(search_term, api_key, cse_id):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id).execute()
        print("Full API Response:")
        print(res)  # Print the full response for debugging
        return res.get('items', [])
    except HttpError as err:
        print(f"An HTTP error occurred: {err}")
        return []

def main():
    # Test with a known term
    search_term = "Google official site"
    results = google_search(search_term, api_key, cse_id)
    
    if results:
        print("Top 10 results:")
        for i, result in enumerate(results[:10]):
            print(f"{i + 1}. {result['title']}")
            print(f"   URL: {result['link']}")
            print()
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
