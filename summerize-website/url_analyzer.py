import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file. Please set it before running.")

def fetch_website_content(url):
    """Fetches website content and extracts links and metadata."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract title and headings
        title = soup.title.string if soup.title else "No Title"
        
        # Extract internal and external links/paths
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("/") or url in href:
                links.add(href)
                
        # Extract script and style assets to detect asset paths
        assets = set()
        for tag in soup.find_all(["script", "link", "img"], src=True):
            assets.add(tag.get("src"))
        for tag in soup.find_all("link", href=True):
            assets.add(tag.get("href"))

        return {
            "title": title,
            "links": list(links)[:30],  # Limit links sent to LLM
            "assets": list(assets)[:20]  # Limit assets sent to LLM
        }
    
    except Exception as e:
        print(f"Error fetching website {url}: {e}")
        return None

def analyze_directories_with_openrouter(website_url, site_data):
    """Sends extracted URL data to OpenRouter to predict and layout project directories."""
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an expert full-stack developer and web architect.
Analyze the following scraped metadata from the target website: {website_url}

Target Title: {site_data['title']}
Discovered Links: {site_data['links']}
Discovered Assets: {site_data['assets']}

Based on these endpoints, assets, standard web architecture, and URL structure:
1. Reconstruct the probable project directory and file structure (like a folder tree or sitemap).
2. Categorize standard routes (e.g., Pages, Assets, API endpoints, Admin routes).
3. Outline how the website's project appears to be organized (e.g., static HTML, React/Next.js routes, PHP server architecture).

Provide a clear, formatted tree structure in Markdown.
"""

    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": "You analyze web application structures and generate project directory layouts."},
            {"role": "user", "content": prompt}
        ]
    }

    print("\nSending data to OpenRouter LLM for analysis...\n")
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        
        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"API Error: {res_json}"

    except Exception as e:
        return f"Failed to call OpenRouter API: {e}"

if __name__ == "__main__":
    target_url = input("Enter website URL (e.g., https://example.com): ").strip()
    
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    print(f"\n[1/2] Fetching content from {target_url}...")
    scraped_data = fetch_website_content(target_url)

    if scraped_data:
        print(f"[2/2] Scraped {len(scraped_data['links'])} links and {len(scraped_data['assets'])} assets.")
        analysis = analyze_directories_with_openrouter(target_url, scraped_data)
        
        print("\n" + "="*50)
        print("PROJECT DIRECTORY & SITE MAP ANALYSIS")
        print("="*50 + "\n")
        print(analysis)