"""
測試腳本 - 驗證各模組功能
"""
import os
import sys


def test_imports():
    """測試所有模組是否可以正常導入"""
    print("測試模組導入...")
    
    try:
        import config
        print("✓ config.py")
        
        from document_processor import DocumentProcessor
        print("✓ document_processor.py")
        
        from vector_db import VectorDatabase
        print("✓ vector_db.py")
        
        # MCP Server 需要在執行時測試
        print("✓ mcp_server.py (跳過導入測試)")
        
        return True
        
    except Exception as e:
        print(f"✗ 導入失敗: {e}")
        return False


def test_document_processor():
    """測試文件處理器"""
    print("\n測試文件處理器...")
    
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        print("✓ DocumentProcessor 初始化成功")
        
        # 測試文字分塊
        test_text = "這是一個測試文字。" * 100
        chunks = processor.chunk_text(test_text, chunk_size=100, overlap=10)
        print(f"✓ 文字分塊功能正常 (生成 {len(chunks)} 個分塊)")
        
        # 測試嵌入
        test_chunks = ["這是測試文字1", "這是測試文字2"]
        embeddings = processor.embed_text(test_chunks)
        print(f"✓ 嵌入功能正常 (向量維度: {len(embeddings[0])})")
        
        return True
        
    except Exception as e:
        print(f"✗ 文件處理器測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_vector_db():
    """測試向量資料庫連接"""
    print("\n測試向量資料庫...")
    
    try:
        from vector_db import VectorDatabase
        
        db = VectorDatabase()
        print("✓ VectorDatabase 初始化成功")
        
        # 測試取得統計
        stats = db.get_stats()
        print(f"✓ 資料庫統計: {stats}")
        
        # 測試取得資料名稱
        data_names = db.get_all_data_names()
        print(f"✓ 現有資料名稱: {data_names}")
        
        return True
        
    except Exception as e:
        print(f"✗ 向量資料庫測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """測試配置"""
    print("\n測試配置...")
    
    try:
        import config
        
        print(f"✓ Qdrant 路徑: {config.QDRANT_PATH}")
        print(f"✓ Collection: {config.COLLECTION_NAME}")
        print(f"✓ 嵌入模型: {config.EMBEDDING_MODEL}")
        print(f"✓ 向量維度: {config.VECTOR_SIZE}")
        print(f"✓ 支援格式: {list(config.SUPPORTED_EXTENSIONS.keys())}")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置測試失敗: {e}")
        return False


def main():
    """執行所有測試"""
    print("=" * 60)
    print("Local RAG 系統模組測試")
    print("=" * 60)
    
    results = []
    
    # 測試配置
    results.append(("配置", test_config()))
    
    # 測試導入
    results.append(("模組導入", test_imports()))
    
    # 測試文件處理器
    results.append(("文件處理器", test_document_processor()))
    
    # 測試向量資料庫
    results.append(("向量資料庫", test_vector_db()))
    
    # 總結
    print("\n" + "=" * 60)
    print("測試結果:")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"{name:20s} {status}")
    
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ 所有測試通過！")
        print("\n可以執行 GUI 應用程式:")
        print("  python main.py")
    else:
        print("\n✗ 部分測試失敗，請檢查錯誤訊息")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
