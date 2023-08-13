import pyautogui
import time
import virtualkeystroke as vkey
import keyboard
import win32api, win32con
from PIL import Image
from tqdm import tqdm


# Function to simulate a mouse click at given coordinates
def click(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
	time.sleep(.01)


# Define coordinates for various actions
firstX, firstY = 664, 175
lastX, lastY = 1254, 765
openButtonX, openButtonY = 1084, 822
inputX, inputY = 1081, 740
closeButtonX, closeButtonY = 1319, 538

diffX = lastX - firstX
diffY = lastY - firstY
stepX = diffX / 31
stepY = diffY / 31
step = (stepX + stepY) / 2

pixels = {}

# Load the image and process its pixels
imageName = input("Image name:")
image = Image.open(imageName)
if image.size[0] != 32 or image.size[1] != 32:
	print("Resizing image")
	image = image.resize((32, 32), resample=Image.BOX)
	image.save(imageName, quality=100)
imagePixels = image.load()
for x in range(32):
	for y in range(32):
		try:
			pixels[imagePixels[x, y]].append([x, y])
		except KeyError:
			pixels[imagePixels[x, y]] = [[x, y]]
image.close()


# Function to convert RGB to HEX
def rgb2hex(pixel):
	return '{:02x}{:02x}{:02x}'.format(pixel[0], pixel[1], pixel[2])


# Function to simulate a mouse click on a pixel
def clickPixel(clickX, clickY):
	click(clickX, clickY)


# Function to quickly simulate a mouse click on a pixel
def clickFastPixel(addX, addY):
	clickX = round(firstX + addX * stepX)
	clickY = round(firstY + addY * stepY)
	clickPixel(clickX, clickY)


# Function to check and click a pixel with a specific color
def clickCheckPixel(addX, addY, color, s):
	clickX = round(firstX + addX * stepX)
	clickY = round(firstY + addY * stepY)
	pixelColor = s.getpixel((clickX, clickY))
	if pixelColor[0:3] == color[0:3]:
		return False
	selectColor(color)
	clickPixel(clickX, clickY)
	# print(f"{pixelColor[0:3]} -> {color[0:3]}")
	return True


# Function to select a color in the game
def selectColor(color):
	hexColor = rgb2hex(color)
	click(openButtonX, openButtonY)
	time.sleep(.01)
	click(inputX, inputY)
	time.sleep(.01)
	vkey.typer(string=hexColor)
	time.sleep(.01)
	click(closeButtonX, closeButtonY)


# Main execution
inputVar = input("Use FastPixel? ")

click(closeButtonX, closeButtonY)
click(closeButtonX, closeButtonY)

time.sleep(0.1)

if inputVar == "y":
	for color in tqdm(pixels):
		selectColor(color)
		for pixel in pixels[color]:
			clickFastPixel(pixel[0], pixel[1])
			if keyboard.is_pressed('q'):
				quit()

while keyboard.is_pressed('q') == False:
	s = pyautogui.screenshot()
	changedPixel = False
	time.sleep(0.1)
	for color in tqdm(pixels):
		for pixel in pixels[color]:
			if clickCheckPixel(pixel[0], pixel[1], color, s):
				changedPixel = True
			if keyboard.is_pressed('q'):
				quit()
	if not changedPixel:
		break
	click(closeButtonX, closeButtonY)
	time.sleep(0.1)
