import requests

def download_image(img_url, save_path):
    try:
        response = requests.get(img_url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
        print(f"Image downloaded and saved to {save_path}")
    except Exception as e:
        print(f"Error downloading image from {img_url}: {e}")
