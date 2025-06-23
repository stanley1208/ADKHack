@echo off
title Google ADK Disaster Response System - Demo Menu
color 0E

:menu
cls
echo.
echo  ================================================================
echo   🎯 GOOGLE ADK DISASTER RESPONSE SYSTEM - DEMO MENU
echo  ================================================================
echo   🏆 Perfect for Google ADK/Cloud Hackathon Presentation!
echo  ================================================================
echo.
echo   Choose your demo option:
echo.
echo   [1] 🚀 Complete Demo Presentation (Recommended for Hackathon)
echo   [2] 🤖 Real Google ADK Agents Test  
echo   [3] 🌐 Test Live Cloud Deployment
echo   [4] 📱 Start Frontend Demo
echo   [5] 📋 View Demo Guide
echo   [6] ❌ Exit
echo.
echo  ================================================================

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto complete_demo
if "%choice%"=="2" goto adk_test
if "%choice%"=="3" goto deployment_test
if "%choice%"=="4" goto frontend_demo
if "%choice%"=="5" goto view_guide
if "%choice%"=="6" goto exit

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:complete_demo
cls
echo  🚀 Starting Complete Demo Presentation...
call demo_cmd.bat
goto menu

:adk_test
cls
echo  🤖 Starting Real ADK Agents Test...
call test_adk_cmd.bat
goto menu

:deployment_test
cls
echo  🌐 Testing Live Deployment...
call test_deployed_cmd.bat
goto menu

:frontend_demo
cls
echo  📱 Starting Frontend Demo...
call demo_frontend.bat
goto menu

:view_guide
cls
echo  📋 Opening Demo Guide...
start notepad DEMO_GUIDE.md
echo  Demo guide opened in Notepad!
timeout /t 3 >nul
goto menu

:exit
cls
echo.
echo  ================================================================
echo   🎉 Thanks for using Google ADK Disaster Response System!
echo   🏆 Good luck with your hackathon presentation!
echo  ================================================================
echo.
timeout /t 3 >nul
exit 