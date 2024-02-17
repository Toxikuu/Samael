@echo off

rem Define the Python version to install
set PYTHON_VERSION=3.12.2
echo Downloading python version %PYTHON_VERSION%

rem Define the installation directory
set INSTALL_DIR=C:\Python\%PYTHON_VERSION%
echo Installation directory: %INSTALL_DIR%

rem Define the download URL for Python
set DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

rem Create the installation directory
mkdir %INSTALL_DIR%

rem Download Python installer using PowerShell
echo Downloading Python with PowerShell
powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile 'python-installer.exe'"

rem Install Python silently
echo Installing Python
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo Deleting Python installer
rem Remove the Python installer
del python-installer.exe
set PATH=%PATH%


rem Install Samael dependencies
echo Installing Samael dependencies...

rem List of modules to install
set "MODULES=requests"
echo Pip installing necessary python libraries

rem Loop through modules and install
for %%i in (%MODULES%) do (
python -m pip install %%i
)

echo Dependencies installed.



rem Define Samael version
set SAMAEL_VERSION=v5.1.2
echo Downloading Samael %SAMAEL_VERSION% from Github...

rem Define the destination directory using the current user's profile directory
set DESTINATION_DIR=%USERPROFILE%\Samael

rem Create the destination directory if it doesn't exist
mkdir "%DESTINATION_DIR%" 2>nul

rem Define the URL of the raw file on GitHub
set SAMAEL_URL=https://raw.githubusercontent.com/Toxikuu/Samael/%SAMAEL_VERSION%/Samael.py
set TOX_ASSETS_URL=https://raw.githubusercontent.com/Toxikuu/Samael/%SAMAEL_VERSION%/tox_assets.py

echo Downloading Samael.py and tox_assets.py to %DESTINATION_DIR% with PowerShell
rem Download the file using PowerShell
powershell -Command "Invoke-WebRequest -Uri '%SAMAEL_URL%' -OutFile '%DESTINATION_DIR%\Samael.py'"
powershell -Command "Invoke-WebRequest -Uri '%TOX_ASSETS_URL%' -OutFile '%DESTINATION_DIR%\tox_assets.py'"

rem Check PowerShell exit code
if %errorlevel%==0 (
    echo Downloaded successfully.
    echo Now run %DESTINATION_DIR%\Samael.py
    echo After running Samael.py, you'll have to edit the config. Then you'll be done!
    pause
    exit /b 0
) else (
    echo Failed to download.
    pause
    exit /b 1
)
