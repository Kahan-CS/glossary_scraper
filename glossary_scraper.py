import requests
from bs4 import BeautifulSoup
import csv
import re

def clean_text(text):
    """Removes unnecessary surrounding quotes but keeps inner quotes intact."""
    text = text.strip()
    text = re.sub(r'^["\']|["\']$', '', text)  # Remove leading/trailing single/double quotes
    return text

def scrape_glossary(url, output_file="glossary.csv"):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    dl_elements = soup.find_all("dl", class_="definition")
    
    glossary_data = []

    for dl in dl_elements:
        terms = dl.find_all("dt")
        definitions = dl.find_all("dd")

        for term, definition in zip(terms, definitions):
            term_text = clean_text(term.get_text(strip=True))
            definition_text = clean_text(definition.get_text(strip=True))
            glossary_data.append([term_text, definition_text, url])

    if not glossary_data:
        print(f"No glossary terms found at {url}")
        return

    # Write to CSV
    with open(output_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(glossary_data)

    print(f"Scraped {len(glossary_data)} glossary terms from {url}")

# Example usage
urls = [
    "https://open.oregonstate.education/aandp/chapter/1-1-how-structure-determines-function/",
    # Add more URLs here
]

# Create a CSV with headers
with open("glossary.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Term", "Definition", "Source URL"])

# Scrape each URL
for url in urls:
    scrape_glossary(url)
