import requests
from PIL import Image, ImageDraw
import numpy as np
import cv2
import penrobo

def hare():
	global img
	print("hare no ugoki")
	# kawari ni e wo kaku
	#im = Image.new('RGB', (400, 400), (255, 255, 255))
	#draw = ImageDraw.Draw(im)

	#draw.ellipse((100, 100, 300, 300), fill=(255, 255, 255), outline=(0, 0, 0))
	pr.circle(img, 200, 200, 100, 0, 360)
	#draw.line((200, 0, 200, 60), fill=(0, 0, 0), width=1)
	pr.line(img, 200, 60, 200, 0)	
	#draw.line((399, 200, 340, 200), fill=(0, 0, 0), width=1)
	pr.line(img, 399, 200, 340, 200)	
	#draw.line((200, 399, 200, 340), fill=(0, 0, 0), width=1)
	pr.line(img, 200, 399, 200, 340)
	#draw.line((0, 200, 60, 200), fill=(0, 0, 0), width=1)
	pr.line(img, 0, 200, 60, 200)
	#im.save('hare.jpg', quality=95)

def ame():
	global img
	print("ame no ugoki")
	# kawari ni e wo kaku
	im = Image.new('RGB', (400, 400), (255, 255, 255))
	draw = ImageDraw.Draw(im)
	# draw.ellipse((100, 100, 300, 300), fill=(255, 255, 255), outline=(0, 0, 0))
	# draw.rectangle((100, 100, 300, 300), fill=(255, 255, 255), outline=(0, 0, 0))
	#draw.line((60, 200, 200, 80), fill=(0, 0, 0), width=1)
	#draw.line((340, 200, 200, 80), fill=(0, 0, 0), width=1)
	pr.circle(img, 200, 200, 100, -90, 90)
	pr.line(img, 300, 200, 100, 200)
	pr.line(img, 200, 200, 200, 320)
	im.save('ame.jpg', quality=95)

def kumori():
	global img
	print("kumori no ugoki")
	# kawari ni e wo kaku
	im = Image.new('RGB', (400, 400), (255, 255, 255))
	draw = ImageDraw.Draw(im)
	pr.circle(img, 200, 180, 80, -90, 90)
	pr.circle(img, 280, 260, 80, 0, 180)
	pr.line(img, 280, 340, 120, 340)
	pr.circle(img, 120, 260, 80, -180, 0)
	# draw.ellipse((100, 100, 300, 300), fill=(255, 255, 255), outline=(0, 0, 0))
	# draw.rectangle((100, 100, 300, 300), fill=(255, 255, 255), outline=(0, 0, 0))
	# draw.line((100, 0, 400, 0), fill=(255, 255, 255), width=1)
	im.save('kumori.jpg', quality=95)
    
def yuki():
	global img
	print("yuki no ugoki")
	# kawari ni e wo kaku
	im = Image.new('RGB', (400, 400), (255, 255, 255))
	draw = ImageDraw.Draw(im)
	draw.ellipse((150, 80, 250, 180), fill=(255, 255, 255), outline=(0, 0, 0))	
	draw.ellipse((100, 180, 300, 380), fill=(255, 255, 255), outline=(0, 0, 0))
	# draw.rectangle((100, 100, 300, 300), fill=(255, 255, 255), outline=(0, 0, 0))
	draw.line((120, 190, 30, 100), fill=(0, 0, 0), width=1)
	im.save('yuki.jpg', quality=95)
    
url = 'http://weather.livedoor.com/forecast/webservice/json/v1'
payload = {'city':'130010'}
tenki_data = requests.get(url,params=payload).json()

# print(tenki_data)

print(tenki_data['forecasts'][0]['date'])
print(tenki_data['forecasts'][1]['telop'])
print(tenki_data['forecasts'][1]['temperature']['max']['celsius'])

tenki = tenki_data['forecasts'][0]['telop']

# penrobo start
img = np.ones((400, 400, 3), np.uint8)*255
pr = penrobo.penRobo()
pr.start(img)


# if '曇' in tenki:
#	kumori()

# if '雨' in tenki:
#	ame()

# test
hare()
pr.erase(img)
ame()
pr.erase(img)
kumori()
# yuki()

cv2.waitKey(0)
cv2.destroyAllWindows()

