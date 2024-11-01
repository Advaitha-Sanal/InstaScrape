import os
import requests
import json
import logging

# Configure logging
logging.basicConfig(
    filename='image_downloader.log',  # Log to a file
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

with open('varanasi_response.json', 'r') as file:
    data = json.load(file)

# Create a directory to save images
os.makedirs("downloaded_images", exist_ok=True)

# getting image count 
image_count, err_count = 0, 0
itm_arr = data["data"]["items"]

for i in range(0, len(itm_arr)):
    item = itm_arr[i]
    if "carousel_media" in item:
        for media in item["carousel_media"]:
            img_url = media["image_versions"]["items"][0]["url"]
            image_count += 1
            try:
                img_data = requests.get(img_url).content
                img_name = os.path.join("downloaded_images", f"image_{image_count}.jpg")
                with open(img_name, 'wb') as img_file:
                    img_file.write(img_data)
                logging.info(f"Successfully downloaded image: {img_name}")
            except Exception as e:
                logging.error(f"Failed to download image from {img_url}: {e}")
                err_count += 1
    elif "image_versions" in item:
        img_url = item["image_versions"]["items"][0]["url"]
        image_count += 1
        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join("downloaded_images", f"image_{image_count}.jpg")
            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)
            logging.info(f"Successfully downloaded image: {img_name}")
        except Exception as e:
            logging.error(f"Failed to download image from {img_url}: {e}")
            err_count += 1
    else:
        logging.warning(f"No 'carousel_media' or 'image_versions' found in item[{i}]")
        err_count += 1