"""
Qdrant 向量資料庫操作模組
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Optional
import uuid
import config


# 全域 Qdrant 客戶端（避免重複建立）
_qdrant_client = None


def get_qdrant_client():
    """取得或建立 Qdrant 客戶端（單例模式）"""
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(path=config.QDRANT_PATH)
    return _qdrant_client


class VectorDatabase:
    def __init__(self):
        """初始化 Qdrant 客戶端 - 使用本地文件系統"""
        # 使用共用的客戶端
        self.client = get_qdrant_client()
        self._ensure_collection()
        
    def _ensure_collection(self):
        """確保 collection 存在，不存在則建立"""
        collections = self.client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if config.COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=config.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=config.VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )
            print(f"建立 collection: {config.COLLECTION_NAME}")
    
    def insert_documents(self, chunks: List[str], embeddings: List[List[float]], 
                        file_name: str, data_name: str) -> int:
        """
        插入文件分塊到資料庫
        
        Args:
            chunks: 文字分塊列表
            embeddings: 對應的嵌入向量列表
            file_name: 檔案名稱
            data_name: 資料名稱
            
        Returns:
            插入的點數量
        """
        points = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            point_id = str(uuid.uuid4())
            payload = {
                'text': chunk,
                'file_name': file_name,
                'data_name': data_name,
                'chunk_index': idx
            }
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            ))
        
        self.client.upsert(
            collection_name=config.COLLECTION_NAME,
            points=points
        )
        
        return len(points)
    
    def search(self, query_vector: List[float], data_names: Optional[List[str]] = None, 
               limit: int = 5) -> List[Dict]:
        """
        向量相似度搜尋
        
        Args:
            query_vector: 查詢向量
            data_names: 要搜尋的資料名稱列表（None 表示搜尋全部）
            limit: 返回結果數量
            
        Returns:
            搜尋結果列表
        """
        search_params = {
            'collection_name': config.COLLECTION_NAME,
            'query_vector': query_vector,
            'limit': limit
        }
        
        # 如果指定了資料名稱，添加過濾條件
        if data_names:
            search_params['query_filter'] = Filter(
                must=[
                    FieldCondition(
                        key='data_name',
                        match=MatchValue(value=name)
                    ) for name in data_names
                ]
            )
        
        results = self.client.search(**search_params)
        
        return [
            {
                'score': result.score,
                'text': result.payload['text'],
                'file_name': result.payload['file_name'],
                'data_name': result.payload['data_name'],
                'chunk_index': result.payload['chunk_index']
            }
            for result in results
        ]
    
    def get_all_data_names(self) -> List[str]:
        """
        取得所有資料名稱
        
        Returns:
            資料名稱列表（去重）
        """
        # 使用 scroll 取得所有點
        scroll_result = self.client.scroll(
            collection_name=config.COLLECTION_NAME,
            limit=1000,  # 每次取得的數量
            with_payload=True,
            with_vectors=False
        )
        
        data_names = set()
        for point in scroll_result[0]:
            if 'data_name' in point.payload:
                data_names.add(point.payload['data_name'])
        
        return sorted(list(data_names))
    
    def delete_by_data_name(self, data_name: str) -> int:
        """
        刪除指定資料名稱的所有文件
        
        Args:
            data_name: 資料名稱
            
        Returns:
            刪除的點數量
        """
        # 先搜尋要刪除的點
        scroll_result = self.client.scroll(
            collection_name=config.COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key='data_name',
                        match=MatchValue(value=data_name)
                    )
                ]
            ),
            limit=1000,
            with_payload=False,
            with_vectors=False
        )
        
        point_ids = [point.id for point in scroll_result[0]]
        
        if point_ids:
            self.client.delete(
                collection_name=config.COLLECTION_NAME,
                points_selector=point_ids
            )
        
        return len(point_ids)
    
    def get_stats(self) -> Dict:
        """
        取得資料庫統計資訊
        
        Returns:
            統計資訊字典
        """
        collection_info = self.client.get_collection(config.COLLECTION_NAME)
        return {
            'total_points': collection_info.points_count,
            'vector_size': collection_info.config.params.vectors.size,
            'data_names_count': len(self.get_all_data_names())
        }
