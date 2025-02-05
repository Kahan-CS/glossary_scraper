import requests
from bs4 import BeautifulSoup
import json
import time

def get_chapter_links(start_url, stop_title="Creative Commons License", output_file="../data/extracted_links.json"):
    """
    Extracts all chapter links starting from `start_url`, following the 'Next' button until `stop_title` is found.
    Saves the collected links in a JSON file.
    """
    links = []
    current_url = start_url

    while current_url:
        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Failed to fetch {current_url}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the current chapter title
        current_title = soup.title.get_text(strip=True) if soup.title else ""

        # Stop condition: Reached the last page
        if stop_title.lower() in current_title.lower():
            print(f"Reached stop page: {current_title}")
            break

        # Store the current chapter link
        links.append(current_url)
        print(f"Added: {current_url}")

        # Find the "Next Chapter" button
        next_button = soup.find("a", title=lambda x: x and x.lower().startswith("next"))
        if next_button and "href" in next_button.attrs:
            current_url = next_button["href"]
            time.sleep(1)  # Small delay to avoid overwhelming the server
        else:
            print("No 'Next' button found. Stopping.")
            break

    # Save links to JSON
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump({"urls": links}, file, indent=4)

    print(f"Saved {len(links)} chapter links to {output_file}")

# usage: Start from Chapter 1.1
start_url = "https://open.oregonstate.education/aandp/chapter/1-1-how-structure-determines-function/"
get_chapter_links(start_url)
