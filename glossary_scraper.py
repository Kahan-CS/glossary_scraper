import requests
from bs4 import BeautifulSoup
import csv
import re
import json

# Function to clean text by removing unnecessary surrounding quotes
def clean_text(text):
    text = text.strip()
    text = re.sub(r'^["\']|["\']$', '', text)  # Remove leading/trailing single/double quotes
    return text

# Function to scrape glossary terms and definitions from a given URL
def scrape_glossary(url, output_file="./data/glossary.csv"):
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

    # Append data to CSV
    with open(output_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(glossary_data)

    print(f"Scraped {len(glossary_data)} glossary terms from {url}")

# Function to load URLs from a JSON file
def load_urls(json_file="./data/links.json"):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("urls", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON file: {e}")
        return []

# Load URLs from JSON
urls = load_urls()

# Create a CSV with headers
with open("./data/glossary.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Term", "Definition", "Source URL"])

# Scrape each URL from JSON
for url in urls:
    scrape_glossary(url)
