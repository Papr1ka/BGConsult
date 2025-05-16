"""from fastapi import APIRouter
from back.app.api.services.qdrant import QdrantService
from back.app.api.services.llm import LLMService
from back.app.models.schemas import RAGQuery, RAGResponse

router = APIRouter(tags=["rag"])


@router.post("/query", response_model=RAGResponse)
async def rag_query(query: RAGQuery):
    return {"answer": 123}

    context = await QdrantService.search(query.text)
    answer = await LLMService.generate(query.text, context)
    return {"answer": answer}"""