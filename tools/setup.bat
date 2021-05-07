@echo off
cd "%~dp0\.."
if exist "%cd%\env\" (
    echo Deleting old env...
    rd /S /Q env || rem
)
if %errorlevel% NEQ 0 (
    echo 'env' folder deletion failed, please delete 'env' folder manually and run again!
    goto end
)
echo Creating new env...
echo.
virtualenv env
echo.
echo Installing Packages...
echo.
call .\env\Scripts\activate.bat
"%cd%\env\Scripts\python.exe" -m pip install --no-cache -r "%cd%\tools\requirements.txt"
echo.
echo Installation complete!
deactivate
:end
@echo on