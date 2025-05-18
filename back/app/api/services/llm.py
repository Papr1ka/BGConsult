# api/services/llm.py
from back.app.api.services.qdrant import qdrant
from pathlib import Path
from huggingface_hub import InferenceClient
from loguru import logger
from back.config import config

class LLMService:
    def __init__(self):
        self.qdb = qdrant
        self.model_name = "mistralai/Mistral-Nemo-Instruct-2407"
        self.client = InferenceClient(token=config.hf_token, provider="hf-inference")
    
    def check_health(self):
        logger.debug("LLM: OK")

    def answer(self, query, game) -> str:
        context = self.qdb.get_relevant_context(query)

        prompt = f"""Ты - помощник. Твоя задача - отвечать на вопросы по настольной игре "{game}". На все вопросы не по игре ты отказываешься отвечать (даже при наличии цитаты из правил). Для ответа на вопрос можно использовать цитату из официальных правил. Если цитата уже полностью раскрывает ответ, не пиши ничего от себя.
        ЦИТАТА ИЗ ПРАВИЛ: {context}
        Вопрос: {query}\n
        Ответ: """

        parameters = {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
        try:
            response = self.client.text_generation(prompt, model=self.model_name, **parameters) + f"\n\nContex:\n{context}"
        except Exception as e:
            response = f"\n\nContex:\n<blockquote>{context}</blockquote>"

        return response
    
llm = LLMService()