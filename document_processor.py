"""
文件處理模組 - 使用 Markitdown 轉換文件並進行向量化
"""
from markitdown import MarkItDown
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict
import config


class DocumentProcessor:
    def __init__(self):
        """初始化文件處理器"""
        self.markitdown = MarkItDown()
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        
    def convert_to_markdown(self, file_path: str) -> str:
        """
        使用 Markitdown 轉換文件為 Markdown
        
        Args:
            file_path: 文件路徑
            
        Returns:
            轉換後的 Markdown 文字
        """
        try:
            result = self.markitdown.convert(file_path)
            return result.text_content
        except Exception as e:
            raise Exception(f"文件轉換失敗: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """
        將文字分塊處理
        
        Args:
            text: 輸入文字
            chunk_size: 每塊大小
            overlap: 重疊大小
            
        Returns:
            文字分塊列表
        """
        if chunk_size is None:
            chunk_size = config.CHUNK_SIZE
        if overlap is None:
            overlap = config.CHUNK_OVERLAP
            
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            if chunk.strip():  # 只加入非空白的分塊
                chunks.append(chunk)
            start = end - overlap
            
        return chunks
    
    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        將文字轉換為嵌入向量
        
        Args:
            texts: 文字列表
            
        Returns:
            嵌入向量列表
        """
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    
    def process_document(self, file_path: str, data_name: str) -> Dict:
        """
        處理文件：轉換、分塊、嵌入
        
        Args:
            file_path: 文件路徑
            data_name: 資料名稱
            
        Returns:
            包含文件資訊、分塊和嵌入的字典
        """
        # 轉換為 Markdown
        markdown_text = self.convert_to_markdown(file_path)
        
        # 文字分塊
        chunks = self.chunk_text(markdown_text)
        
        # 生成嵌入向量
        embeddings = self.embed_text(chunks)
        
        # 準備返回資料
        return {
            'file_name': os.path.basename(file_path),
            'data_name': data_name,
            'markdown_text': markdown_text,
            'chunks': chunks,
            'embeddings': embeddings
        }
    
    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        """
        檢查檔案格式是否支援
        
        Args:
            file_path: 文件路徑
            
        Returns:
            是否支援
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in config.SUPPORTED_EXTENSIONS
