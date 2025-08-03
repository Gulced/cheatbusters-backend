from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import List

from app.services.analyze import analyze_service
from app.schemas.response import AnalysisResponse

router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Sınav Kağıtlarında Kopya Tespiti",
    description="Birden fazla sınav kağıdı görseli yükleyerek aralarındaki kopya olasılığını analiz eder."
)
async def analyze_exams_endpoint(files: List[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Analiz için en az 2 dosya gereklidir.")

    image_files = []
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Desteklenmeyen dosya: {file.filename}")

        content = await file.read()
        image_files.append({"filename": file.filename, "content": content})

    try:
        result = analyze_service.analyze_documents(image_files)
        if result.get("error"):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, result["error"])
        return AnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Beklenmedik bir sunucu hatası oluştu: {e}")