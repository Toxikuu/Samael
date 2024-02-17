@echo off

rem Define the Python version to install
set PYTHON_VERSION=3.12.2

rem Define the installation directory
set INSTALL_DIR=C:\Python\%PYTHON_VERSION%

rem Define the download URL for Python
set DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

rem Create the installation directory
mkdir %INSTALL_DIR%

rem Download Python installer using PowerShell
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile 'python-installer.exe'"

rem Install Python silently
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

rem Check if Python was installed successfully by running `python --version`
python --version > nul 2>&1
if %errorlevel%==0 (
    echo Python %PYTHON_VERSION% installed successfully.
    set SUCCESS=0
) else (
    echo Failed to install Python %PYTHON_VERSION%.
    set SUCCESS=1
)

rem Remove the Python installer
del python-installer.exe

rem Exit if Python failed to install
if %SUCCESS%==1 (
    pause
    exit /b 1
)



rem Install Samael dependencies
echo Installing Samael dependencies...

rem List of modules to install
set "MODULES=requests"

rem Loop through modules and install
for %%i in (%MODULES%) do (
python -m pip install %%i
)

echo Dependencies installed.



echo Downloading Samael from Github...
rem Define Samael version
set SAMAEL_VERSION=5.1.1

rem Define the destination directory using the current user's profile directory
set DESTINATION_DIR=%USERPROFILE%\Samael

rem Create the destination directory if it doesn't exist
mkdir "%DESTINATION_DIR%" 2>nul

rem Define the URL of the raw file on GitHub
set FILE_URL=https://raw.githubusercontent.com/Toxikuu/Samael/%SAMAEL_VERSION%/Samael.py

rem Download the file using PowerShell
powershell -Command "Invoke-WebRequest -Uri '%FILE_URL%' -OutFile '%DESTINATION_DIR%\Samael.py'"

rem Check PowerShell exit code
if %errorlevel%==0 (
    echo Samael downloaded successfully.
    echo Now run %DESTINATION_DIR%\Samael.py
    echo After running Samael.py, you'll have to edit the config. Then you'll be done!
    pause
    exit /b 0
) else (
    echo Failed to download Samael.
    pause
    exit /b 1
)
