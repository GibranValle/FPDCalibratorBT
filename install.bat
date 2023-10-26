@ECHO OFF
SET var=%cd%
set DIR=%var%
pyinstaller main.py --noconfirm --collect-all customtkinter 
xcopy %DIR%\img %DIR%\dist\main\img\ /R /S /Y /Q /E
pause
exit

