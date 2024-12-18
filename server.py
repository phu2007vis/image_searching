import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from utils import get_image
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel

# Define the input model for the request
class ImageURLRequest(BaseModel):
    url: str

app = FastAPI()

# Initialize feature extractor
fe = FeatureExtractor()
features = []
img_paths = []

# Load CSV map file
csv_map_file = "map_url.csv"
url_map = pd.read_csv(csv_map_file)

def get_image_url(image_name):
    return url_map[url_map.img_name == image_name].url.values[0]

# Precompute features for existing images
for feature_path in tqdm(Path("./static/img").glob("*.jpg")):
    img_path = feature_path
    img_paths.append(img_path)
    img = Image.open(img_path)
    query = fe.extract(img)
    features.append(query)
features = np.array(features)


@app.post("/predict")
async def index(request: ImageURLRequest):

    # Validate URL and fetch image (dummy logic, adjust as needed)
    try:
        img = get_image(request.url)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image URL not found")



    query = fe.extract(img)

    # Calculate distances and retrieve top 30 results
    dists = np.linalg.norm(features - query, axis=1)
    ids = np.argsort(dists)[:5]
    scores = [(float(dists[id]), str(img_paths[id])) for id in ids]
    
    # Prepare URLs for the top images
    imgs_url = [get_image_url(str(Path(image).name)) for _, image in scores]
    
    return JSONResponse(content={ "image_urls": imgs_url})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
