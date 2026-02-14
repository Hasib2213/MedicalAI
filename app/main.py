from fastapi import FastAPI, HTTPException
from app.models.request_models import ChatRequest
from app.services.ai_service import AIService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Medical AI API")
ai_service = AIService()

# Enable CORS for frontend/backend integration
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = await ai_service.get_response(
            query=request.user_query,
            maps_data=request.maps_data,
            location=request.user_location
        )
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))