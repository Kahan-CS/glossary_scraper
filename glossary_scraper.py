import requests
from bs4 import BeautifulSoup
import csv
import json

# Function to clean text by removing unnecessary surrounding quotes
def clean_text(text):
    text = text.strip()

    # Remove surrounding quotes *only* if the entire string is quoted
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        text = text[1:-1].strip()

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
            term_text = term.get_text(strip=True)
            definition_text = definition.get_text(strip=True)

            # Add raw extracted data first
            glossary_data.append([term_text, definition_text, url])

    if not glossary_data:
        print(f"No glossary terms found at {url}")
        return
    
    # # Print term, definition, and source for debugging
    # for term, definition, source in glossary_data:
    #     print(f"Term: {term}\nDefinition: {definition}\nSource: {source}\n")
    
    # Clean text after adding to the list
    cleaned_glossary_data = [[clean_text(term), clean_text(definition), source] for term, definition, source in glossary_data]

    # # Print cleaned term, definition, and source for debugging
    # for term, definition, source in cleaned_glossary_data:
    #     print(f"Cleaned Term: {term}\nCleaned Definition: {definition}\nSource: {source}\n")

    # Append cleaned data to CSV
    with open(output_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_glossary_data)

    print(f"Scraped {len(cleaned_glossary_data)} glossary terms from {url}")

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
