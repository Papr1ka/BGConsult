from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.http.models import PointStruct, VectorParams
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client.http.models import SearchRequest, Filter, FieldCondition, MatchValue
import numpy as np
import time
from sentence_transformers import SentenceTransformer
from loguru import logger
from huggingface_hub import login
from back.config import config
import uuid

class QdrantService():
    def __init__(self):
        self.qdrant_client = self.connect_to_qdrant()
        
        self.refresh_qdrant()

        self.embedder = SentenceTransformer("intfloat/multilingual-e5-base", token=config.hf_token)

        self.upload_to_qdrant("manchkin_chunks.txt")

        logger.info("RAG is ready")


    def connect_to_qdrant(self, max_attempts=5, delay=5):
        """
        Подключается к серверу Qdrant с заданным количеством попыток и задержкой.

        Args:
            max_attempts (int): Максимальное количество попыток подключения.
            delay (int): Задержка между попытками подключения в секундах.

        Returns:
            QdrantClient: Подключенный клиент Qdrant.

        Raises:
            ResponseHandlingException: Если не удается подключиться после максимального количества попыток.
        """
        for attempt in range(max_attempts):
            logger.debug(f"Connecting to Qdrant, attempt {attempt + 1}")
            try:
                client = QdrantClient("qdrant", port=6334, prefer_grpc=True)
                client.get_collections()  # Проверка подключения
                logger.debug("Qdrant connected")
                return client
            except ResponseHandlingException:
                if attempt < max_attempts - 1:
                    time.sleep(delay)
                else:
                    raise


    def create_qdrant_collection(self):
        """
        Создает коллекцию 'documents' в Qdrant, если она еще не существует.

        Raises:
            Exception: Если не удается получить информацию о коллекции.
        """
        logger.debug("Create collection...")
        try:
            self.qdrant_client.get_collection("documents")
            logger.debug("Collection already exists")
        except Exception:
            self.qdrant_client.create_collection(
                "documents",
                vectors_config=VectorParams(size=768, distance="Cosine")
            )
            logger.debug("Collection created")



    def upload_to_qdrant(self, file_name, collection_name='documents'):
        """
        Загружает данные в коллекцию Qdrant, создавая эмбеддинги для каждого текста.

        Args:
            data (list[dict]): Список словарей с данными для загрузки.
            collection_name (str): Название коллекции для загрузки данных (по умолчанию 'documents').
        """
        
        logger.debug("Load data to Qdrant")
        with open(f"/app/back/rules/{file_name}", "r", encoding="utf-8") as file:
            chunks = file.read().split("\n\n")

        points = []
        for i, chunk in enumerate(chunks):
            vector = self.embedder.encode("query: " + chunk).tolist()
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"game": file_name, "text_fragment": chunk}
            ))

            if (i + 1) % 10 == 0:
                logger.debug(f"{file_name}: {i + 1}/{len(chunks)}")

        self.qdrant_client.upsert(collection_name=collection_name, points=points)
        logger.debug("Dala loaded")


    def get_relevant_context(self, query: str):
        """
        Осуществляет поиск в Qdrant чанков, соответствующих запросу.
        Args:
            query (str): Вопрос пользователя.
        """


        query_vector = self.embedder.encode([query])[0]
        hits = self.qdrant_client.search(
            collection_name="documents",
            query_vector=query_vector,
            limit=1,
            with_payload=True,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="game",
                        match=MatchValue(value="manchkin_chunks.txt")
                    )
                ]
            )
        )
        context = "\n".join([hit.payload["text_fragment"] for hit in hits])
        return context

    def refresh_qdrant(self):
        """
        Очищает коллекцию 'documents' в Qdrant и создаёт её заново.
        """
        self.qdrant_client.delete_collection(collection_name="documents")
        self.create_qdrant_collection()

qdrant = QdrantService()