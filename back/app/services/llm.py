from back.app.core.storage.qdrant import qdrant
from huggingface_hub import InferenceClient
from loguru import logger
from back.app.core.config import get_settings, games_info


class LLMService:
    def __init__(self):
        self.qdb = qdrant
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.3"
        logger.debug(get_settings().hf_token)
        self.client = InferenceClient(token=get_settings().hf_token, provider="hf-inference")
    
    def check_health(self):
        logger.debug("LLM: OK")

    def answer(self, query, game) -> str:
        context = self.qdb.get_relevant_context(query, game)
        logger.debug(f"LLM: Context: {context}")

        prompt = f"""Ты — строго ограниченный помощник по настольной игре "{game}". 
        Ты можешь использовать **только официальные правила** (цитата ниже) для ответа на вопрос. 
        Если в цитате нет информации для точного ответа — ты **отказываешься** отвечать.

        ⚠️ **Не пиши ничего от себя**, даже если тебе кажется, что ты знаешь ответ. 
        Не пытайся додумывать. Только отвечай на вопрос, если цитата это позволяет.

        ---

        📘 ЦИТАТА ИЗ ПРАВИЛ:
        {context}

        ❓ Вопрос:
        {query}

        💬 Ответ:
        """

        parameters = {
            "max_new_tokens": 256,
            "temperature": 0.1,
            "top_p": 0.9,
            "do_sample": False,
            "return_full_text": False
        }

        try:
            response = self.client.text_generation(prompt, model=self.model_name, **parameters)
        except Exception as e:
            logger.error(e)
            response = f"\n\nЦитата из официальных правил игры:\n<blockquote>{games_info[game].url}</blockquote>"

        logger.debug(f"len(response): {len(response)}\n\nresponse: {response}")
        return response
    
llm = LLMService()