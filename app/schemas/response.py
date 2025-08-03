from pydantic import BaseModel
from typing import List, Optional

class DetailedAnalysis(BaseModel):
    is_cheating: bool
    reason: str
    suspicious_parts: List[str]

class CheatingReport(BaseModel):
    students: List[str]
    similarity_score: float
    analysis: DetailedAnalysis

class AnalysisResponse(BaseModel):
    total_documents_processed: int
    cheating_pairs_found: int
    report: List[CheatingReport]
    error: Optional[str] = None