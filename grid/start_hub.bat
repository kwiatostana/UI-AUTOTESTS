@echo off
title SE_HUB
cd /d "%~dp0"
echo Starting Selenium HUB...
java -jar selenium-server.jar hub --host 127.0.0.1 --publish-events tcp://127.0.0.1:4442 --subscribe-events tcp://127.0.0.1:4443
pause