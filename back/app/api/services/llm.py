# api/services/llm.py
from openai import AsyncOpenAI
from back.app.core.config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

class LLMService:
    @classmethod
    async def generate(cls, query: str, context: list[str]) -> str:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Query: {query}\nContext: {context}"}
            ]
        )
        return response.choices[0].message.content