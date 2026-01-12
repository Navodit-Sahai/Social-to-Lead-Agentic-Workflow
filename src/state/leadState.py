from typing import Optional,TypedDict,List

class LeadState(TypedDict):
    user_query: str
    intent: Optional[str]
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    response:str
    chat_history: List[dict]
    lead_captured: Optional[bool]