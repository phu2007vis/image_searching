import numpy as np  # Thư viện xử lý mảng số học
from PIL import Image  # Thư viện xử lý hình ảnh
from feature_extractor import FeatureExtractor  # Module để trích xuất đặc trưng từ hình ảnh
from pathlib import Path  # Module làm việc với đường dẫn tệp
import pandas as pd  # Thư viện xử lý dữ liệu dạng bảng
from tqdm import tqdm  # Thư viện hiển thị tiến trình
from utils import get_image  # Hàm tiện ích để tải hình ảnh
from fastapi import FastAPI, HTTPException  # FastAPI framework để xây dựng API
from fastapi.responses import JSONResponse  # Để trả về dữ liệu JSON
from pydantic import BaseModel  # Module để tạo các mô hình dữ liệu đầu vào

# Định nghĩa lớp dữ liệu đầu vào với thuộc tính 'url'
class ImageURLRequest(BaseModel):
    url: str

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Khởi tạo trình trích xuất đặc trưng
fe = FeatureExtractor()
features = []  # Danh sách lưu trữ các đặc trưng hình ảnh
img_paths = []  # Danh sách lưu trữ đường dẫn hình ảnh

# Đọc tệp CSV ánh xạ tên hình ảnh với URL
csv_map_file = "map_url.csv"
url_map = pd.read_csv(csv_map_file)  # Tải dữ liệu từ map_url.csv
csv_map_name_file = "map_name.csv" 
url_map_name = pd.read_csv(csv_map_name_file)  # Tải dữ liệu từ map_name.csv

# Hàm lấy URL của hình ảnh từ tên hình ảnh
def get_image_url(image_name):
    return url_map[url_map.img_name == image_name].url.values[0]

# Hàm lấy tên sản phẩm từ URL
def get_product_name(url):
    return url_map_name[url_map_name.url ==url].product_name.values[0]

# Tiền xử lý: Trích xuất đặc trưng từ các hình ảnh có sẵn
for feature_path in tqdm(Path("./static/img").glob("*.jpg")):
    img_path = feature_path  # Lưu đường dẫn hình ảnh
    img_paths.append(img_path)  # Thêm vào danh sách đường dẫn
    img = Image.open(img_path)  # Mở hình ảnh
    query = fe.extract(img)  # Trích xuất đặc trưng
    features.append(query)  # Lưu đặc trưng vào danh sách
features = np.array(features)  # Chuyển danh sách đặc trưng thành mảng numpy

# Định nghĩa endpoint POST để dự đoán
@app.post("/predict")
async def index(request: ImageURLRequest):
    try:
        img = get_image(request.url)  # Lấy hình ảnh từ URL đầu vào
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image URL not found")  # Trả về lỗi nếu không tải được hình ảnh

    query = fe.extract(img)  # Trích xuất đặc trưng từ hình ảnh đầu vào

    dists = np.linalg.norm(features - query, axis=1)  # Tính khoảng cách giữa đặc trưng đầu vào và tất cả các đặc trưng đã lưu
    ids = np.argsort(dists)[:5]  # Lấy 5 hình ảnh giống nhất 
    scores = [(float(dists[id]), str(img_paths[id])) for id in ids]  # Lưu điểm số và đường dẫn hình ảnh tương ứng

    imgs_url = [get_image_url(str(Path(image).name)) for _, image in scores]  # Lấy URL của các hình ảnh tương ứng
    product_name  = [get_product_name(url) for url in imgs_url]  # Lấy tên sản phẩm tương ứng với các URL

    return JSONResponse(content={ "image_urls": imgs_url,"product_name":product_name})  # Trả về kết quả dưới dạng JSON

# Điểm bắt đầu chạy ứng dụng
if __name__ == "__main__":
    import uvicorn  # Thư viện chạy ứng dụng FastAPI
    uvicorn.run(app, host="0.0.0.0", port=7999)  # Khởi chạy ứng dụng trên cổng 79997999