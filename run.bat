%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
set CURRENT_PATH=/d %~dp0
cd %CURRENT_PATH%
python piano.py
quit