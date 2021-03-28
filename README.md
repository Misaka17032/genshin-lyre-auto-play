# genshin-lyre-auto-play
根据midi文件演奏“风物之诗琴”的脚本。由python驱动。

## 运行环境

```
Windows
python 3.x
pywin32 （用于模拟键盘输入）
```

配置好python环境后使用pip install pywin32命令安装模块。

## 使用方法

对于没有接触过相关内容的用户，可以使用由@shadlc打包的exe文件：[下载链接](https://github.com/Misaka17032/genshin-lyre-auto-play/releases/download/V1.0/piano.exe)

将midi文件直接拖放在文件之上即可开始。

将曲谱放入名为`songs`的文件夹，并确保midi文件中的音符在中央C和上下两个八度的白键位。

双击run.bat或者使用管理员权限运行`python piano.py`

按照提示输入midi文件名（不包含后缀，即`.mid`）以及沉睡时间（即等待几秒开始播放）。

请务必在开始演奏前切换回游戏内页面，并且在演奏过程中保持在游戏内。

## 声明

转载请务必加上来源，谢谢。

多人联携模式正在开发中。

可以给一个star嘛，秋梨膏~
