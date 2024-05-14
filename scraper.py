from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from extractor import extract_satellite_info

def scrape_satellite_data(website):
    driver = webdriver.Chrome()
    driver.get(website)
    driver.implicitly_wait(5)
    
    t_body_xpath = '//*[@id="sat_grid"]/tbody/tr[@class="class_tr"]'
    tr_body_elements = driver.find_elements(By.XPATH, t_body_xpath)
    
    hrefs = []
    unique_hrefs = set()

    for tr in tr_body_elements:
        try:
            a_tag = WebDriverWait(tr, 10).until(
                EC.presence_of_element_located((By.XPATH, './/a[@class="link" and contains(@href, "/satellites?norad=")]'))
            )
            href_value = a_tag.get_attribute('href')
            hrefs.append(href_value)
            unique_hrefs.add(href_value)
        except Exception as e:
            print(f"Error finding a tag in tr: {e}")

    print(f"Number of unique hrefs: {len(unique_hrefs)}")
    
    satellite_data_list = []

    for href in unique_hrefs:
        try:
            driver.get(href)
            time.sleep(5)
            data = extract_satellite_info(driver.page_source)
            if data:
                satellite_data_list.append(data)
            driver.back()
            time.sleep(5)
        except Exception as e:
            print(f"Error visiting href {href}: {e}")
    
    driver.quit()
    return satellite_data_list
