@echo off
title NATO Metadata Standards Tool
cd /d %~dp0

echo Installing dependencies...
C:\Users\cvest\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt -q

echo.
echo Starting NATO Metadata Standards Tool...
echo Open your browser at: http://localhost:5000
echo Press Ctrl+C to stop.
echo.

C:\Users\cvest\AppData\Local\Programs\Python\Python312\python.exe app.py
pause
