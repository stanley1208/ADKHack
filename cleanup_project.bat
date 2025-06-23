@echo off
title Clean Up Project Files
color 0A

echo.
echo  ================================================================
echo   🧹 CLEANING UP PROJECT - REMOVING UNRELATED FILES
echo  ================================================================
echo   Making your project clean and professional for demo
echo  ================================================================
echo.

cd /d "%~dp0"

echo  🗑️  Removing development/test files...

REM Remove old/redundant test files
if exist "test_real_adk.py" (
    del "test_real_adk.py"
    echo  ✅ Removed: test_real_adk.py (old version)
)

if exist "test_real_adk_fixed.py" (
    del "test_real_adk_fixed.py"  
    echo  ✅ Removed: test_real_adk_fixed.py (intermediate version)
)

REM Remove redundant documentation files
if exist "CMD_DEMO_READY.txt" (
    del "CMD_DEMO_READY.txt"
    echo  ✅ Removed: CMD_DEMO_READY.txt (redundant)
)

if exist "RUN_FROM_CMD.txt" (
    del "RUN_FROM_CMD.txt"
    echo  ✅ Removed: RUN_FROM_CMD.txt (redundant)
)

if exist "TESTING_CHECKLIST.txt" (
    del "TESTING_CHECKLIST.txt"
    echo  ✅ Removed: TESTING_CHECKLIST.txt (redundant)
)

REM Remove development verification files (we know it works)
if exist "verify_agent_coordination.py" (
    del "verify_agent_coordination.py"
    echo  ✅ Removed: verify_agent_coordination.py (development test)
)

if exist "verify_agents.bat" (
    del "verify_agents.bat"
    echo  ✅ Removed: verify_agents.bat (development test)
)

REM Remove one-time deployment scripts
if exist "redeploy_fix.bat" (
    del "redeploy_fix.bat"
    echo  ✅ Removed: redeploy_fix.bat (one-time use)
)

if exist "quick_test.bat" (
    del "quick_test.bat"
    echo  ✅ Removed: quick_test.bat (redundant)
)

REM Remove Python cache directories
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo  ✅ Removed: __pycache__ directory
)

REM Remove development artifacts
if exist ".bolt" (
    rmdir /s /q ".bolt"
    echo  ✅ Removed: .bolt directory (development artifact)
)

REM Remove unused agent engine if it exists and is empty/unused
if exist "agent_engine" (
    echo  ⚠️  Found agent_engine directory - checking if it's needed...
    echo     (Keeping it for now - you can remove manually if not needed)
)

echo.
echo  🧹 Cleaning up temporary files...

REM Remove any log files
if exist "*.log" (
    del "*.log"
    echo  ✅ Removed: log files
)

REM Remove any temporary files
if exist "*.tmp" (
    del "*.tmp"
    echo  ✅ Removed: temporary files
)

REM Remove test output file from parent directory
if exist "..\adk_test_output.txt" (
    del "..\adk_test_output.txt"
    echo  ✅ Removed: ../adk_test_output.txt (test output)
)

echo.
echo  ================================================================
echo   🎉 PROJECT CLEANUP COMPLETE!
echo  ================================================================
echo.
echo   📁 REMAINING ESSENTIAL FILES:
echo   ├── 🚀 Demo Files: demo_menu.bat, demo_cmd.bat, test_adk_cmd.bat
echo   ├── 🤖 Core System: main.py, Dockerfile, requirements.txt
echo   ├── 🌐 Frontend: src/, package.json, index.html
echo   ├── 🐍 Agents: python_agents/ (Detection, Analysis, Alert)
echo   ├── 📊 Backend: backend/ (Express.js API)
echo   └── 📋 Guide: DEMO_GUIDE.md
echo.
echo   🏆 Your project is now clean and ready for hackathon demo!
echo  ================================================================
echo.

pause 