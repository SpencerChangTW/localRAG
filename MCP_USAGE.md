# MCP Server 使用指南

## MCP Server 說明

**注意**: 此腳本只能測試 Server 是否運行，無法進行完整的 MCP 通信。

## 配置說明

### GUI 方式

1. 在 GUI 左側選擇要提供服務的資料（可多選）
2. 點擊 **▶ Start Server** 
3. 系統會啟動 MCP Server 並顯示配置資訊

### 命令行方式

```bash
# 直接啟動 MCP Server
python mcp_server.py "資料名稱1" "資料名稱2"
```

## Claude Desktop 配置範例

### 完整配置範例

```json
{
  "mcpServers": {
    "local-rag": {
      "command": "python",
      "args": [
        "C:\\temp\\localRAG\\mcp_server.py",
        "技術文件",
        "產品說明"
      ]
    }
  }
}
```

### 使用路徑注意事項

- **Windows**: 使用雙反斜線 `\\` 或正斜線 `/`
- **確保 Python 路徑**: 如果 `python` 不在 PATH，請使用完整路徑
  ```json
  "command": "C:\\Python312\\python.exe"
  ```

## 常見問題

### Q: 為什麼瀏覽器打開顯示錯誤？
A: MCP Server 使用特殊協議，不支援直接瀏覽器訪問。請使用 MCP 客戶端（如 Claude Desktop）。

### Q: 如何測試 Server 是否正常？
A: 使用提供的 `test_mcp_client.py` 測試腳本。

### Q: Server 啟動後做什麼？
A: Server 會在背景運行，等待 MCP 客戶端（如 Claude Desktop）連接並調用工具。

### Q: 如何停止 Server？
A: 
- GUI: 點擊 **⏹ Stop Server**
- 命令行: 按 `Ctrl+C`

## 工具說明

MCP Server 提供以下工具：

### 1. search_documents
在選定的資料中進行語義搜尋

**參數：**
- `query` (必填): 搜尋查詢文字
- `limit` (選填): 返回結果數量，預設 5

**範例：**
```
搜尋關於「如何安裝」的文件
```

### 2. list_available_data
列出目前可檢索的資料名稱

**無參數**

## 下一步

1. 確保已上傳文件到系統
2. 啟動 MCP Server（GUI 或命令行）
3. 配置 Claude Desktop
4. 開始使用！
