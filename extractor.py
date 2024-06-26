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

    img_tags = soup.find_all('div', class_='footprint_map_picture_container')
    base_url = "https://www.satbeams.com"
    satellite_data['Image Data'] = []

    for img_tag in img_tags:
        img = img_tag.find('img')
        if img and 'src' in img.attrs:
            img_url = base_url + img['src']
            img_alt = img.get('alt', 'No Alt Text')
            satellite_data['Image Data'].append({"url": img_url, "alt": img_alt})
            print(f"Found image: {img_url} with alt text: {img_alt}")

    print(f"Extracted data for satellite: {satellite_data.get('Satellite Name', 'Unknown')}")
    
    return satellite_data
