import requests

def download_image(url, path):
    try:
        print(f"Attempting to download image from {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")

        content_type = response.headers.get('Content-Type')
        if 'image' not in content_type:
            print(f"URL {url} does not contain image data, content type is {content_type}")
            return

        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded image: {path}")
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
