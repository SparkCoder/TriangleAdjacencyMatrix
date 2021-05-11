@echo off
pyside2-rcc "%~dp0res.qrc" -o "%~dp0res_rc.py"
@echo on