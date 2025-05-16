"""from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from back.app.core.config import QDRANT_URL, QDRANT_COLLECTION

model = SentenceTransformer("all-MiniLM-L6-v2")

class QdrantService:
    client = QdrantClient(QDRANT_URL)
    
    @classmethod
    async def search(cls, query: str, limit: int = 3) -> list[str]:
        embedding = model.encode(query).tolist()
        hits = cls.client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=embedding,
            limit=limit
        )
        return [hit.payload["text"] for hit in hits]"""