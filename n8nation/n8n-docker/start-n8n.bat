@echo off
cd /d %~dp0

echo 🚀 Starting n8n via Docker Compose...
docker compose up -d

echo 🌐 Starting ngrok tunnel...
start "" ngrok.exe http --domain=generous-wren-fresh.ngrok-free.app 5678

timeout /t 5 >nul

echo 🧠 Opening n8n in your browser...
start https://generous-wren-fresh.ngrok-free.app

echo ✅ All done. You can close this window or leave it open to monitor.
pause
