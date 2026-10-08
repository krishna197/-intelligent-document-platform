from fastapi import APIRouter
from .documents import router as documents_router
from .ner import router as ner_router
from .summarization import router as summarization_router
from .rag import router as rag_router

api_router = APIRouter()

api_router.include_router(documents_router)
api_router.include_router(ner_router)
api_router.include_router(summarization_router)
api_router.include_router(rag_router)