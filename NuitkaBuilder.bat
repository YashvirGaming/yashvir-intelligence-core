@echo off
title 🔥 Yashvir Gaming - Nuitka 4.x PRO Builder 🔥
color 0A
cls

echo ============================================================
echo   Detecting Hardware Capabilities...
echo ============================================================

set THREADS=%NUMBER_OF_PROCESSORS%
if not defined THREADS set THREADS=4
echo [+] CPU Threads detected: %THREADS%

echo.
echo ============================================================
echo   Checking Asset Dependencies...
echo ============================================================

REM ICON RESOLUTION ENGINE
if exist app_icon.ico (
    set ICON_FLAG=--windows-icon-from-ico=app_icon.ico
    echo [+] Icon payload found: app_icon.ico
) else if exist icon.ico (
    set ICON_FLAG=--windows-icon-from-ico=icon.ico
    echo [+] Icon payload found: icon.ico
) else (
    set ICON_FLAG=
    echo [!] WARNING: No .ico file found. Compiling with default binary icon.
)

REM RUNTIME VERIFICATION
if not exist runtime\llama-server.exe (
    echo [!] WARNING: runtime\llama-server.exe missing! 
    echo [!] Ensure your inference binaries exist in \runtime before launching the EXE.
)

echo.
echo ============================================================
echo   Executing Nuitka 4.x Production Build Pipeline
echo ============================================================

python -m nuitka ^
    --mode=onefile ^
    --enable-plugin=pyside6 ^
    --jobs=%THREADS% ^
    --assume-yes-for-downloads ^
    --output-dir=. ^
    --remove-output ^
    --nofollow-import-to=tkinter ^
    --nofollow-import-to=trio ^
    --nofollow-import-to=unittest ^
    %ICON_FLAG% ^
    --include-data-dir=runtime=runtime ^
    --windows-console-mode=disable ^
    --company-name="Yashvir Gaming" ^
    --product-name="Yashvir Intelligence Core" ^
    --file-description="Yashvir Intelligence Core Engine" ^
    --copyright="Copyright (C) 2026 Yashvir Gaming. All Rights Reserved." ^
    --file-version=1.0.0.0 ^
    --product-version=1.0.0.0 ^
    --output-filename=YashvirIntelligence.exe ^
    hacker_chat.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================
    echo [X] BUILD FAILED! Check compiler output log above.
    echo ============================================================
    color 0C
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ============================================================
echo  [+] Compilation completed successfully!
echo  [+] Final Executable: YashvirIntelligence.exe
echo ============================================================
pause