from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from .rag_engine import MedicalRAGEngine

class AIService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, 
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3
        )
        self.rag = MedicalRAGEngine()

    async def get_response(self, query: str, maps_data: list, location: str):
        # Step 1: Process external maps data (RAG)
        context = self.rag.process_maps_data(maps_data)
        
        # Step 2: Build specific medical prompt
        system_msg = self.rag.get_system_prompt(context, location)

        
        
        extra_instruction = """
    Note: If the user explicitly asks to book, make an appointment, or pay, 
    include the tag [TRIGGER_BOOKING] at the end of your response.
    """

        # Step 3: Invoke LLM
        response = self.llm.invoke([
            ("system", system_msg + extra_instruction),
            ("human", query)
        ])
        return response.content
    
        ai_raw_content = response.content
    
    # ব্যাকএন্ড ডেভেলপারকে এই ফরম্যাটে ডাটা পাঠাতে পারেন
        data_to_frontend = {
        "text": ai_raw_content.split("[")[0].strip(), # শুধু কথাটুকু আলাদা করা
        "show_cards": "[SHOW_CARDS]" in ai_raw_content,
        "show_location_button": "[SHOW_BUTTON: detect_location]" in ai_raw_content
    }
        return data_to_frontend