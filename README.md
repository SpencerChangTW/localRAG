# Local RAG 系統

一個本地的 RAG（Retrieval Augmented Generation）文件管理系統，支援多種文件格式的上傳、向量化儲存，並提供 MCP Server 檢索服務。

## 功能特色

✅ **多格式文件支援**
- PDF、Word (.docx, .doc)
- 文字檔 (.txt)
- 圖片 (.jpg, .jpeg, .png)
- PowerPoint (.pptx, .ppt)

✅ **智能文件處理**
- 使用 Markitdown 轉換文件為 Markdown
- 自動文字分塊
- 語義向量嵌入

✅ **向量資料庫**
- 使用 Qdrant 儲存文件向量
- 高效的相似度搜尋
- 資料名稱分類管理

✅ **直觀的 GUI 介面**
- Tkinter 視窗應用程式
- 簡單易用的文件上傳
- 資料管理與刪除

✅ **MCP Server 服務**
- 提供文件檢索 API
- 可選擇特定資料提供服務
- 標準 MCP 協議

## 安裝步驟

### 1. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 2. 執行程式

```bash
python main.py
```

## 資料儲存

> [!NOTE]
> 所有向量資料存儲在本地 `qdrant_data/` 目錄。
> - 首次執行會自動建立
> - 資料持久化保存
> - 可隨時備份或刪除此目錄

> [!TIP]
> 使用 `setup.py` 可以快速檢查環境：
> ```bash
> python setup.py
> ```

**就這麼簡單！** 系統會自動在本地 `qdrant_data/` 目錄建立向量資料庫，無需額外安裝或啟動任何服務。

## 使用說明

### 上傳文件

1. 點擊「選擇檔案」按鈕
2. 選擇要上傳的文件（支援 PDF, Word, TXT, 圖片, PPT）
3. 輸入資料名稱（用於分類管理）
4. 點擊「上傳並處理」

系統會自動：
- 使用 Markitdown 轉換文件
- 進行文字分塊
- 生成嵌入向量
- 儲存到 Qdrant 資料庫

### 管理資料

- **查看資料**: 左側列表顯示所有已儲存的資料名稱
- **刪除資料**: 選中資料後點擊「刪除選中的資料」

### 4. 啟動 MCP Server

1. 在資料列表中選擇要提供服務的資料（可多選）
2. 點擊「▶ Start Server」
3. 複製顯示的 URL

**重要提醒：**
> MCP Server 不是一般網頁服務，**不能直接在瀏覽器訪問**。
> 需要使用 MCP 客戶端（如 Claude Desktop）連接。

### 5. 使用 MCP Server

**方式一：Claude Desktop（推薦）**

在 Claude Desktop 配置文件中加入：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "local-rag": {
      "command": "python",
      "args": ["C:\\temp\\localRAG\\mcp_server.py", "你的資料名稱"]
    }
  }
}
```

重啟 Claude Desktop 後即可使用。

**方式二：測試腳本**

```bash
python test_mcp_client.py "資料名稱"
```

**詳細說明請參考**: [MCP_USAGE.md](file:///c:/temp/localRAG/MCP_USAGE.md)

## 專案結構

```
localRAG/
├── main.py                 # 主程式入口
├── config.py               # 系統配置
├── document_processor.py   # 文件處理模組
├── vector_db.py            # Qdrant 資料庫操作
├── mcp_server.py           # MCP Server 實作
├── gui_app.py              # Tkinter GUI 應用程式
├── requirements.txt        # Python 依賴套件
└── README.md               # 本文件
```

## 技術架構

- **文件轉換**: Markitdown
- **向量嵌入**: Sentence Transformers (all-MiniLM-L6-v2)
- **向量資料庫**: Qdrant
- **GUI 框架**: Tkinter
- **MCP 框架**: mcp Python SDK

## 配置說明

主要配置在 `config.py` 中：

```python
QDRANT_PATH = "./qdrant_data"     # 本地資料庫路徑
EMBEDDING_MODEL = "..."            # 嵌入模型
CHUNK_SIZE = 500                   # 分塊大小
CHUNK_OVERLAP = 50                 # 分塊重疊
```

## 依賴套件

- markitdown: 文件轉換
- qdrant-client: 向量資料庫客戶端
- sentence-transformers: 文字嵌入
- mcp: MCP Server 框架
- python-docx, pypdf, PIL 等: 文件處理

## 常見問題

**Q: Qdrant 連接失敗？**
A: 確保 Qdrant 已啟動並監聽在 6333 埠號。

**Q: 支援哪些文件格式？**
A: PDF, Word (.docx, .doc), TXT, 圖片 (.jpg, .jpeg, .png), PowerPoint (.pptx, .ppt)

**Q: 如何使用 MCP Server？**
A: 選擇資料後啟動 MCP Server，使用顯示的指令連接，然後可以使用 `search_documents` 工具進行檢索。

## 授權

MIT License
