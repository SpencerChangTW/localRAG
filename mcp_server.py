"""
Local RAG MCP Server - 參考 Microsoft MarkItDown 實作
支援 stdio 和 HTTP/SSE 雙模式
"""
import contextlib
import sys
import os
import argparse
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.types import Receive, Scope, Send
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
import uvicorn
from typing import List, Optional

import config


# 全域變數用於儲存選定的資料和實例
_selected_data_names: List[str] = []
_processor = None
_vector_db = None


# 初始化 FastMCP server
mcp = FastMCP("local-rag")


def initialize_server(selected_data_names: List[str],
                     processor=None,
                     vector_db=None):
    """
    初始化 MCP Server 的資料
    
    Args:
        selected_data_names: 資料名稱列表
        processor: 文件處理器實例（可選）
        vector_db: 向量資料庫實例（可選）
    """
    global _selected_data_names, _processor, _vector_db
    
    _selected_data_names = selected_data_names
    
    if processor is not None:
        _processor = processor
    else:
        from document_processor import DocumentProcessor
        _processor = DocumentProcessor()
        
    if vector_db is not None:
        _vector_db = vector_db
    else:
        from vector_db import VectorDatabase
        _vector_db = VectorDatabase()


@mcp.tool()
async def search_documents(query: str, limit: int = 5) -> str:
    """
    在選定的文件資料中進行語義搜尋
    
    Args:
        query: 要搜尋的查詢文字
        limit: 返回結果數量（預設5，最大20）
    
    Returns:
        Markdown 格式的搜尋結果
    """
    if not query:
        return "錯誤: 查詢文字不能為空"
    
    print(f"搜尋查詢: {query}\n\n")
    
    # 驗證 limit
    limit = max(1, min(20, limit))
    print(f"搜尋 limit: {limit}\n\n")
    
    try:
        # 生成查詢向量
        query_embedding = _processor.embed_text([query])[0]
        print(f"搜尋 query_embedding 維度: {len(query_embedding)}\n\n")
        
        # 在選定的資料名稱中搜尋
        results = _vector_db.search(
            query_vector=query_embedding,
            data_names=_selected_data_names if _selected_data_names else None,
            limit=limit
        )
        print(f"搜尋 result 數量: {len(results)}\n\n")
        # 格式化為 Markdown
        if not results:
            markdown = f"# 搜尋結果\n\n未找到與「{query}」相關的文件。\n"
        else:
            markdown = f"# 搜尋結果：{query}\n\n"
            markdown += f"找到 {len(results)} 個相關結果\n\n"
            markdown += "---\n\n"
            
            for idx, result in enumerate(results, 1):
                markdown += f"## {idx}. {result['file_name']}\n\n"
                markdown += f"**資料來源**: {result['data_name']}\n\n"
                markdown += f"**相關度分數**: {result['score']:.4f}\n\n"
                markdown += f"### 內容摘要\n\n"
                markdown += f"{result['text']}\n\n"
                markdown += "---\n\n"
        
        print(markdown)
        return markdown
        
    except Exception as e:
        return f"搜尋錯誤: {str(e)}"


@mcp.tool()
async def list_data_sources() -> str:
    """
    列出目前 MCP Server 可檢索的資料來源名稱
    
    Returns:
        Markdown 格式的資料來源列表
    """
    markdown = "# 可檢索的資料來源\n\n"
    
    if not _selected_data_names:
        markdown += "目前沒有可用的資料來源。\n"
    else:
        markdown += f"本 MCP Server 提供以下 {len(_selected_data_names)} 個資料來源:\n\n"
        for name in _selected_data_names:
            markdown += f"- **{name}**\n"
    
    return markdown


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """
    建立 Starlette 應用程式，支援 SSE 和 StreamableHTTP
    
    Args:
        mcp_server: MCP Server 實例
        debug: 除錯模式
    
    Returns:
        Starlette 應用程式
    """
    sse = SseServerTransport("/messages/")
    session_manager = StreamableHTTPSessionManager(
        app=mcp_server,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    async def handle_sse(request: Request) -> None:
        """處理 SSE 連接"""
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        """處理 StreamableHTTP 請求"""
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """應用程式生命週期管理"""
        async with session_manager.run():
            print("Local RAG MCP Server 已啟動 (HTTP/SSE 模式)!", file=sys.stderr)
            print(f"資料來源: {', '.join(_selected_data_names)}", file=sys.stderr)
            try:
                yield
            finally:
                print("Server 正在關閉...", file=sys.stderr)

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/mcp", app=handle_streamable_http),
            Mount("/messages/", app=sse.handle_post_message),
        ],
        lifespan=lifespan,
    )


def main():
    """主程式入口"""
    parser = argparse.ArgumentParser(
        description="Local RAG MCP Server - 提供本地文件檢索服務"
    )
    
    parser.add_argument(
        "data_names",
        nargs="+",
        help="要提供檢索服務的資料名稱（至少一個）"
    )
    
    parser.add_argument(
        "--http",
        action="store_true",
        help="使用 HTTP/SSE 模式（預設: stdio 模式）"
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP 模式的主機位址（預設: 127.0.0.1）"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=3001,
        help="HTTP 模式的埠號（預設: 3001）"
    )
    
    args = parser.parse_args()
    
    # 初始化 server 資料
    initialize_server(args.data_names)
    
    # 取得 MCP server 實例
    mcp_server = mcp._mcp_server
    
    if args.http:
        # HTTP/SSE 模式
        print(f"啟動 Local RAG MCP Server (HTTP/SSE 模式)", file=sys.stderr)
        print(f"URL: http://{args.host}:{args.port}/mcp", file=sys.stderr)
        print(f"SSE: http://{args.host}:{args.port}/sse", file=sys.stderr)
        print(f"資料來源: {', '.join(args.data_names)}", file=sys.stderr)
        
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=args.host,
            port=args.port,
        )
    else:
        # stdio 模式（預設）
        print(f"啟動 Local RAG MCP Server (stdio 模式)", file=sys.stderr)
        print(f"資料來源: {', '.join(args.data_names)}", file=sys.stderr)
        print("等待 MCP 客戶端連接...", file=sys.stderr)
        
        mcp.run()


if __name__ == "__main__":
    main()
