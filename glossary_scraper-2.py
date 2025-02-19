# A different style of glossary scraping. In case of this book: , the glossary terms are in a seperate page named 
# "Key terms" and have a different kind of structure. They don't use the same dt-dt structure as the previous 
# glossary. This scraper will be used to scrape the glossary from such kind of pages.

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

# Function to scrape key terms from a given URL
def scrape_key_terms(url, output_file="./data/glossary2.csv"):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    key_terms_div = soup.find("div", class_="key-terms")

    if not key_terms_div:
        print(f"No key terms found at {url}")
        return

    key_terms_data = []
    
    # Find all <p> elements containing terms and definitions, and then also make sure to remove the <strong> 
    # elements 'properly' before extracting the definition
    for p in key_terms_div.find_all("p"):
        # Extract term correctly
        strong_tags = p.find_all("strong")
        term = " ".join([t.get_text(strip=True) for t in strong_tags])

        # Remove <strong> elements from the paragraph
        for strong in strong_tags:
            strong.extract()

        # Now extract the definition safely
        definition = p.get_text(strip=True)

        key_terms_data.append([clean_text(term), clean_text(definition), url])
    
    # Append cleaned data to CSV
    if key_terms_data:
        with open(output_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(key_terms_data)
        print(f"Scraped {len(key_terms_data)} key terms from {url}")
    else:
        print(f"No key terms found at {url}")

# Function to load URLs from a JSON file
# Note: here the links2.json file is created manually unlike links.json which was created using the scraper
def load_urls(json_file="./data/links2.json"):
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
with open("./data/glossary2.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Term", "Definition", "Source URL"])

# Scrape each URL from JSON
for url in urls:
    scrape_key_terms(url)
