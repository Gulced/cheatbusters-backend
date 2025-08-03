from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List

from app.utils.config import GOOGLE_API_KEY

class EmbeddingService:
    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        try:
            return self.embedding_model.embed_documents(texts)
        except Exception as e:
            print(f"Hata: Embedding oluşturulamadı - {e}")
            return []

embedding_service = EmbeddingService()