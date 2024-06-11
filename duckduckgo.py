import os
from duckduckgo_search import DDGS

def duckduckgo_search(search_term):
    try:
        results = DDGS().text(search_term, max_results=5)
        # Extract URLs from the results
        urls = [result['href'] for result in results if 'href' in result]
        return urls
    except Exception as err:
        print(f"An error occurred: {err}")
        return []

def main():
    search_term = "SIS TER 2100890967"
    urls = duckduckgo_search(search_term)
    
    if urls:
        print("Top results:")
        for i, url in enumerate(urls):
            print(f"{i + 1}. {url}")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
