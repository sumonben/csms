    @echo off
    cd /d "C:\Users\CEDP\Django Projects\csms\csms"  REM Replace with your project's path
    call "C:\Users\CEDP\Django Projects\csms\.env\Scripts\activate.bat" REM Replace with your virtual environment's activate script
    start  "chrome.exe"  "http://127.0.0.1:8000/"        
	python manage.py runserver 0.0.0.0:8000
    @pause
