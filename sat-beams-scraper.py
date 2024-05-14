from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from bs4 import BeautifulSoup

website = "https://www.satbeams.com/satellites?status=active"
t_body_xpath = '//*[@id="sat_grid"]/tbody/tr[@class="class_tr"]'

def extract_text(soup, label):
    """Extract text following the given label."""
    try:
        b_tag = soup.find('b', text=label)
        if b_tag:
            return b_tag.next_sibling.strip()
    except Exception as e:
        print(f"Error extracting text for label '{label}': {e}")
    return "N/A"

def extract_anchor_text(soup, label):
    """Extract text of the anchor following the given label."""
    try:
        b_tag = soup.find('b', text=label)
        if b_tag:
            return b_tag.find_next('a').text.strip()
    except Exception as e:
        print(f"Error extracting anchor text for label '{label}': {e}")
    return "N/A"

try:
    driver = webdriver.Chrome()
    driver.get(website)
    driver.implicitly_wait(5)
    
    tr_body_elements = driver.find_elements(By.XPATH, t_body_xpath)
    
    # List to store all URLs
    hrefs = []
    # Set to store unique URLs
    unique_hrefs = set()

    # Iterate over all tbody/tr elements
    for tr in tr_body_elements:
        try:
            # Check for tag presence
            a_tag = WebDriverWait(tr, 10).until(
                EC.presence_of_element_located((By.XPATH, './/a[@class="link" and contains(@href, "/satellites?norad=")]'))
            )
            href_value = a_tag.get_attribute('href')
            hrefs.append(href_value)
            unique_hrefs.add(href_value)
        except Exception as e:
            print(f"Error finding a tag in tr: {e}")

    print(f"Number of unique hrefs: {len(unique_hrefs)}")
    
    # Visit each href
    for href in unique_hrefs:
        try:
            # Navigate to the href
            driver.get(href)
            # Wait for the new page to load completely
            time.sleep(5)
            
            # Extract data from the new page
            page_title = driver.title
            print(f"Visited {href}, Page title: {page_title}")
            
            individual_sat_details = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="sat_grid1"]/tbody/tr[2]'))
            )

            # Extract the text from the element
            data_text = individual_sat_details.get_attribute('innerHTML')

            # Parse the extracted text
            soup = BeautifulSoup(data_text, 'html.parser')

            satellite_data = {}

            # Extract relevant data using the extract_text and extract_anchor_text functions
            satellite_data['Satellite Name'] = extract_text(soup, "Satellite Name:")
            satellite_name = satellite_data['Satellite Name']
            if not satellite_name or satellite_name == "N/A":
                print(f"Invalid satellite name for {href}, skipping...")
                continue

            satellite_data['Status'] = extract_text(soup, "Status:")
            satellite_data['Position'] = extract_text(soup, "Position:")
            satellite_data['NORAD'] = extract_anchor_text(soup, "NORAD:")
            satellite_data['Cospar number'] = extract_anchor_text(soup, "Cospar number:")
            satellite_data['Operator'] = extract_anchor_text(soup, "Operator:")
            satellite_data['Launch date'] = extract_text(soup, "Launch date:")
            satellite_data['Launch site'] = extract_anchor_text(soup, "Launch site:")
            satellite_data['Launch vehicle'] = extract_anchor_text(soup, "Launch vehicle:")
            satellite_data['Launch mass (kg)'] = extract_text(soup, "Launch mass (kg):")
            satellite_data['Dry mass (kg)'] = extract_text(soup, "Dry mass (kg):")
            satellite_data['Manufacturer'] = extract_anchor_text(soup, "Manufacturer:")
            satellite_data['Model (bus)'] = extract_anchor_text(soup, "Model (bus):")
            satellite_data['Orbit'] = extract_text(soup, "Orbit:")
            satellite_data['Expected lifetime'] = extract_text(soup, "Expected lifetime:")

            # Sanitize Satellite Name
            sanitized_name = "".join(c if c.isalnum() or c in " ._-" else "_" for c in satellite_name)
            if not sanitized_name:
                print(f"Sanitized satellite name is empty for {href}, skipping...")
                continue
            
            # Ensure the output directory exists
            if not os.path.exists(sanitized_name):
                os.makedirs(sanitized_name)
                
            file_path = os.path.join(sanitized_name, f"{sanitized_name}.txt")
            with open(file_path, 'w') as file:
                for key, value in satellite_data.items():
                    file.write(f'{key}: {value}\n')
            
            print(f"Created file: {file_path}")

            # Go back to the initial page
            driver.back()
            # Optional: wait for the initial page to load completely
            time.sleep(5)
            
        except Exception as e:
            print(f"Error visiting href {href}: {e}")    
finally:
    driver.quit()
