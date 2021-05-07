@echo off
cd "%~dp0\.."
start .\env\Lib\site-packages\PySide2\designer.exe .\lib\ui\main.ui
@echo on