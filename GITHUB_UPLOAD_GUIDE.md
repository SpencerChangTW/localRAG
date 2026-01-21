# GitHub 上傳使用說明

## 批次檔說明

本專案提供兩個批次檔用於管理 GitHub 倉庫：

### 1. upload_to_github.bat - 初次上傳

**用途**: 第一次上傳專案到 GitHub

**使用前準備**:
1. 安裝 Git: https://git-scm.com/download/win
2. 安裝 GitHub CLI: https://cli.github.com/
3. 登入 GitHub: `gh auth login`

**使用步驟**:

1. **編輯批次檔**，設定你的 GitHub 使用者名稱：
   ```batch
   set GITHUB_USERNAME=你的GitHub使用者名
   ```

2. **執行批次檔**：
   ```
   upload_to_github.bat
   ```

3. **完成**！倉庫會建立為**私有**並自動推送

### 2. update_github.bat - 更新變更

**用途**: 推送變更到已存在的 GitHub 倉庫

**使用方法**:
```
update_github.bat
```

系統會提示輸入提交訊息，或按 Enter 使用預設訊息。

---

## 手動操作（備選）

如果批次檔遇到問題，可以手動執行：

### 初次上傳

```bash
# 1. 初始化 Git
git init

# 2. 加入檔案
git add .

# 3. 提交
git commit -m "Initial commit"

# 4. 登入 GitHub CLI
gh auth login

# 5. 建立私有倉庫並推送
gh repo create localRAG --private --source=. --remote=origin --push
```

### 更新變更

```bash
# 1. 加入變更
git add .

# 2. 提交
git commit -m "更新說明"

# 3. 推送
git push
```

---

## 常見問題

### Q: GitHub CLI 登入失敗？
**A**: 執行 `gh auth login` 並選擇：
- What account: GitHub.com
- Protocol: HTTPS
- Authenticate: Login with a web browser

### Q: 倉庫名稱已存在？
**A**: 使用 `update_github.bat` 更新現有倉庫，或在批次檔中修改倉庫名稱

### Q: 推送失敗？
**A**: 
1. 檢查網路連線
2. 執行 `git pull` 同步遠端變更
3. 確認 GitHub 權限

### Q: 想改為公開倉庫？
**A**: 在 GitHub 網站上：
- 進入倉庫設定 (Settings)
- 拉到最下方 "Danger Zone"
- 點擊 "Change visibility"

---

## .gitignore 設定

已自動排除以下檔案：
- `qdrant_data/` - Qdrant 資料庫
- `__pycache__/` - Python 緩存
- `*.pyc` - Python 編譯檔
- `.env` - 環境變數

---

## 安全提醒

⚠️ **注意事項**:
1. 確保沒有提交敏感資訊（API keys、密碼等）
2. 檢查 `.gitignore` 是否正確設定
3. 私有倉庫只有你可以訪問
4. 定期備份重要資料

---

## 相關資源

- Git 官網: https://git-scm.com/
- GitHub CLI: https://cli.github.com/
- Git 教學: https://git-scm.com/book/zh-tw/v2
