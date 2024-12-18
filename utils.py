import requests
from PIL import Image

def dowload_image(image_url,image_path):
	response = requests.get(image_url, stream=True)
	response.raise_for_status()  # Raise an error for bad responses

	# Save the image
	with open(image_path, "wb") as image_file:
		for chunk in response.iter_content(1024):  # Download in chunks
			image_file.write(chunk)
def get_image(image_url):
	response = requests.get(image_url, stream=True)
	response.raise_for_status()  # Raise an error for bad responses
	image_path = "tmp.jpg"
	# Save the image
	with open(image_path, "wb") as image_file:
		for chunk in response.iter_content(1024):  # Download in chunks
			image_file.write(chunk)

	pil_image = Image.open(image_path)
	return pil_image