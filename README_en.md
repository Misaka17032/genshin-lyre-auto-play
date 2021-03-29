# genshin-lyre-auto-play
Using python to automatically play "Windsong Lyre" according to midi files.  
This README is also available in [中文](./README.md)

[official reply to this project](./1.png)  
translation of the reply:
> It's illegal. Please don't use third-party tools, which will cause security risk to your account. We hope that travelers can work with us to maintain fairness and friendship in Teyvat.  

We promise that the code in this project will not cause security problems.

Tips: If your keyboard is typing but the game has no response, it's because the program doesn't have administrator rights. Double click `run_en.bat` Or running the command line in administrator mode can solve the problem!  

If the program crash once you open it, please check according to the following steps:
1. Check if python 3.x is installed and path is set correctly.  
2. Check if the dependency package is installed.  
3. Check if the input parameters are wrong.  
4. Open an issue with details.  

## environment

```
Windows
python 3.x
pywin32 (to simulate keyboard input)
numpy
```

use `pip install pywin32 numpy` to install the module after you installed python correctly.  

## usage

Put your midi file in the `songs` folder. Please make sure that the notes in the midi file are white key in three octaves in C major.  

Double click `run_en.bat` Or run `python piano_en.py` with administrator rights.  

Follow the tips to input the midi file's name(without suffix `.mid`) and sleep time(wait how many seconds to start playing).  

Please switch back to the game before the program starting to play. And stay in the game during playing.

## statement

Please indicate the source when reprint.  
Please do not use the project itself or the music in it for business.  
The Multiplayer mode is under development.  

Give a ⭐️ if this project helped you!
