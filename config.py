"""
系統配置檔案
"""
import os

# Qdrant 設定 - 使用本地檔案系統
QDRANT_PATH = os.path.join(os.path.dirname(__file__), "qdrant_data")
COLLECTION_NAME = "documents"

# MCP Server HTTP 設定
MCP_SERVER_HOST = "127.0.0.1"
MCP_SERVER_PORT = 3001
MCP_SERVER_PATH = "/mcp"
MCP_SERVER_URL = f"http://{MCP_SERVER_HOST}:{MCP_SERVER_PORT}{MCP_SERVER_PATH}"

# 嵌入模型設定
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_SIZE = 384  # all-MiniLM-L6-v2 的向量維度

# 文字分塊參數
CHUNK_SIZE = 500  # 每個分塊的字元數
CHUNK_OVERLAP = 50  # 分塊重疊字元數

# 支援的檔案格式
SUPPORTED_EXTENSIONS = {
    '.pdf': 'PDF',
    '.docx': 'Word',
    '.doc': 'Word',
    '.txt': 'Text',
    '.jpg': 'Image',
    '.jpeg': 'Image',
    '.png': 'Image',
    '.pptx': 'PowerPoint',
    '.ppt': 'PowerPoint'
}

# 資料儲存路徑
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
