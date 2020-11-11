#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import time
import os

# os.get_terminal_size().columns
# os.get_terminal_size().lines

# print(os.get_terminal_size().lines)

# IMPORTANT! You cannot print to the bottom line of the screen using Curses!
# You can, just not the last character on the bottom line, that would trigger a return

x = 0
curLine = ""

# scr = ["+------+----------+------+-----------------------------------------------------+","| Exit | Settings | Back | /Users/jonm/Documents/Demo                          |","+------+----------+------+-----------------------------------------------------+","|                __            ______      ______       __                    ^|","|               |  \\____     /|Open  |    |Open  |\\    |  \\____                |","|   /______     |       |    \\|Exit  |    |Exit  |/    |       |               |","|   \\‾‾‾‾‾‾     |       |     |Rename|    |Rename|     |       |               |","|                ‾‾‾‾‾‾‾      |Copy  |    |Copy  |      ‾‾‾‾‾‾‾                |","|  Up One       Lorem ips     |Move  |    |Move  |     Lorem ips               |","|  Directory    um dol...     |Info  |    |Info  |     um dol...               |","|                pulvinar     |Delete|    |Delete|      pulvinar               |","|                              ‾‾‾‾‾‾      ‾‾‾‾‾‾                              |","|    ___            _                                                          |","|   |   |\\        _| |_                                                        |","|   |    ‾|      |     |                                                       |","|   |     |       ‾| |‾                                                        |","|    ‾‾‾‾‾          ‾                                                          |","|  Lorem ips    Add File                                                       |","|  um dol...    Or Folder                                                      |","|  vinar.txt                                                                   |","|                                                                              |","|                                                                             v|","+------------------------------------------------------------------------------+"]
# print(scr[23])
# printing out an example screen
# for y in range(0,23):
# 	curLine = scr[y]
# 	screen.addstr(y,0,curLine)


# Minimum lines: 13
# Minimum columns: 20
try:
	if os.get_terminal_size().columns < 20 or os.get_terminal_size().lines < 14:
		print("Your terminal isn't large enough")
		print("Yatui requires at least 20 columns and 13 lines to run")
except Exception as e:
	print("Yatui was not able to get your terminal window size")
	raise e

# Initializing the log text file
logTextFile = open("fmtuiFullLog.txt", "a")
# adding a time stamp to the log before the program is run
t = time.localtime()
# This tutorial is very helpful for understanding the format function
# https://realpython.com/python-formatted-output
logTextFile.write("\n\nProgram run on {:d}/{:0>2d}/{:0>2d} at {:0>2d}:{:0>2d}:{:0>2d}\n".format(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec))
logTextFile.close()

# print(menuBorderLine)
# print(menuLine)
# print(menuBorderLine)
# print(centralLine)
# print(bottomLine)

class directoryItem:
	def __init__(self, label, iconName, xPos, yPos):
		self.label = label
		self.iconName = iconName
		self.xPos = xPos
		self.yPos = yPos

def log(cursesScreenObject, text):
	logTextFile = open("fmtuiFullLog.txt", "a")
	try:
		logTextFile.write(str(text) + "\n")
	except Exception as e:
		logTextFile.write("An error ocurred while trying to add a line to the log file")
		logTextFile.write("This could be because of an error with the data type you are trying to log")
		print("error displaying text for the log function")
		raise e
	logTextFile.close()
	cursesScreenObject.addstr(os.get_terminal_size().lines-1,0,text)

def printIcon(cursesScreenObject, directoryItemObject):#, line, column, type, text=""):
	# add input validation so that you can't print outside of the boundries of the screen

	if directoryItemObject.iconName=="+":
		iconStrArray = ["    _    ","  _| |_  "," |     | ","  ‾| |‾  ","    ‾    "]
		# text = "Add File Or Folder"
	elif directoryItemObject.iconName=="<":
		iconStrArray = ["  ,      "," /|_____ ","|       |"," \\|‾‾‾‾‾ ","  `      "]
		# text = "Up One   Directory"
	elif directoryItemObject.iconName=="directory":
		iconStrArray = [" __      ","|  \\____ ","|       |","|       |"," ‾‾‾‾‾‾‾ "]
	elif directoryItemObject.iconName=="file":
		iconStrArray = ["  ___    "," |   |\\  "," |    ‾| "," |     | ","  ‾‾‾‾‾  "]
	else:
		iconStrArray = ["..-#-#-#-#-..","..#-#-#-#-#..","..-#-#-#-#-..","..#-#-#-#-#..","..-#-#-#-#-.."]
		# for i in range(0,5):
		# 	cursesScreenObject.addstr(directoryItemObject.yPos+i,directoryItemObject.xPos,iconStrArray[i])
		# return

	filenameStrArray = []
	text = directoryItemObject.label

	filenameStrArray.append(text[0:9])
	text = text[9:]

	if len(text)>18:
		filenameStrArray.append(text[0:8] + "…")
		filenameStrArray.append(text[len(text)-9:])
	else:
		filenameStrArray.append(text[0:9])
		text = text[9:]
		filenameStrArray.append(text)

	for i in range(0,5):
		# cursesScreenObject.addstr(line+i,column,"  " + iconStrArray[i] + "  ")
		cursesScreenObject.addstr(directoryItemObject.yPos+i,directoryItemObject.xPos,iconStrArray[i])
	for i in range(5,8):
		cursesScreenObject.addstr(directoryItemObject.yPos+i,directoryItemObject.xPos,filenameStrArray[i-5])

def main(screen):
	# Hiding the cursor
	curses.curs_set(0)

	# This section sets up the background of the tui
	# Four rows are needed, but menuBorderLine is used twice, because it acts as both the top and bottom of the menu
	# Giving the lines seed values
	menuBorderLine = "+---+---+---+------" # +
	menuLine =       "| X | S | B |      " # |
	centralLine =    "|                  " # |
	bottomLine =     "+------------------" # +

	# adding the charachters that depend on the width of the terminal
	# I'm doing a range from 1 to the max value because there's one additional
	# character added to the end of each line in the next step
	# Setting the lower bound to 1 keeps me from having to subtract the length of the border line +1
	for i in range(1,os.get_terminal_size().columns - len(menuBorderLine)):
		menuBorderLine += "-"
		menuLine += " "
		centralLine += " "
		bottomLine += "-"

	# adding the end-of-line characters
	menuBorderLine += "+"
	menuLine += "|"
	centralLine += "|"
	bottomLine += "+"

	# adding the new lines to the screen
	screen.addstr(0,0,menuBorderLine)
	screen.addstr(1,0,menuLine)
	screen.addstr(2,0,menuBorderLine)
	for r in range(1,os.get_terminal_size().lines-4):
		screen.addstr(r+2,0,centralLine)
	screen.addstr(os.get_terminal_size().lines-2, 0, bottomLine)

	# This section adds the current directory path to the screen
	# If the path is too long, the beginning is cut off, and an elipses (…) character is added
	workingDir = os.getcwd()
	if len(workingDir)>(os.get_terminal_size().columns-16):
		workingDir = workingDir[len(workingDir)-(os.get_terminal_size().columns-16-1):]
		workingDir = "…" + workingDir
	screen.addstr(1,14,workingDir)
	
	# This section sets up the grid that the file and folder icons will be placed in.
	# The // operator is division without remainder
	# The numbers being subtracted account for the lines already in use by the background
	iconColumns = (os.get_terminal_size().columns-3)//13
	iconRows = (os.get_terminal_size().lines-4)//9

	# xOffset and yOffset are used to position the icons on the screen, and represent the icon column and row
	# instead of the actual column and row on the terminal.
	xOffset = 0
	yOffset = 0

	# scrollNeeded is set to true if there isn't enough space on just one page to put all of the icons
	# scrollNeeded = False
	# if len(fileAndFolderList)>(iconColumns*iconRows):
	# 	scrollNeeded = True

	# This code is used to initialize the current page variable, and figure out how many pages are needed to
	# fully display the contents of a directory. The doubble minus signs are a trick to use ceiling integer
	# division, instead of floor integer division, which is documented here:
	# https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
	# I am subtracting 1 from it at the end because curPageNum is zero indexed
	# curPageNum = 0
	# maxPageNum = -(-len(fileAndFolderList)//(iconColumns*iconRows)) - 1	

	# these next two lines can be used to get a directory with fewer items in it, and switch back
	# os.chdir("/Users/joannm/Desktop/Programming/Python/shRender")
	# os.chdir("/Users/joannm/Desktop/Programming/Python/yatui")

	# These two pieces of code are extremely minified, and shamelessly stolen from stackoverflow
	# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
	# onlyFiles and onlyDirectories are lists of strings containing the names of files and directories, respectively

	# onlyFiles = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(), f))]
	# onlyDirectories = [f for f in os.listdir(os.getcwd()) if not(os.path.isfile(os.path.join(os.getcwd(), f)))]

	# This makes one list with all of the directories and files in it.
	# The two additional elements at the beginning and end are for the "up one directory" and "add file/folder" icons

	# fileAndFolderList = [""] + onlyDirectories + onlyFiles + [""]

	xInc = 0
	yInc = 0

	fileAndFolderList = [directoryItem("Up One   Directory","back",0,0)]
	for diName in os.listdir():
		#di stands for directory item
		if os.path.isfile(diName):
			diType = "file"
		else:
			diType = "directory"
		fileAndFolderList.append(directoryItem(diName,diType,xInc,yInc))
		
		xInc += 1
		if xInc == iconColumns:
			xInc = 0
			yInc += 1

		# log(screen, diName + " " + diType + " @ (" + xInc + "," + yInc + ")")
		# log(screen, "{a} {b} at ({c},{d})".format(a=diName, b=diType, c=xInc, d=yInc))
	fileAndFolderList = [directoryItem("Add File Or Folder","add",xInc,yInc)]

	"""
	fileAndFolderLayout = []
	fileAndFolderLayoutHelper = []

	for di in fileAndFolderList:
		fileAndFolderLayoutHelper.append(di)
		log(screen, di.label)
		xInc += 1
		if xInc == iconColumns:
			xInc = 0
			fileAndFolderLayout.append(fileAndFolderLayoutHelper)
			fileAndFolderLayoutHelper = []
			log(screen, "\n")
	"""
		

	screen.refresh()
	key = ""

	"""

	while 1:
		log(screen, "At the beginning of the loop, curPageNum = " + str(curPageNum))
		# log(screen, "key = " + key)
		if key == "KEY_DOWN" and curPageNum < maxPageNum:
			curPageNum += 1
			log(screen, "recieved key down")
			log(screen, "updating curPageNum to " + str(curPageNum))
		elif key == "KEY_UP" and curPageNum > 0:
			curPageNum -= 1
			log(screen, "recieved key down")
			log(screen, "updating curPageNum to " + str(curPageNum))
		elif key == "x":
			break

		for i in range(curPageNum*(iconColumns*iconRows),len(fileAndFolderList)):
			if i == 0:
				typeOfIcon = "<"
				# The first icon to display should always be the "up one directory" arrow
			elif i <= len(onlyDirectories):
				typeOfIcon = "directory"
			elif i != len(fileAndFolderList)-1:
				typeOfIcon = "file"
			else:
				typeOfIcon = "+"
				# The last icon to display is always the "add new file or folder" icon
			
			# Given the type of icon from the if statements above, this actually prints it to the screen
			# along with its name. The equations surrounding yOffset and xOffset convert their icon column and
			# Icon row positions into positions on the terminal screen
			printIcon(screen,3+(yOffset*9),3+(xOffset*13),typeOfIcon,fileAndFolderList[i])

			# This adjusts the position where the icon is printed for the next cycle of the loop
			# i is 0 indexed, so both cases where 1 is added make it 1 indexed for the sake of math
			# The first if statement checks to see if all of the spaces for icons are used up
			# If no more icons can be printed, the second if statement resets the xOffset, and moves the yOffset
			# down one row
			if i+1 == (iconColumns*iconRows):
				xOffset = 0
				yOffset = 0
				break
			xOffset += 1
			if (i+1)%iconColumns == 0:
				xOffset = 0
				yOffset += 1
		# log(screen, "hello")

		screen.refresh()
		# allowing the screen to update, and show the new changes
		log(screen, "execution paused while waiting for user input")
		key = screen.getkey()
		# pausing execution until the user's next keypress
		
		# time.sleep(0.01)
	"""

	# clearing the screen
	screen.clear()


curses.wrapper(main)