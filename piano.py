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

song_list = os.listdir("./songs/")
for song_count in range(0,len(song_list)):
	print(str(song_count) + "：" + song_list[song_count])

midi_file = song_list[int(input("输入您要弹奏的midi编号并按回车："))][:-4]
print("您将要弹奏的是：" + midi_file)

try:
	midi_object = MidiFile("./songs/" + midi_file + ".mid")
except:
	print("文件损坏或不存在。")
	quit()
tick_accuracy = 0
print("尝试计算播放速度......")
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
	print("计算成功。")
except:
	tick_accuracy = int(input("计算失败，请检查文件是否完整，或者手动输入播放速度：（7）"))
type = ['note_on','note_off']
tracks = []
end_track = []
print("开始读取音轨。")
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
print("开始转换乐谱...")
for i in range(mmax):
	start[str(i)] = find(tracks, i)
shift = None
while shift is None:
	auto_tune = input("是否自动变调？([n]/y)")
	if auto_tune == "y":
		shift, score = tuner.get_shift_best_match(tracks)
		print("变调: ", shift, " 按键比例: ", score)
	elif auto_tune == "n" or auto_tune == "":
		shift = 0
close_on_switch = input("是否在切换出原神窗口时自动关闭本程序？（存在问题请不使用此选项）y/N")
auto_open = input("是否直接自动打开原神？（存在问题请不使用此选项）y/N")
if auto_open=='y':
	pop_window("原神")
else:
	stime = int(input("沉睡时间（秒）："))
	print("播放将于" + str(stime) + "秒后开始，请做好准备。")
	time.sleep(stime) 
if close_on_switch=='y':
	threading.Thread(target=watch_dog,args=("原神",)).start()
for i in range(mmax):
	if i != 0:
		for note in start[str(i - 1)]:
			unpress(str(note+shift))
	for note in start[str(i)]:
		press(str(note+shift))
	time.sleep(0.025)
print("播放结束。")
