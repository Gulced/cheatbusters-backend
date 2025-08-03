from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

from app.services.vision import vision_service
from app.services.embedding import embedding_service
from app.services.compare import compare_service


class AnalyzeService:
    def _process_image(self, image_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tek bir görseli işler ve metnini çıkarır.
        image_data şunları içerir:
        {
            "student_name": "Ali Özdemir",
            "content": base64_string
        }
        """
        text = vision_service.get_text_from_image(image_data["content"])
        return {
            "student_name": image_data["student_name"],
            "text": text
        }

    def analyze_documents(self, image_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        OCR ➝ Embedding ➝ Cosine Similarity ➝ Gemini Detaylı Analiz
        """
        if len(image_files) < 2:
            return {"error": "Lütfen en az 2 doküman yükleyin."}

        # 1. OCR
        with ThreadPoolExecutor() as executor:
            ocr_results = list(executor.map(self._process_image, image_files))

        valid_results = [res for res in ocr_results if res["text"]]
        if len(valid_results) < 2:
            return {"error": "Görsellerin en az ikisinden metin çıkarılamadı."}

        names = [res["student_name"] for res in valid_results]
        texts = [res["text"] for res in valid_results]
        text_map = dict(zip(names, texts))

        # 2. Embedding
        embeddings = embedding_service.get_embeddings(texts)
        if not embeddings:
            return {"error": "Metinlerden embedding vektörleri oluşturulamadı."}

        # 3. Cosine Similarity + Threshold filtrelemesi
        similar_pairs = compare_service.find_similar_pairs(embeddings, names)

        # 4. Gemini ile detaylı analiz
        final_report = []
        for pair in similar_pairs:
            student_pair = pair["students"]
            similarity = round(pair["similarity"] * 100, 2)  # yüzdelik

            analysis = compare_service.detailed_cheat_analysis(
                text_map[student_pair[0]],
                text_map[student_pair[1]]
            )

            final_report.append({
                "students": student_pair,
                "similarity_score": similarity,
                "analysis": analysis
            })

        cheating_pairs = [r for r in final_report if r["analysis"].get("is_cheating")]

        return {
            "total_documents_processed": len(valid_results),
            "cheating_pairs_found": len(cheating_pairs),
            "report": final_report
        }


analyze_service = AnalyzeService()
