# GitHub Copilot / VS Code MCP 配置指南

## 方式一：VS Code MCP 擴展（推薦）

### 1. 安裝 MCP 擴展

在 VS Code 中搜尋並安裝：
- **MCP Client** 或相關的 MCP 擴展

### 2. 配置 MCP Server

找到 VS Code 的設定文件：

**Windows**:
```
%APPDATA%\Code\User\settings.json
```

加入 MCP Server 配置：

```json
{
  "mcp.servers": {
    "local-rag": {
      "command": "python",
      "args": [
        "C:\\temp\\localRAG\\mcp_server.py",
        "Advantech"
      ],
      "cwd": "C:\\temp\\localRAG"
    }
  }
}
```

### 3. 重啟 VS Code

重新啟動 VS Code 讓配置生效。

### 4. 使用方式

在 VS Code 中，MCP Server 提供的工具會自動可用：
- 在 Copilot Chat 中可以要求「搜尋 Advantech 文件」
- Server 會返回 Markdown 格式的結果

---

## 方式二：workspace 配置（項目級別）

在你的項目根目錄創建 `.vscode/settings.json`：

```json
{
  "mcp.servers": {
    "local-rag": {
      "command": "python",
      "args": [
        "C:\\temp\\localRAG\\mcp_server.py",
        "Advantech",
        "DDR"
      ],
      "env": {
        "PYTHONPATH": "C:\\temp\\localRAG"
      }
    }
  }
}
```

---

## 方式三：MCP HTTP 模式（遠端訪問）

如果需要遠端訪問或團隊共享：

### 1. 啟動 HTTP 模式

```bash
python mcp_server.py --http Advantech --port 3001 --host 0.0.0.0
```

### 2. VS Code 配置

```json
{
  "mcp.servers": {
    "local-rag-http": {
      "url": "http://localhost:3001/mcp",
      "type": "http"
    }
  }
}
```

---

## 可用工具

你的 MCP Server 提供以下工具給 GitHub Copilot：

### 1. search_documents
```
搜尋本地文件資料庫

參數：
- query: 搜尋查詢（必填）
- limit: 結果數量（選填，預設5）

範例使用：
"搜尋關於 DDR memory 的 Advantech 文件"
```

### 2. list_data_sources
```
列出可用的資料來源

無參數

範例使用：
"列出所有可搜尋的資料來源"
```

---

## 驗證配置

### 檢查 Server 是否運行

```bash
# 確保 Server 正在運行
python mcp_server.py Advantech
```

### 在 VS Code 中測試

1. 打開 Copilot Chat
2. 輸入：「使用 local-rag 搜尋關於 XXX 的文件」
3. Copilot 會調用你的 MCP Server

---

## 故障排除

### Server 無法連接
- 確認 Python 路徑正確
- 確認 `mcp_server.py` 路徑正確
- 查看 VS Code 輸出面板的錯誤訊息

### Qdrant 並發錯誤
- 確保只有一個 Server 實例在運行
- 關閉其他使用 Qdrant 的程序

### Server 啟動失敗
- 檢查依賴是否安裝：`pip install -r requirements.txt`
- 確認 Qdrant 資料庫完整：`python setup.py`

---

## 進階配置

### 多個資料來源

```json
{
  "mcp.servers": {
    "local-rag-all": {
      "command": "python",
      "args": [
        "C:\\temp\\localRAG\\mcp_server.py",
        "Advantech",
        "DDR",
        "Technical Docs"
      ]
    }
  }
}
```

### 環境變數

```json
{
  "mcp.servers": {
    "local-rag": {
      "command": "python",
      "args": ["C:\\temp\\localRAG\\mcp_server.py", "Advantech"],
      "env": {
        "PYTHONPATH": "C:\\temp\\localRAG",
        "CUDA_VISIBLE_DEVICES": "0"
      }
    }
  }
}
```

---

## 注意事項

1. **Server 模式**: VS Code 使用 stdio 模式（預設），不需要 `--http` flag
2. **路徑**: 使用絕對路徑避免問題
3. **並發**: 一次只能運行一個 Server 實例（Qdrant 限制）
4. **資源**: Server 會載入 AI 模型，需要一定記憶體

---

## 參考資源

- MCP 官方文件: https://modelcontextprotocol.io
- VS Code MCP 擴展文件
- 本地檔案: `MCP_USAGE.md`
