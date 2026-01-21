@echo off
:: 切換字碼頁為 UTF-8
chcp 65001 > nul
REM ============================================================
REM Local RAG 專案 - GitHub 更新批次檔
REM 用於推送變更到已存在的 GitHub 倉庫
REM ============================================================

echo ============================================================
echo Local RAG 專案 - GitHub 更新工具
echo ============================================================
echo.

REM 檢查是否為 Git 倉庫
if not exist ".git" (
    echo [錯誤] 此目錄不是 Git 倉庫
    echo 請先執行 upload_to_github.bat 建立倉庫
    pause
    exit /b 1
)

echo [步驟 1/4] 查看變更狀態...
git status
echo.

echo [步驟 2/4] 加入所有變更...
git add .
echo ✓ 變更已加入
echo.

echo [步驟 3/4] 建立提交...
set /p COMMIT_MSG="請輸入提交訊息 (直接 Enter 使用預設訊息): "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Update: 更新 Local RAG 專案
)
git commit -m "%COMMIT_MSG%"
if %ERRORLEVEL% EQU 0 (
    echo ✓ 提交成功
) else (
    echo ! 沒有新的變更需要提交
    pause
    exit /b 0
)
echo.

echo [步驟 4/4] 推送到 GitHub...
git push
if %ERRORLEVEL% EQU 0 (
    echo ✓ 推送成功
    echo.
    echo ============================================================
    echo 完成！變更已上傳到 GitHub
    echo ============================================================
) else (
    echo [錯誤] 推送失敗
    echo.
    echo 可能原因:
    echo 1. 網路連線問題
    echo 2. 需要先執行: git pull
    echo 3. 遠端倉庫設定問題
)
echo.
pause
