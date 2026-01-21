"""
Local RAG 系統主程式
"""
import sys
import os

# 確保可以導入本地模組
sys.path.insert(0, os.path.dirname(__file__))

from gui_app import main as gui_main


if __name__ == "__main__":
    print("啟動 Local RAG 系統...")
    print("使用本地 Qdrant 資料庫，資料存儲在 qdrant_data/ 目錄")
    gui_main()
