"""
MCP 客戶端測試腳本 - 測試 stdio 模式的 MCP Server
"""
import asyncio
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_server():
    """測試 MCP Server (stdio 模式)"""
    
    print("=" * 60)
    print("測試 Local RAG MCP Server (stdio 模式)")
    print("=" * 60)
    print()
    
    # 設定 server 參數
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py", "Advantech"],
        env=None
    )
    
    try:
        # 連接到 server
        print("正在連接到 MCP Server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化
                print("✓ 已連接到 MCP Server")
                print()
                
                # 測試 1: 列出可用工具
                print("-" * 60)
                print("測試 1: 列出可用工具")
                print("-" * 60)
                tools = await session.list_tools()
                print(f"找到 {len(tools.tools)} 個工具:")
                for tool in tools.tools:
                    print(f"  - {tool.name}: {tool.description}")
                print()
                
                # 測試 2: 列出資料來源
                print("-" * 60)
                print("測試 2: 列出資料來源")
                print("-" * 60)
                result = await session.call_tool("list_data_sources", arguments={})
                print("結果:")
                for content in result.content:
                    print(content.text)
                print()
                
                # 測試 3: 搜尋文件
                print("-" * 60)
                print("測試 3: 搜尋文件")
                print("-" * 60)
                query = "測試查詢"
                print(f"查詢: {query}")
                result = await session.call_tool(
                    "search_documents",
                    arguments={"query": query, "limit": 3}
                )
                print("結果:")
                for content in result.content:
                    print(content.text)
                print()
                
                print("=" * 60)
                print("✓ 所有測試完成")
                print("=" * 60)
                
    except Exception as e:
        print(f"\n✗ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    print("""
注意: 此測試會啟動一個新的 MCP Server 實例進行測試
如果已有 MCP Server 在運行，可能會遇到 Qdrant 並發問題
建議先停止其他 MCP Server 實例

按 Enter 繼續...
""")
    input()
    
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)
