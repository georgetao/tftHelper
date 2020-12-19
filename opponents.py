import pytesseract
import cv2
import sys

from PIL import Image

import pyautogui
import keyboard

from difflib import SequenceMatcher

pytesseract.pytesseract.tesseract_cmd ='C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

args = sys.argv


loadingBind = '='
keyBind = '`'
test = False

def getPlayers():
	if not test:
		l_img = pyautogui.screenshot('./screenshots/loadingScreen.png')
	else:
		l_img = Image.open('./screenshots/loadingScreen.png')

	count = 0
	width, height = l_img.size
	players = []

	for y in (0, 540):
		for x in range(4):
			#CROPPING IMAGE
			left = (width/2) - 550 + (288 * x)
			top = 485 + y
			right = (width/2) - 310 + (288 * x)
			bottom = 508 + y
			p_name = l_img.crop((left, top, right, bottom))
			
			#CLEANING IMAGE			
			p_name.save('./screenshots/player'+str(count)+'.png', dpi=(300,300))
			p_name = cv2.imread('./screenshots/player'+str(count)+'.png')
			count += 1
			p_name = cv2.resize(p_name, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
			retval, threshold = cv2.threshold(p_name,127,255,cv2.THRESH_BINARY)

			#IMAGE TO STRING
			res = pytesseract.image_to_string(threshold)
			res = res.replace("\n", "")
			players.append(res)

	currMax = 0
	currPlayer = ""
	for player in players:
		prob = SequenceMatcher(None, args[1], player).ratio()
		if prob > currMax:
			currPlayer = player
			currMax = prob

	players.remove(currPlayer)	

	return players

def getCurrentRound(count):
	if not test:
		img = pyautogui.screenshot('./screenshots/round' + str(count) + '.png')
	else:
		img = Image.open('./screenshots/round' + str(count) + '.png')

	#ROUND NUMBER
	width, height = img.size
	left = (width/2) - 205
	right =(width/2) - 150
	top = 10
	bottom = 35
	round_num_img = img.crop((left, top, right, bottom))
	round_num_img.save('./screenshots/round_num' + str(count) + '.png', dpi=(300, 300))

	#CLEANING IMAGE
	round_num_img = cv2.imread('./screenshots/round_num'+str(count)+'.png')
	round_num_img = cv2.resize(round_num_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
	retval, threshold = cv2.threshold(round_num_img,127,255,cv2.THRESH_BINARY)

	#IMAGE TO STRING
	round_num = pytesseract.image_to_string(threshold)
	####ROUND_NUM IS THE ROUND NUMBER
	round_num = round_num.replace("\n", "")
	print(round_num)
	return round_num

def getLastOpponent(round_num, count):
	img = Image.open('./screenshots/loadingScreen.png')
	
	#CROPPING IMAGE
	width, height = img.size
	left = (width/2) - 118 + (int(round_num[-1]) * 34)
	if int(round_num[-1]) == 5:
		left = (width/2) - 118 + (4 * 34)

	top = 55
	right = left + 250
	bottom = 87

	pyautogui.moveTo(left-55, top-35)

	if not test:
		img = pyautogui.screenshot('./screenshots/opponent' + str(count) + '.png')
	else:
		img = Image.open('./screenshots/round' + str(count) + '.png')
	
	prev_player = img.crop((left, top, right, bottom))

	#CLEANING IMAGE
	prev_player.save('./screenshots/prev_player' + str(count) + '.png', dpi=(600,600))
	prev_player = cv2.imread('./screenshots/prev_player'+str(count)+'.png')

	# img2 = Image.open('test600' +str(count) + '.png')
	prev_player = cv2.resize(prev_player, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
	retval, threshold = cv2.threshold(prev_player,127,255,cv2.THRESH_BINARY)
		
		#IMAGE TO STRING
	result = pytesseract.image_to_string(threshold)
	result = result.replace("\n", "")
	if result[0] == 'L':
		result = result[14:]
	else:
		result = result[13:]

	currMax = 0
	currPlayer = ""
	for player in players:
		prob = SequenceMatcher(None, result, player).ratio()
		if prob > currMax:
			currPlayer = player
			currMax = prob

	return currPlayer




game = True
playersLoaded = True
count = 0

while game:
	#LOADING SCREEN
	if keyboard.is_pressed(loadingBind) and playersLoaded:

		playersLoaded = False
		players = getPlayers()
		print(players)

		canPlay = players.copy()
		cantPlay = []

	#EACH ROUND
	if keyboard.is_pressed(keyBind):
		round_num = getCurrentRound(count)
		lastOpponent = getLastOpponent(round_num, count)
		count += 1

		print(lastOpponent)
		cantPlay.append(lastOpponent)
		canPlay.remove(lastOpponent)
		if len(cantPlay) > 4:
			canPlay.append(cantPlay.pop(0))

		print(canPlay)
		




#when round changes:
#hover over round and screenshot who you faced
#crop screenshot

