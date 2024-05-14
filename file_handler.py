import os
from utils import download_image

def create_parent_directory(parent_directory):
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

def save_satellite_data(parent_directory, satellite_name, satellite_data):
    satellite_dir = os.path.join(parent_directory, satellite_name)
    if not os.path.exists(satellite_dir):
        os.makedirs(satellite_dir)
    
    file_path = os.path.join(satellite_dir, f"{satellite_name}.txt")
    with open(file_path, 'w') as file:
        for key, value in satellite_data.items():
            if key != 'Images':  # Exclude images from the text file
                file.write(f'{key}: {value}\n')
    
    print(f"Created file: {file_path}")
    return satellite_dir

def save_satellite_images(image_info, satellite_dir):
    for img in image_info:
        title = img['title']
        img_url = img['url']
        sanitized_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in title)
        img_path = os.path.join(satellite_dir, f"{sanitized_title}.png")
        download_image(img_url, img_path)
