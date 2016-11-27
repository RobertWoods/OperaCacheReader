import time
import shelve
import sys
import re

from selenium import webdriver

drv = '' #get global reference for driver later

def get_links():
	op = "C:\\Users\\rober_000\\AppData\\Roaming\\Opera Software\\Opera Stable" #Path to profile
	options = webdriver.ChromeOptions()
	options.add_argument('user-data-dir=' + op)
	global drv
	drv = webdriver.Opera(opera_options=options)
	#drv.set_window_position(-2000, 0) #'Minimize' after opening
	#drv = webdriver.Opera()
	#drv.get("http://facebook.com") #Populate cache with default selenium profile
	drv.get("opera:view-http-cache")
	links = drv.find_elements_by_tag_name("a")
	images = []
	for link in links:
		link = str(link.get_attribute("href"))
		link = link.replace("chrome://", "opera:")
		#Only image formats specified to reduce the number of files returned
		#facebook specified as example during testing
		if (".png" in link or ".jpg" in link or ".gif" in link or "safe_image" in link or "jpeg") and ("facebook" in link or "fbcdn" in link):
			images.append(link)
	return images

def get_characters_from_text(text):
	try:
		image_text = text[text.index("00000000:", text.index("00000000:")+1)-1:]
	except ValueError:
		return None
	characters = []
	hex_digits = re.findall("(?=( [0-9|a-f][0-9|a-f] ))", image_text)
	for i in range(0, len(hex_digits)):
		characters.append(chr(int('0x'+hex_digits[i].strip(), 16)))
	return characters
	
def write_text_to_file(text, name, ext):
	with open("cache/"+name+'.'+ext, 'wb') as f:
		for character in text:
			f.write(character)
	
	
	
d = shelve.open("cache_data.txt")
body_texts = []
if len(sys.argv) > 1:
	if sys.argv[1] == '-u':
		d["texts"] = get_links()

try:
	images = d["texts"]
except KeyError:
	images = get_links()
	d["texts"] = images
	
for link in images:
#check if we already have data for it, otherwise collect data on it
	try:
		data = d[link]
	except KeyError:
		print link
		drv.get(link)
		d[link] = (drv.find_element_by_tag_name("body").text)
		time.sleep(.5)
		
link_keys = d.keys()
link_keys.remove('texts')
a = 0
for link in link_keys:
	characters = get_characters_from_text(d[link])
	if characters is not None:
		extension = re.search("image/((png)|(jpg)|(jpeg)|(gif))", d[link])
		write_text_to_file(characters, str(a), extension.group(1))
		a = a+1
		
d.close()
	