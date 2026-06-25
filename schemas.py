from pydantic import BaseModel

class ChatRequest(BaseModel):
    branch_id: str
    message: str

class CreateSessionRequest(BaseModel):
    title: str = "새 대화"  

class SessionOut(BaseModel):
    id: str
    title: str
    main_branch_id: str

class ChatResponse(BaseModel):
    reply: str

class MessageOut(BaseModel):
    role: str
    content: str
    created_at: str

    model_config = {"from_attributes": True}   

class ConversationOut(BaseModel):
    id: str
    title: str
    created_at: str

    model_config = {"from_attributes": True}

class BranchOut(BaseModel):
    id: str
    name: str
    head_id: int | None
    model_config = {"from_attributes": True}

class CreateBranchRequest(BaseModel):
    session_id: str
    from_message_id: int   # 이 메시지 지점에서 분기
    name: str = "새 가지"