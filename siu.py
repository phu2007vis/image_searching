import re
import requests
import os
import hashlib
from utils import dowload_image
# File path containing the data
file_path = r"hi.php"
import pandas as pd
# Output directory to save images
output_dir = r"./static/img"
csv_path =  "map_url.csv"
csv_name_path = "map_name.csv"
map_dict = {

}
map_name = {
     
}
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Regex to match the 'hinh_anh' field with a URL
# pattern = r"'hinh_anh'\s*=>\s*'((https?://[^\s']+))'"
pattern = r"'ten_san_pham'\s*=>\s*'([^']+)',\s*\n.*?\s*'hinh_anh'\s*=>\s*'((https?://[^\s']+))'"

try:
    # Read the file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Extract all image links
    matches = re.findall(pattern, content)

    # Download and save each image
    for idx, match in enumerate(matches):
        # for data in match:  # Extract the URL
            try:
                # import pdb;pdb.set_trace()
                
                product_name ,image_url = match[:2]
                map_name[image_url] = product_name
                url_hash = hashlib.md5(image_url.encode()).hexdigest()  # Unique hash for the URL
                image_extension = "jpg"  # Default to .jpg if no extension
                image_name =  f"image_{idx + 1}_{url_hash[:8]}.{image_extension}"
                image_path = os.path.join(output_dir,image_name)

                dowload_image(image_url,image_path)
                map_dict[image_name] = image_url
              
            except requests.RequestException as e:
                print(f"Failed to download {image_url}: {e}")


except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error: {e}")

df = pd.DataFrame(list(map_dict.items()), columns=['img_name', 'url'])
df.to_csv(csv_path,index=None)



df2 = pd.DataFrame(list(map_name.items()), columns=['url', 'product_name'])
df2.to_csv(csv_name_path,index=None)

