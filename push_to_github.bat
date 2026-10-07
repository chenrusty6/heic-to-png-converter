@echo off
chcp 65001 >nul
cd /d "%~dp0"

set HOME=C:\Users\05050002

echo ========================================================
echo   推送 HEIC to PNG Converter 至 GitHub (chenrusty6)
echo ========================================================
echo.
echo 目標遠端: https://github.com/chenrusty6/heic-to-png-converter.git
echo 分支: main
echo.
echo 正在推送到 GitHub...
echo (若瀏覽器彈出 GitHub 登入視窗，請點選 Authorize 授權)
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   [成功] 程式碼與文件已成功推送到 GitHub！
    echo   您可以至以下網址查看專案：
    echo   https://github.com/chenrusty6/heic-to-png-converter
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo   [提醒] 推送未完成。請確認：
    echo   1. 您已在 GitHub 上建立了「heic-to-png-converter」倉庫。
    echo   2. GitHub 登入驗證是否已通過。
    echo ========================================================
)

echo.
pause
