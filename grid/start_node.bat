@echo off
title SE_NODE
cd /d "%~dp0"
echo Starting Selenium NODE...
java -jar selenium-server.jar node --detect-drivers true --hub http://127.0.0.1:4444 --host 127.0.0.1
pause