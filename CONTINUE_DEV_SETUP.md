# Continue.dev MCP Server 配置指南

## Continue.dev 使用 Streamable-HTTP 模式

Continue.dev 支援 **streamable-http** 類型的 MCP Server，這正是我們實作的 HTTP/SSE 模式！

---

## 快速配置步驟

### 1. 啟動 MCP Server（HTTP 模式）

```bash
python mcp_server.py --http Advantech --port 3001
```

### 2. Continue.dev 配置

配置文件位置（Windows）：
```
%USERPROFILE%\.continue\config.yaml
```

加入以下配置：

```yaml
mcpServers:
  - name: local-rag
    type: streamable-http
    url: http://127.0.0.1:3001/mcp
```

### 3. 完整範例

```yaml
models:
  - title: "GPT-4"
    provider: "openai"
    model: "gpt-4"
    apiKey: "your-api-key"

# MCP Servers 配置
mcpServers:
  - name: local-rag
    type: streamable-http
    url: http://127.0.0.1:3001/mcp
  
  # 可以配置多個 MCP Server
  - name: local-rag-ddr
    type: streamable-http
    url: http://127.0.0.1:3002/mcp

contextProviders:
  - name: "code"
  - name: "diff"
  - name: "terminal"
```

---

## 多資料來源配置

### 方式一：單 Server 多資料

```bash
# 啟動包含多個資料來源的 Server
python mcp_server.py --http Advantech DDR "Technical Docs" --port 3001
```

```yaml
mcpServers:
  - name: local-rag-all
    type: streamable-http
    url: http://127.0.0.1:3001/mcp
```

### 方式二：多 Server 分開

啟動多個 Server 實例（不同端口）：

```bash
# Terminal 1
python mcp_server.py --http Advantech --port 3001

# Terminal 2  
python mcp_server.py --http DDR --port 3002

# Terminal 3
python mcp_server.py --http "Technical Docs" --port 3003
```

Continue.dev 配置：

```yaml
mcpServers:
  - name: local-rag-advantech
    type: streamable-http
    url: http://127.0.0.1:3001/mcp
  
  - name: local-rag-ddr
    type: streamable-http
    url: http://127.0.0.1:3002/mcp
  
  - name: local-rag-tech-docs
    type: streamable-http
    url: http://127.0.0.1:3003/mcp
```

---

## 遠端 Server 配置

如果 Server 在遠端機器或網路上：

```yaml
mcpServers:
  - name: local-rag-remote
    type: streamable-http
    url: http://192.168.1.100:3001/mcp
  
  - name: local-rag-cloud
    type: streamable-http
    url: https://your-server.com/mcp
```


---

## 使用方式

配置完成後，在 Continue.dev 中：

### 1. 直接對話

```
請搜尋 Advantech 關於 DDR memory 的文件
```

Continue.dev 會自動調用你的 MCP Server 的 `search_documents` 工具。

### 2. 使用自訂命令

如果配置了 `customCommands`：

```
/search-docs DDR memory specifications
```

### 3. 查看可用工具

```
列出 local-rag 的可用功能
```

MCP Server 會返回：
- `search_documents` - 語義搜尋
- `list_data_sources` - 列出資料來源

---

## 進階配置

### 多資料來源

```yaml
mcpServers:
  local-rag-advantech:
    command: python
    args:
      - C:\temp\localRAG\mcp_server.py
      - Advantech
  
  local-rag-ddr:
    command: python
    args:
      - C:\temp\localRAG\mcp_server.py
      - DDR
  
  local-rag-all:
    command: python
    args:
      - C:\temp\localRAG\mcp_server.py
      - Advantech
      - DDR
      - Technical Docs
```

### 環境變數

```yaml
mcpServers:
  local-rag:
    command: python
    args:
      - C:\temp\localRAG\mcp_server.py
      - Advantech
    env:
      PYTHONPATH: C:\temp\localRAG
      CUDA_VISIBLE_DEVICES: "0"
      # 可以設定其他環境變數
      LOG_LEVEL: INFO
```

### 工作目錄

```yaml
mcpServers:
  local-rag:
    command: python
    args:
      - mcp_server.py
      - Advantech
    cwd: C:\temp\localRAG
    env: {}
```

---

## 驗證配置

### 1. 檢查配置檔案

```bash
# Windows PowerShell
cat $env:USERPROFILE\.continue\config.yaml
```

### 2. 重啟 Continue.dev

重新載入 VS Code 或 IDE 讓配置生效。

### 3. 測試連接

在 Continue.dev 聊天中輸入：

```
測試 local-rag 連接
```

如果配置正確，應該可以看到 MCP Server 的回應。

---

## 故障排除

### MCP Server 無法連接

**檢查項目**:
1. ✅ Server 正在運行：`python mcp_server.py Advantech`
2. ✅ Python 路徑正確
3. ✅ 資料名稱正確
4. ✅ 沒有 Qdrant 並發問題

**查看日誌**:
Continue.dev 的日誌通常在：
```
%USERPROFILE%\.continue\logs
```

### YAML 格式錯誤

使用線上 YAML 驗證器檢查：
- https://www.yamllint.com/

常見錯誤：
- 縮排錯誤（使用空格，不要用 Tab）
- 路徑中的 `\` 需要轉義 `\\` 或使用 `/`

### Server 啟動失敗

```bash
# 手動測試 Server
python mcp_server.py Advantech

# 檢查依賴
pip install -r requirements.txt
```

---

## 範例使用場景

### 場景 1: 程式碼文件查詢

在 Continue.dev 中：
```
我需要實作 DDR4 記憶體初始化，請搜尋相關的 Advantech 技術文件
```

MCP Server 會：
1. 搜尋 "DDR4 memory initialization" 
2. 返回 Markdown 格式的相關文件
3. Continue.dev 整合結果並提供建議

### 場景 2: 技術規格查詢

```
查詢 Advantech 關於 power consumption 的規格
```

### 場景 3: 程式碼生成輔助

```
根據 Advantech 的 API 文件，生成記憶體測試程式
```

---

## 最佳實踐

1. **保持 Server 運行**: 使用 GUI (`python main.py`) 管理 Server
2. **多資料來源**: 為不同專案配置不同的 MCP Server
3. **使用相對路徑**: 在團隊環境中使用 `cwd` 配置
4. **環境變數**: 敏感資訊使用環境變數
5. **日誌監控**: 定期檢查 Continue.dev 日誌

---

## 參考資源

- Continue.dev 官方文件: https://continue.dev/docs
- MCP 協議規範: https://modelcontextprotocol.io
- 本地文件:
  - `MCP_USAGE.md`
  - `GITHUB_COPILOT_SETUP.md`

---

## 快速開始檢查清單

- [ ] 確保 MCP Server 正在運行
- [ ] 找到 Continue.dev 配置文件位置
- [ ] 加入 MCP Server 配置
- [ ] 重啟 IDE
- [ ] 測試連接
- [ ] 開始使用！
