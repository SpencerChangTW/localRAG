"""
快速啟動腳本 - 用於啟動 Qdrant 和檢查環境
"""
import subprocess
import sys
import time
import socket


def check_port(host, port):
    """檢查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def check_qdrant():
    """檢查 Qdrant 本地儲存路徑"""
    print("檢查 Qdrant 本地儲存...")
    
    import config
    
    if os.path.exists(config.QDRANT_PATH):
        print(f"✓ Qdrant 資料目錄已存在: {config.QDRANT_PATH}")
    else:
        print(f"○ Qdrant 資料目錄將自動建立: {config.QDRANT_PATH}")
    
    return True  # 本地模式總是可用


def check_dependencies():
    """檢查 Python 依賴"""
    print("\n檢查 Python 依賴...")
    required_packages = [
        'markitdown',
        'qdrant_client',
        'sentence_transformers',
        'mcp',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} 未安裝")
            missing.append(package)
    
    if missing:
        print(f"\n請安裝缺少的套件:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    return True


def main():
    """主函數"""
    print("=" * 60)
    print("Local RAG 系統環境檢查")
    print("=" * 60)
    
    # 檢查依賴
    deps_ok = check_dependencies()
    
    # 檢查 Qdrant 路徑
    qdrant_ok = check_qdrant()
    
    print("\n" + "=" * 60)
    print("環境檢查結果:")
    print("=" * 60)
    print(f"Python 依賴: {'✓ 正常' if deps_ok else '✗ 缺少套件'}")
    print(f"Qdrant:     {'✓ 就緒' if qdrant_ok else '✗ 錯誤'}")
    print("=" * 60)
    
    if deps_ok and qdrant_ok:
        print("\n✓ 環境準備完成，可以執行:")
        print("  python main.py")
        print("\n註: 使用本地 Qdrant，資料存儲在 qdrant_data/ 目錄")
        return True
    else:
        print("\n✗ 環境未就緒，請解決上述問題")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
