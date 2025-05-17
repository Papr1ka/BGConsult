# api/services/llm.py
from back.app.api.services.qdrant import QdrantService
from pathlib import Path
from huggingface_hub import InferenceClient
from loguru import logger
from back.config import config

class LLMService:
    def __init__(self):
        self.qdb = QdrantService()
        self.model_name = "mistralai/Mistral-Nemo-Instruct-2407"
        self.client = InferenceClient(token=config.hf_token, provider="hf-inference")
    
    def check_health(self):
        logger.debug("LLM: OK")

    def answer(self, query, game):
        context = ""

        prompt = f"""Ты - помощник. Твоя задача - отвечать на вопросы по настольной игре "{game}". На все вопросы не по этой теме отказывайся отвечать.\n
        Вопрос: {query}\n
        Ответ:"""

        parameters = {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }

        response = self.client.text_generation(prompt, model=self.model_name, **parameters)
        return response
    
llm = LLMService()