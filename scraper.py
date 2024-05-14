import requests
from bs4 import BeautifulSoup
from extractor import extract_satellite_info

def scrape_satellite_data(website_url):
    response = requests.get(website_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    satellite_links = [a['href'] for a in soup.select('a[href^="/satellites?norad="]')]
    base_url = "https://www.satbeams.com"
    satellite_data_list = []

    for link in satellite_links:
        satellite_url = base_url + link
        satellite_response = requests.get(satellite_url)
        satellite_data = extract_satellite_info(satellite_response.content)
        satellite_data_list.append(satellite_data)
        print(f"Scraped data from {satellite_url}")

    return satellite_data_list
