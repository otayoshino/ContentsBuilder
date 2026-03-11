@echo off
chcp 65001 > nul
echo ========================================
echo   ContentsBuilder プレビューサーバー
echo ========================================
cd /d "%~dp0"
uv run python server.py
pause
