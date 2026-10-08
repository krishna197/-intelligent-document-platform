from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/extract")
async def extract_entities(payload: dict):
    """Extract named entities from text"""
    try:
        text = payload.get("text", "")
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text provided")

        # Simple mock NER response - in real implementation, use NERExtractor
        # This returns a basic structure that the frontend expects
        mock_entities = [
            {"text": "Apple Inc.", "label": "ORG", "start": 0, "end": 10},
            {"text": "Steve Jobs", "label": "PERSON", "start": 20, "end": 32},
            {"text": "Cupertino", "label": "GPE", "start": 40, "end": 49},
            {"text": "April 1976", "label": "DATE", "start": 55, "end": 65}
        ]

        return {
            "entities": mock_entities,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))