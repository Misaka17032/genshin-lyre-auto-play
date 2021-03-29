from __future__ import print_function
import ctypes, sys
import os
import time
import win32api
import win32con
import win32gui
import threading

from midi.midifiles.midifiles import MidiFile
from midi.helpers import tuner

letter = {'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90}
mapping = {'48': 'z', '50': 'x', '52': 'c', '53': 'v', '55': 'b', '57': 'n', '59': 'm', '60': 'a', '62': 's', '64': 'd', '65': 'f', '67': 'g', '69': 'h', '71': 'j', '72': 'q', '74': 'w', '76': 'e', '77': 'r', '79': 't', '81': 'y', '83': 'u'}

def dinput():
	a = {}
	count = 36
	while count <= 84:
		a[str(count)] = int(input())
		count += 1
	return a

def find(arr, time):
	result = []
	for i in arr:
		if i["time"] == time:
			result.append(i["note"])
	return result

def press(note):#48 83
	if note in mapping.keys():
		win32api.keybd_event(letter[mapping[note]], 0, 0, 0)
		#print("Press: ", letter[mapping[note]])
	return

def unpress(note):#48 83
	if note in mapping.keys():
		win32api.keybd_event(letter[mapping[note]], 0, win32con.KEYEVENTF_KEYUP, 0)
	return

def make_map():
	s = "zxcvbnmasdfghjqwertyu"
	for i, k in enumerate(mapping.keys()):
		mapping[k] = s[i]
	print(mapping)

def pop_window(name):
	handle = win32gui.FindWindow(0, name)
	if handle == 0:
		return False
	else:
		win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND,
								win32con.SC_RESTORE, 0)
		win32gui.SetForegroundWindow(handle)
		while (win32gui.IsIconic(handle)):
			continue
		return True

def watch_dog(name):
	while True:
		if win32gui.GetWindowText(win32gui.GetForegroundWindow())!=name:
			os._exit(0)

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False
if is_admin():
	pass
else:
	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
	exit(0)

midi_file = input("Midi file's name(without suffix .mid):")
try:
	midi_object = MidiFile("./songs/" + midi_file + ".mid")
except:
	print("File is broken or does not exist.")
	quit()
tick_accuracy = 0
print("Try to calculate the playback speed...")
try:
	flag = False
	for i in midi_object.tracks:
		for j in i :
			if j.dict()["type"] == "set_tempo":
				flag = True
				tempo = j.tempo
				break
		if flag:
			break
	bpm = 60000000 / tempo
	tick_accuracy = bpm / 20
	print("Calculate successfully")
except:
	tick_accuracy = int(input("Calculation failed, please check whether the file is broken or manually input the playback speed:(7)"))
type = ['note_on','note_off']
tracks = []
end_track = []
print("Start reading tracks")
for i,track in enumerate(midi_object.tracks):
	print(f'track{i}')
	last_time = 0
	last_on = 0
	for msg in track:
		info = msg.dict()
		info['pertime'] = info['time']
		info['time'] += last_time
		last_time = info['time']
		if (info['type'] in type):
			del info['channel']
			del info['velocity']
			info['time'] = round(info['time'] / tick_accuracy)
			if info['type'] == 'note_on':
				del info['type']
				del info['pertime']
				last_on = info['time']
				tracks.append(info)
			else:
				del info['type']
				del info['pertime']
				last_on = info['time']
				end_track.append(info)
mmax = 0
for i in tracks:
	mmax = max(mmax, i['time'] + 1)
start = {}
print("Start converting music score...")
for i in range(mmax):
	start[str(i)] = find(tracks, i)
shift = None
while shift is None:
	auto_tune = input("Automatic tone shift?([n]/y)")
	if auto_tune == "y":
		shift, score = tuner.get_shift_best_match(tracks)
		print("Tone shift: ", shift, " Key ratio: ", score)
	elif auto_tune == "n" or auto_tune == "":
		shift = 0
close_on_switch = input("Close this program once switch out game window?(Don't use this if there's any problem)(y/N)")
auto_open = input("Open game window automatically？(Don't use this if there's any problem)(y/N)")
if auto_open=='y':
	pop_window("Genshin Impact")
else:
	stime = int(input("Sleep time(seconds):"))
	print("Play will start in " + str(stime) + " seconds")
	time.sleep(stime)
if close_on_switch=='y':
	threading.Thread(target=watch_dog,args=("Genshin Impact",)).start()
for i in range(mmax):
	if i != 0:
		for note in start[str(i - 1)]:
			unpress(str(note+shift))
	for note in start[str(i)]:
		press(str(note+shift))
	time.sleep(0.025)
print("End of play.")
