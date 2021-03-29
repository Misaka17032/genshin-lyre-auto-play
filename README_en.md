# genshin-lyre-auto-play
Using python to automatically play "Windsong Lyre" from midi files.  
This README is also available in [中文](./README.md)

[official reply to this project](./1.png)  
translation of the reply:
> It's illegal. Please don't use third-party tools, which will cause security risk to your account. We hope that travelers can work with us to maintain fairness and friendship in Teyvat.  

This project is simply just a macro, the code in this project will not cause security problems.
(Feel free to view the source code if you wanna make sure)

Tip: If your keyboard is typing but the game has no response, it's because the program doesn't have administrator rights. Double click `run_en.bat` Or running `python piano_en.py` in administrator to solve the problem!  

If the program crashes, please go through these steps:
1. Check if python 3.x is installed and path is set correctly.  
2. Check if the dependency packages are installed.  
3. Check if the input parameters are wrong.  
4. Open an issue [Here](https://github.com/Misaka17032/genshin-lyre-auto-play/issues/new/choose) with details.  

## Dependencies

```
Windows
python 3.x
pywin32 (to simulate keyboard input)
numpy
```

use `pip install pywin32 numpy` to install the modules after you installed python correctly.  

## Usage

Put your midi file in the `songs` folder. Please make sure that the notes in the midi file are white key in three octaves in C major (From C4 to B6).

Double click `run_en.bat` Or run `python piano_en.py` with administrator rights.  

Follow the instructions in the command line
- The midi file's name (Without the `.mid` suffix)
- Sleep time (How long it waits, in seconds, before the song starts playing).  

Please switch back to the game before the song starts to play. And keep the game in focus (don't tab out/switch windows) during the performance.

## Extra

Please credit the source when used for content creation (Youtube video, Reddit post, etc.).  
Please do not sell the project or the music in it.  
The Multiplayer mode is under development.  

Give a ⭐️ if this project helped you!
