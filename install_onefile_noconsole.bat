@ECHO OFF
SET var=%cd%
set DIR=%var%
pyinstaller main.py --noconfirm --noconsole --onefile --collect-all customtkinter 
xcopy %DIR%\img %DIR%\dist\img\ /R /S /Y /Q /E
pause
exit

