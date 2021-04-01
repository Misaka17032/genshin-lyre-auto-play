import time
import win32api
import win32con
import random
import cv2
import os

from midi.midifiles.midifiles import MidiFile

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
for i, track in enumerate(midi_object.tracks):
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
start = []
intervals = []
print("开始转换乐谱...")
t = 0
for i in range(mmax):
	a = find(tracks, i)
	if a != []:
		start.append(a)
		intervals.append(t)
		t = 0.025
	else:
		t += 0.025
back = cv2.imread('./B.png')
index = 0
print("准备就绪。")
pressed = False
timer = time.time()
while index < len(start):
	img = back.copy()
	interval = timer - time.time()
	if interval <= 1.8:
		radius = 61
		if interval > 0:
			radius = (1.8 - interval) / 3 * 100
		cv2.circle(img, (73, 73), int(radius), (68, 224, 255), thickness=-1)
	if win32api.GetAsyncKeyState(win32con.VK_SPACE) == 0 and pressed:
		pressed = False
	if win32api.GetAsyncKeyState(win32con.VK_SPACE) != 0 and not pressed:
		pressed = True
		for note in start[index]:
			# while random.random() < 0.5 and len(start[index]) > 1:
			# 	time.sleep(random.uniform(0.01, 0.02))
			press(str(note))
		time.sleep(0.025)
		for note in start[index]:
			unpress(str(note))
		index += 1
		timer = time.time() + intervals[index]
	cv2.imshow("按下光圈", img)
	cv2.waitKey(1)
print("播放结束。")
cv2.destroyAllWindows()