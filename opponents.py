import pytesseract
import cv2

from PIL import Image

import pyautogui
import keyboard

from difflib import SequenceMatcher

pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
game = True
loadingBind = '='
keyBind = '`'
playersLoaded = True
count = 0
count1 = 0
while game:
	#LOADING SCREEN
	if keyboard.is_pressed(loadingBind) and playersLoaded:
		# l_img = pyautogui.screenshot('ltest.png')
		l_img = Image.open('ltest.png')

		width, height = l_img.size
		players = []
		for j in (0, 540):
			for i in range(4):
				#CROPPING IMAGE
				p_left = (width/2) - 550 + (288 * i)
				p_top = 485 + j
				p_right = (width/2) - 310 + (288 * i)
				p_bottom = 508 + j
				l_img1 = l_img.crop((p_left, p_top, p_right, p_bottom))
				
				#CLEANING IMAGE			
				l_img1.save('l_img'+str(count1)+'.png', dpi=(300,300))
				l_img1 = cv2.imread('l_img'+str(count1)+'.png')
				count1 += 1
				l_img1 = cv2.resize(l_img1, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
				retval, threshold = cv2.threshold(l_img1,127,255,cv2.THRESH_BINARY)

				#IMAGE TO STRING
				result1 = pytesseract.image_to_string(threshold)
				result1 = result1.replace("\n", "")
				players.append(result1)

		playersLoaded = False
		print(players)

	#EACH ROUND
	if keyboard.is_pressed(keyBind):
		# img = pyautogui.screenshot('test' + str(count) + '.png')
		img = Image.open('test' + str(count) + '.png')

		#ROUND NUMBER
		width, height = img.size
		left = (width/2) - 205
		right =(width/2) - 150
		top = 10
		bottom = 35
		round_image = img.crop((left, top, right, bottom))
		round_image.save('round' + str(count) + '.png', dpi=(300, 300))

		#CLEANING IMAGE
		round_image2 = cv2.imread('round'+str(count)+'.png')
		round_image2 = cv2.resize(round_image2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
		retval, threshold = cv2.threshold(round_image2,127,255,cv2.THRESH_BINARY)

		#IMAGE TO STRING
		round_result = pytesseract.image_to_string(threshold)
		####ROUND_RESULT IS THE ROUND NUMBER
		round_result = round_result.replace("\n", "")


		#CROPPING IMAGE
		left = (width/2) - 118 + (int(round_result[-1]) * 34)
		if int(round_result[-1]) == 5:
			left = (width/2) - 118 + (4 * 34)

		top = 55
		right = left + 250
		bottom = 87
		img1 = img.crop((left, top, right, bottom))

		#CLEANING IMAGE
		img1.save('test600' + str(count) + '.png', dpi=(600,600))
		img2 = cv2.imread('test600'+str(count)+'.png')

		# img2 = Image.open('test600' +str(count) + '.png')
		count += 1
		img2 = cv2.resize(img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
		retval, threshold = cv2.threshold(img2,127,255,cv2.THRESH_BINARY)
 		
 		#IMAGE TO STRING
		result = pytesseract.image_to_string(threshold)
		result = result.replace("\n", "")
		if result[0] == 'L':
			result = result[14:]
		else:
			result = result[13:]

		print(result)
		currMax = 0
		currPlayer = ""
		for player in players:
			prob = SequenceMatcher(None, result, player).ratio()
			if prob > currMax:
				currPlayer = player
				currMax = prob

		print(currPlayer)
		




#when round changes:
#hover over round and screenshot who you faced
#crop screenshot
