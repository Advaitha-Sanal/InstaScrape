import http.client
import json
import requests
import os

# Set up the connection
conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")

# Define headers with your API key
headers = {
    'x-rapidapi-key': "42b839f4fcmsh8ad98ebd602901ap187e27jsn9a7e49777fa0",
    'x-rapidapi-host': "instagram-scraper-api3.p.rapidapi.com"
}

conn.request("GET", "/hashtag_media?hashtag=kashi&feed_type=recent", headers=headers)
res = conn.getresponse()
data = res.read()

# Decode the data to string
response_data = data.decode("utf-8")

# Parse the response data as JSON and save it
try:
    json_data = json.loads(response_data)
    with open("varanasi_response.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    print("Response has been written to varanasi_response.json")
except json.JSONDecodeError as e:
    print("Failed to decode JSON:", e)
    json_data = None

# Ensure valid JSON data exists
if json_data:
    # Directory for images
    image_dir = "varanasi_images"
    os.makedirs(image_dir, exist_ok=True)

    # Extract image URLs and download them
    for idx, post in enumerate(json_data.get("posts", [])):
        # Print the post to inspect keys
        print("Post data:", post)  # Debugging line to see the structure of each post

        # Find and use the correct key for the image URL
        image_url = post.get("image_url")  # Update this key based on JSON inspection
        print(f"Image URL found: {image_url}")  # Print the image URL being processed

        if image_url:
            try:
                # Download the image
                img_data = requests.get(image_url).content
                # Save the image with a unique filename
                img_filename = os.path.join(image_dir, f"image_{idx + 1}.jpg")
                with open(img_filename, "wb") as img_file:
                    img_file.write(img_data)
                print(f"Downloaded {img_filename}")
            except Exception as e:
                print(f"Failed to download {image_url}: {e}")
        else:
            print("No image URL found for this post.")
