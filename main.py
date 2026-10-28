import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def generate_brochure_and_summary(website_text, links):
  """Uses OpenRouter to summarize the site and generate a professional brochure."""
  prompt = f"""
Analyze the following website content and perform two tasks:
1. Provide a concise executive summary of the company/website.
2. Create a professional, compelling marketing brochure layout (Headline, About Us, Core Services/Products, Value Proposition, and Call to Action).

Website Content:
{website_text}

Available Key Links:
{links[:15]}
"""

  completion = client.chat.completions.create(
      model="openrouter/auto",  # Automatically routes to an available active model
      messages=[{"role": "user", "content": prompt}],
  )

  return completion.choices[0].message.content

# Initialize the OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)


def scrape_website(url):
  """Fetches webpage text and extracts all internal/external links."""
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      )
  }
  response = requests.get(url, headers=headers, timeout=10)
  response.raise_for_status()

  soup = BeautifulSoup(response.text, "html.parser")

  # Remove script and style elements
  for script in soup(["script", "style"]):
    script.extract()

  # Extract visible text
  text = soup.get_text(separator="\n", strip=True)

  # Extract relevant links
  links = []
  for a in soup.find_all("a", href=True):
    href = a["href"]
    text_label = a.get_text(strip=True)
    if href.startswith("http") and text_label:
      links.append({"text": text_label, "url": href})

  return text[:15000], links  # Limit text length to fit context windows


def generate_brochure_and_summary(website_text, links):
  """Uses OpenRouter to summarize the site and generate a professional brochure."""
  prompt = f"""
Analyze the following website content and perform two tasks:
1. Provide a concise executive summary of the company/website.
2. Create a professional, compelling marketing brochure layout (Headline, About Us, Core Services/Products, Value Proposition, and Call to Action).

Website Content:
{website_text}

Available Key Links:
{links[:15]}
"""

  completion = client.chat.completions.create(
      model="openai/gpt-4o-mini",  # Or any other model available on OpenRouter
      messages=[{"role": "user", "content": prompt}],
  )

  return completion.choices[0].message.content


if __name__ == "__main__":
  target_url = input("Enter website URL (e.g., https://example.com): ")

  print("\n[1/3] Scraping website content and links...")
  try:
    page_text, extracted_links = scrape_website(target_url)

    print("[2/3] Processing with OpenRouter API...")
    output = generate_brochure_and_summary(page_text, extracted_links)

    print("\n[3/3] Generated Output:\n")
    print("=" * 60)
    print(output)
    print("=" * 60)

    print("\nRelevant Links Found:")
    for l in extracted_links[:10]:
      print(f"- {l['text']}: {l['url']}")

  except Exception as e:
    print(f"Error: {e}")
