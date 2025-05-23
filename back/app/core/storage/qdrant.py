import os

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.http.models import PointStruct, VectorParams
import time
from sentence_transformers import SentenceTransformer
from loguru import logger
from back.app.core.config import get_settings
from back.app.core.storage.postgres import get_db

from back.app.utils.pdf import find_intervals, extract_documents_from_pdf, PDF_DIRECTORY, prepare_data_for_qdrant



class QdrantService():
    def __init__(self):
        self.qdrant_client = self.connect_to_qdrant()

        self.pg = get_db()

        self.embedder = SentenceTransformer("intfloat/multilingual-e5-base", token=get_settings().hf_token)

        for pdf_file in os.listdir(PDF_DIRECTORY):
            if pdf_file.endswith('.pdf'):
                self.refresh_qdrant(pdf_file)
                logger.debug(f"pdf_file : {pdf_file}")
                self.upload_to_qdrant(pdf_file)


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
                client = QdrantClient("qdrant", port=6333)
                client.get_collections()  # Проверка подключения
                logger.debug("Qdrant connected")
                return client
            except ResponseHandlingException:
                if attempt < max_attempts - 1:
                    time.sleep(delay)
                else:
                    raise


    def create_qdrant_collection(self, collection_name):
        """
        Создает коллекцию 'documents' в Qdrant, если она еще не существует.

        Raises:
            Exception: Если не удается получить информацию о коллекции.
        """
        logger.debug("Create collection...")
        try:
            self.qdrant_client.get_collection(collection_name)
        except Exception:
            self.qdrant_client.create_collection(
                collection_name,
                vectors_config=VectorParams(size=768, distance="Cosine")
            )
        logger.debug(f"Collection {collection_name} created")



    def upload_to_qdrant(self, pdf_file):
        """
        Загружает данные в коллекцию Qdrant, создавая эмбеддинги для каждого текста.

        Args:
            data (list[dict]): Список словарей с данными для загрузки.
            collection_name (str): Название коллекции для загрузки данных (по умолчанию 'default').
        """
        logger.debug(f"generating chunks...")
        chunks = extract_documents_from_pdf(pdf_file)

        logger.debug(f"formating chunks...")
        data = prepare_data_for_qdrant(chunks, 512)

        logger.debug(f"saving chunks... len {len(data)}")

        points = []
        collection_info = self.qdrant_client.get_collection(pdf_file)
        cur_id = collection_info.points_count + 1
        for item in data:
            text = item['text']
            vector = self.embedder.encode(text).tolist()
            payload = {"text": text, "metadata": {"link": item["link"], "title": item["title"],
                                                  "filename": item["filename"]}}  # Метаданные

            points.append(PointStruct(
                id=cur_id,
                vector=vector,
                payload=payload
            ))
            cur_id += 1
        logger.debug(f"Uploaded {len(data)} documents to Qdrant")
        self.qdrant_client.upsert(collection_name=pdf_file, points=points)


    def get_relevant_context(self, query: str, collection_name: str):
        """
        Осуществляет поиск в Qdrant чанков, соответствующих запросу.
        Args:
            query (str): Вопрос пользователя.
        """


        query_vector = self.embedder.encode([query])[0]
        resp = self.qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=5,
        )
        search_idx = [point.id for point in resp]
        context_idx = find_intervals(search_idx)
        context_points = [self.qdrant_client.retrieve(collection_name, range(group[0], group[1] + 1)) for group in context_idx]

        logger.info(f"search_idx {search_idx}\n\ncontext_idx {context_idx}\n\n context_points{context_points}")
        context = ""
        for group_points in context_points:
            context += f" Название документа: {group_points[0].payload['metadata']['filename']}\n"
            context += f" Заголовок: {group_points[0].payload['metadata']['title']}\n"
            context += " ".join([point.payload["text"].strip() for point in group_points])

        return context

    def refresh_qdrant(self, collection_name):
        """
        Очищает коллекцию 'documents' в Qdrant и создаёт её заново.
        """

        self.qdrant_client.delete_collection(collection_name=collection_name)
        self.create_qdrant_collection(collection_name)
        pass

qdrant = QdrantService()