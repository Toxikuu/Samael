@echo off
echo Installing Samael dependencies...

rem List of modules to install
set "MODULES=requests dhooks"

rem Loop through modules and install
for %%i in (%MODULES%) do (
  python -m pip install %%i
)

echo Dependencies installed.
pause
