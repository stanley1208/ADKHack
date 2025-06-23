@echo off
title Real Google ADK Agents Test
color 0B

echo.
echo  ================================================================
echo   🤖 REAL GOOGLE ADK MULTI-AGENT SYSTEM TEST
echo  ================================================================
echo   Testing: Detection Agent → Analysis Agent → Alert Agent
echo  ================================================================
echo.

cd /d "%~dp0"

echo  🧪 Running Real Google ADK Pipeline...
echo.

python test_real_adk_simple.py

echo.
echo  ================================================================
echo   ✅ Real ADK Agent Test Complete!
echo  ================================================================
echo.

pause 