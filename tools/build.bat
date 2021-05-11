@echo off
cd "%dp0~\.."
rd /S /Q dist || rem
call .\env\Scripts\activate.bat
pyinstaller "%cd%\app.spec" --noconfirm
rd /S /Q build || rem
deactivate
@echo on