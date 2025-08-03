import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY":
    raise ValueError("GOOGLE_API_KEY ortam değişkeni bulunamadı veya ayarlanmamış. Lütfen .env dosyasını kontrol edin.")

# Model adlarının doğru formatı "models/" önekiyle başlar.
GEMINI_VISION_MODEL = "models/gemini-2.0-flash"
GEMINI_TEXT_MODEL = "models/gemini-2.0-flash"
SIMILARITY_THRESHOLD = 0.8