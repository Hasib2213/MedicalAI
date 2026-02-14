from pydantic import BaseModel
from typing import List, Optional, Any

class ChatRequest(BaseModel):
    user_query: str
    maps_data: Optional[List[Any]] = [] # ম্যাপ থেকে পাওয়া ক্লিনিক্যাল ডাটা
    user_location: Optional[str] = "Unknown" # ম্যানুয়াল বা ডিটেক্ট করা লোকেশন