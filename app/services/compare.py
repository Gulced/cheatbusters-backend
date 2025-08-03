import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import google.generativeai as genai
import json

from app.utils.config import GOOGLE_API_KEY, GEMINI_TEXT_MODEL, SIMILARITY_THRESHOLD

genai.configure(api_key=GOOGLE_API_KEY)

class CompareService:
    def __init__(self):
        # v1beta ile ilgili tüm kodlar kaldırıldı.
        self.model = genai.GenerativeModel(GEMINI_TEXT_MODEL)

    def find_similar_pairs(self, embeddings: List[List[float]], filenames: List[str]) -> List[Dict[str, Any]]:
        if len(embeddings) < 2: return []
        similarity_matrix = cosine_similarity(np.array(embeddings))
        pairs = []
        for i in range(len(filenames)):
            for j in range(i + 1, len(filenames)):
                if similarity_matrix[i][j] >= SIMILARITY_THRESHOLD:
                    pairs.append({
                        "students": [filenames[i], filenames[j]],
                        "similarity": float(similarity_matrix[i][j])
                    })
        return pairs

    def detailed_cheat_analysis(self, text1: str, text2: str) -> Dict[str, Any]:
        prompt = f"""
        Aşağıdaki iki metni akademik kopya açısından analiz et. Cevabını yalnızca JSON formatında şu anahtarlarla ver:
        "is_cheating": (boolean) Kopya varsa true, yoksa false.
        "reason": (string) Neden kopya olduğunu veya olmadığını açıklayan kısa gerekçe.
        "suspicious_parts": (list of strings) Kopya şüphesi uyandıran veya aynı olan ifadelerin listesi.

        Metin 1:\n---\n{text1}\n---\n\nMetin 2:\n---\n{text2}\n---
        """
        try:
            response = self.model.generate_content(prompt, request_options={"timeout": 180})
            json_text = response.text.strip().lstrip("```json").rstrip("```").strip()
            return json.loads(json_text)
        except Exception as e:
            print(f"Hata: Gemini detaylı analiz - {e}")
            return {"is_cheating": False, "reason": "Analiz sırasında bir hata oluştu.", "suspicious_parts": []}

compare_service = CompareService()