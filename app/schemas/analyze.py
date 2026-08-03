from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


class AnalyzeResponse(BaseModel):
    ats_score: int
    summary: str
    matched_skills: list[str]
    missing_skills: list[str]
    suggestions: list[str]
    interview_questions: list[str]