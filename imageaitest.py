from g4f.client import Client
from PIL import Image
from g4f.cookies import get_cookies
import requests # request img from web
import shutil
import sys

cookies = get_cookies(".bing.com")
client = Client(cookies=cookies)
print(cookies)
prompt = input("Your prompt: ")
err_count = 0
def create_image(prompt, err_count):
	try:
		response = client.images.generate(model="dall-e-3",prompt=prompt)
		return response
	except Exception as e:
		err_count += 1
		print("Error")
		if err_count >= 10:
			raise e
		create_image(prompt, err_count)
	
	
try:
    response = create_image(prompt, err_count)
except Exception as e:
	print(f"Count of errors: 10+, Fatal Error: {e}(check your prompt)")
	sys.exit()
print(response)
print(client.images.models)
print(response)
image_url = response.data
counter = 0
for i in image_url:
	counter += 1
	res = requests.get(i.url, stream = True)
	if res.status_code == 200:
		with open(f"image{counter}.jpg",'wb') as f:
			shutil.copyfileobj(res.raw, f)
			print(f"Image{counter} done!")
		