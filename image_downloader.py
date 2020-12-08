import requests
import shutil

def download(url,name):

	r=requests.get(url,stream=True)
	if r.status_code==200:
		r.raw.decode_content=True
		with open("images/schedules/"+name+".png", "wb") as f:
			shutil.copyfileobj(r.raw,f)