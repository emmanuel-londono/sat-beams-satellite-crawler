import os
from utils import download_image

def create_parent_directory(parent_directory):
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)
        print(f"Created parent directory: {parent_directory}")

def save_satellite_data(parent_directory, satellite_name, satellite_data):
    satellite_dir = os.path.join(parent_directory, satellite_name)
    if not os.path.exists(satellite_dir):
        os.makedirs(satellite_dir)
        print(f"Created satellite directory: {satellite_dir}")
    
    file_path = os.path.join(satellite_dir, f"{satellite_name}.txt")
    with open(file_path, 'w') as file:
        for key, value in satellite_data.items():
            if key != 'Image Data':  # Exclude image data from the text file
                file.write(f'{key}: {value}\n')
    
    print(f"Created file: {file_path}")
    return satellite_dir

def save_satellite_images(img_data_list, satellite_dir):
    for img_data in img_data_list:
        img_url = img_data['url']
        img_alt = img_data['alt']
        sanitized_alt = "".join(c if c.isalnum() or c in " ._-" else "_" for c in img_alt)
        img_path = os.path.join(satellite_dir, f"{sanitized_alt}.png")
        print(f"Downloading image from {img_url} to {img_path}")
        download_image(img_url, img_path)
