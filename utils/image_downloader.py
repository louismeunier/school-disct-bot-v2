import requests
import shutil

def download(url,name):
	"""
	This function was almost ENTIRELY "copied" from
	https://towardsdatascience.com/how-to-download-an-image-using-python-38a75cfa21c
	"""
	r=requests.get(url,stream=True)
	if r.status_code==200:
		r.raw.decode_content=True
		with open(f"utils/resources/images/schedules/{name}.png", "wb") as f:
			shutil.copyfileobj(r.raw,f)
		return True
	else: 
		return False