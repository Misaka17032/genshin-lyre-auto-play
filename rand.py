import time
import random
import win32api
import win32con
import win32gui
import os
import threading

letter = {'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90}
chord = "zba xns cmd cmd "
melody = "wetyughjwetyughjwetyughjwetyughj "

def press(note):
	if note in letter.keys():
		win32api.keybd_event(letter[note], 0, 0, 0)
		#print("Press: ", letter[mapping[note]])
	return

def unpress(note):#48 83
	if note in letter.keys():
		win32api.keybd_event(letter[note], 0, win32con.KEYEVENTF_KEYUP, 0)
	return

def watch_dog(name):
	while True:
		if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != name:
			os._exit(0)
		time.sleep(0.01)

def pop_window(name):
	handle = win32gui.FindWindow(0, name)
	if handle == 0:
		return False
	else:
		win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
		win32gui.SetForegroundWindow(handle)
		while (win32gui.IsIconic(handle)):
			continue
		return True

pop_window("原神")
threading.Thread(target=watch_dog, args=("原神", )).start()
index = 0
note = " "
chord_note = " "
while True:
	if note != " ":
		unpress(note)
	if chord_note != " ":
		unpress(chord_note)
	note = random.choice(melody)
	if index % 2 == 0:
		chord_note = chord[(index % 32) // 2]
	if note != " ":
		press(note)
	if chord_note != " ":
		press(chord_note)
	index += 1
	# time.sleep(0.125)
	time.sleep(0.15)