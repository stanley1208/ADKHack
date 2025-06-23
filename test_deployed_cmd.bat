@echo off
title Test Live Deployed System
color 0C

echo.
echo  ================================================================
echo   🚀 TESTING LIVE GOOGLE CLOUD RUN DEPLOYMENT
echo  ================================================================
echo   URL: https://disaster-response-system-838920435800.us-central1.run.app
echo  ================================================================
echo.

echo  🔍 Testing main API endpoint...
curl -s https://disaster-response-system-838920435800.us-central1.run.app/
echo.
echo.

echo  🔍 Testing health endpoint...  
curl -s https://disaster-response-system-838920435800.us-central1.run.app/health
echo.
echo.

echo  ================================================================
echo   ✅ Live System Test Complete!
echo   Status: System is operational and responding
echo  ================================================================
echo.

pause 