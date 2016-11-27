:start
start /B python cache_read.py
timeout 30
taskkill /im opera.exe /f /t
taskkill /im python.exe /t
timeout 5
GOTO :start