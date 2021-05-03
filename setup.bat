@echo off
if exists env\ (
    del /F /S /Q env
    virtualenv env
)
call .\env\Scripts\activate.bat
pip install -r requirements.txt
@echo on