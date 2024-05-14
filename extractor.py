from bs4 import BeautifulSoup

def extract_text(soup, label):
    try:
        b_tag = soup.find('b', text=label)
        if b_tag:
            return b_tag.next_sibling.strip()
    except Exception as e:
        print(f"Error extracting text for label '{label}': {e}")
    return "N/A"

def extract_anchor_text(soup, label):
    try:
        b_tag = soup.find('b', text=label)
        if b_tag:
            return b_tag.find_next('a').text.strip()
    except Exception as e:
        print(f"Error extracting anchor text for label '{label}': {e}")
    return "N/A"

def extract_image_info(soup):
    image_info = []
    base_url = "https://www.satbeams.com"

    slider_div = soup.select_one('#sliderDiv')
    if slider_div:
        img_containers = slider_div.select('div > div > div > div:nth-child(3) > a')
        for container in img_containers:
            title_tag = container.select_one('h2')
            img_tag = container.find_previous('img')
            if title_tag and img_tag:
                title = title_tag.get_text(strip=True)
                img_url = base_url + img_tag['src']
                image_info.append({'title': title, 'url': img_url})
    
    return image_info

def extract_satellite_info(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    satellite_data = {}

    satellite_data['Satellite Name'] = extract_text(soup, "Satellite Name:")
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

    satellite_data['Images'] = extract_image_info(soup)
    
    print(f"Extracted data for satellite: {satellite_data.get('Satellite Name', 'Unknown')}")
    
    return satellite_data
