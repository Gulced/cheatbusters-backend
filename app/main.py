from fastapi import FastAPI
from app.routes import match
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CheatBuster API",
    description="Flutter tabanlı CheatBuster uygulaması için kopya tespiti yapan backend servisi.",
    version="1.0.0"
)

# CORS (Cross-Origin Resource Sharing) ayarları
# Flutter uygulamanızın API'ye erişebilmesi için gereklidir.
origins = [
    "http://localhost",
    "http://localhost:8080", # Flutter web development sunucusu varsayılanı
    # Buraya deploy ettiğiniz Flutter web uygulamasının adresini ekleyebilirsiniz
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotaları uygulamaya dahil et
app.include_router(match.router, prefix="/api/v1", tags=["Analysis"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "CheatBuster API'sine hoş geldiniz! Test için /docs adresine gidin."}