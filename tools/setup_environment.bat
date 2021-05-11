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
pyi-makespec --onefile --windowed --icon "%cd%/icon.ico" --add-data "%cd%/lib/ui/about.ui;lib/ui/about.ui" --add-data "%cd%/lib/ui/main.ui;lib/ui/main.ui" --add-data "%cd%/lib/ui/icons;lib/ui/icons/" "%cd%/app.py"
wrote C:\Users\ABHISHEK D\Desktop\To be sorted\Ammu\App\TriangleAdjacencyMatrix\app.spec
echo.
echo Installation complete!
deactivate
:end
@echo on