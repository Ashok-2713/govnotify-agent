@echo off
cd /d C:\Users\Ashok P\Downloads\govnotify_agent

echo [%date% %time%] Starting State Jobs...
uv run python run_states.py

echo [%date% %time%] Waiting 15 minutes for API quota reset...
timeout /t 900 /nobreak

echo [%date% %time%] Starting Central Jobs...
uv run python run_central.py

echo [%date% %time%] Importing all data to backend...
uv run python auto_upload.py

echo [%date% %time%] All updates completed!