from scraper import scrape_satellite_data
from file_handler import create_parent_directory, save_satellite_data, save_satellite_images

def main():
    website = "https://www.satbeams.com/satellites?status=active"
    parent_directory = "Satellites_Data"

    # Ensure the parent directory exists
    create_parent_directory(parent_directory)
    
    # Scrape satellite data
    satellite_data_list = scrape_satellite_data(website)
    
    # Save satellite data
    for satellite_data in satellite_data_list:
        satellite_name = satellite_data.get('Satellite Name', 'Unknown_Satellite')
        sanitized_name = "".join(c if c.isalnum() or c in " ._-" else "_" for c in satellite_name)
        satellite_dir = save_satellite_data(parent_directory, sanitized_name, satellite_data)
        
        # Save satellite images if available
        img_urls = satellite_data.get('Image URLs', [])
        if img_urls:
            save_satellite_images(img_urls, satellite_dir, sanitized_name)
    
if __name__ == "__main__":
    main()
