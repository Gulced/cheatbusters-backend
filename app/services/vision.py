from PIL import Image
import google.generativeai as genai
import io

from app.utils.config import GOOGLE_API_KEY, GEMINI_VISION_MODEL

genai.configure(api_key=GOOGLE_API_KEY)

class VisionService:
    def __init__(self):
        # v1beta ile ilgili tüm kodlar kaldırıldı.
        self.model = genai.GenerativeModel(GEMINI_VISION_MODEL)

    def get_text_from_image(self, image_bytes: bytes) -> str:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            prompt = "Bu bir sınav kağıdıdır. Üzerindeki tüm metinleri olduğu gibi, yorum eklemeden çıkar."
            response = self.model.generate_content([prompt, img], request_options={"timeout": 120})
            return response.text
        except Exception as e:
            print(f"Hata: Görsel metne çevrilemedi - {e}")
            return ""

vision_service = VisionService()