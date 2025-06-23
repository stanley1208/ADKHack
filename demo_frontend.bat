@echo off
echo 🎯 STARTING FRONTEND DEMO FOR DISASTER RESPONSE SYSTEM
echo =====================================================
echo.

cd /d "%~dp0"

echo 📦 Installing frontend dependencies...
npm install

echo.
echo 🚀 Starting development server...
echo Frontend will connect to deployed backend: 
echo https://disaster-response-system-838920435800.us-central1.run.app
echo.
echo 🌐 Frontend will be available at: http://localhost:5173
echo.

npm run dev

pause 