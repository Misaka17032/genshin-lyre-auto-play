import time
from midi.midifiles.midifiles import MidiFile

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

midi_file = input("Midi文件名（不含后缀）：")
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
start = {}
print("开始转换乐谱...")
for i in range(mmax):
	start[str(i)] = find(tracks, i)
out = ""
for i in range(mmax):
	temp = ""
	for note in start[str(i)]:
		try:
			temp += mapping[str(note)].upper()
		except:
			pass
	if temp != "":
		out += temp + "\n"
print("转换结束。")
print(out)
f = open("./songs/" + midi_file + ".txt", "w")
f.write(out)
f.close()