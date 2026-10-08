from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/")
async def summarize_text(payload: dict):
    """Summarize text"""
    try:
        text = payload.get("text", "")
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text provided")

        # Simple mock summarization - in real implementation, use Summarizer
        # This returns a basic structure that the frontend expects
        if len(text) > 100:
            summary = text[:100] + "..."
        else:
            summary = text

        return {
            "summary_text": summary,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))