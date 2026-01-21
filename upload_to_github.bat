@echo off
:: 切換字碼頁為 UTF-8
chcp 65001 > nul
REM ============================================================
REM Local RAG 專案 - GitHub 上傳批次檔
REM 會建立私有倉庫並上傳所有檔案
REM ============================================================

echo ============================================================
echo Local RAG 專案 GitHub 上傳工具
echo ============================================================
echo.

REM 設定變數
set REPO_NAME=localRAG
set GITHUB_USERNAME=SpencerChangTW

REM 檢查是否已設定 GitHub 使用者名稱
if "%GITHUB_USERNAME%"=="SpencerChangTW" (
    echo [錯誤] 請先編輯此批次檔，設定你的 GitHub 使用者名稱
    echo 請在檔案開頭修改: set GITHUB_USERNAME=你的GitHub使用者名
    pause
    exit /b 1
)

echo 專案名稱: %REPO_NAME%
echo GitHub 帳號: %GITHUB_USERNAME%
echo.

REM 檢查 Git 是否安裝
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 未安裝 Git，請先安裝 Git
    echo 下載: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM 檢查 GitHub CLI 是否安裝
where gh >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 未安裝 GitHub CLI (gh)
    echo 下載: https://cli.github.com/
    echo.
    echo 安裝後請執行: gh auth login
    pause
    exit /b 1
)

echo [步驟 1/6] 檢查 GitHub 登入狀態...
gh auth status >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [警告] 尚未登入 GitHub CLI
    echo 正在啟動登入流程...
    gh auth login
    if %ERRORLEVEL% NEQ 0 (
        echo [錯誤] GitHub 登入失敗
        pause
        exit /b 1
    )
)
echo ✓ GitHub 已登入
echo.

echo [步驟 2/6] 初始化 Git 倉庫...
if not exist ".git" (
    git init
    echo ✓ Git 倉庫已初始化
) else (
    echo ✓ Git 倉庫已存在
)
echo.

echo [步驟 3/6] 加入所有檔案...
git add .
echo ✓ 檔案已加入
echo.

echo [步驟 4/6] 建立首次提交...
git commit -m "Initial commit: Local RAG MCP Server" -m "完整的本地 RAG 系統，支援 MCP 協議"
if %ERRORLEVEL% EQU 0 (
    echo ✓ 提交成功
) else (
    echo ! 可能沒有新的變更或已經提交過
)
echo.

echo [步驟 5/6] 在 GitHub 建立私有倉庫...
gh repo create %REPO_NAME% --private --source=. --remote=origin --push
if %ERRORLEVEL% EQU 0 (
    echo ✓ 私有倉庫已建立並推送
    echo.
    echo ============================================================
    echo 成功！專案已上傳到 GitHub
    echo ============================================================
    echo.
    echo 倉庫 URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo 類型: 私有倉庫
    echo.
) else (
    echo [錯誤] 建立倉庫失敗
    echo.
    echo 可能原因:
    echo 1. 倉庫名稱已存在
    echo 2. 網路連線問題
    echo 3. GitHub 權限不足
    echo.
    echo 如果倉庫已存在，請使用更新腳本 (update_github.bat)
    pause
    exit /b 1
)

echo [步驟 6/6] 設定預設分支...
git branch -M main
git push -u origin main
echo.

echo ============================================================
echo 完成！
echo ============================================================
echo.
echo 下次更新使用: update_github.bat
echo.
pause
