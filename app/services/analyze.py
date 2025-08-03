from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

from app.services.vision import vision_service
from app.services.embedding import embedding_service
from app.services.compare import compare_service


class AnalyzeService:
    def _process_image(self, image_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tek bir görseli işler ve metnini çıkarır."""
        text = vision_service.get_text_from_image(image_data["content"])
        return {"filename": image_data["filename"], "text": text}

    def analyze_documents(self, image_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tüm süreci yönetir: OCR, Embedding, Filtreleme ve Detaylı Analiz."""
        if len(image_files) < 2:
            return {"error": "Lütfen en az 2 doküman yükleyin."}

        # 1. Aşama: OCR (Görselleri paralel işle)
        with ThreadPoolExecutor() as executor:
            ocr_results = list(executor.map(self._process_image, image_files))

        valid_results = [res for res in ocr_results if res["text"]]
        if len(valid_results) < 2:
            return {"error": "Görsellerin en az ikisinden metin çıkarılamadı."}

        filenames = [res["filename"] for res in valid_results]
        texts = [res["text"] for res in valid_results]
        text_map = dict(zip(filenames, texts))

        # 2. Aşama: Embedding
        embeddings = embedding_service.get_embeddings(texts)
        if not embeddings:
            return {"error": "Metinlerden embedding vektörleri oluşturulamadı."}

        # 3. Aşama: Benzerlik Filtrelemesi
        similar_pairs = compare_service.find_similar_pairs(embeddings, filenames)

        # 4. Aşama: Detaylı Analiz
        final_report = []
        for pair in similar_pairs:
            student_ids = pair["students"]
            analysis_result = compare_service.detailed_cheat_analysis(
                text_map[student_ids[0]],
                text_map[student_ids[1]]
            )
            if analysis_result.get("is_cheating"):
                final_report.append({
                    "students": student_ids,
                    "similarity_score": pair["similarity"],
                    "analysis": analysis_result
                })

        return {
            "total_documents_processed": len(valid_results),
            "cheating_pairs_found": len(final_report),
            "report": final_report
        }


analyze_service = AnalyzeService()