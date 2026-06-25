from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import service,repository
from schemas import ChatRequest, ChatResponse, MessageOut, ConversationOut, SessionOut, BranchOut, CreateBranchRequest, CreateSessionRequest
from database import get_db

router = APIRouter()   

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    answer = service.handle_chat(db, req)   
    return ChatResponse(reply=answer)

@router.get("/chat/history", response_model=list[MessageOut])
def history(session_id: str, db: Session = Depends(get_db)):
    import repository
    return repository.get_history(db, session_id)

# 세션 생성 
@router.post("/sessions", response_model=SessionOut)
def new_session(req: CreateSessionRequest, db: Session = Depends(get_db)):
    conv, main = repository.create_conversation(db, title=req.title)
    return SessionOut(id=conv.id, title=conv.title, main_branch_id=main.id)

@router.get("/sessions", response_model=list[ConversationOut])
def all_sessions(db: Session = Depends(get_db)):
    return repository.list_conversations(db)     # 사이드바용 대화 목록

# (2) 가지 만들기 (브랜치 버튼)
@router.post("/branches", response_model=BranchOut)
def make_branch(req: CreateBranchRequest, db: Session = Depends(get_db)):
    return repository.create_branch(db, req.session_id, req.from_message_id, req.name)

# (3) 한 세션의 가지 목록 (사이드바용)
@router.get("/sessions/{session_id}/branches", response_model=list[BranchOut])
def session_branches(session_id: str, db: Session = Depends(get_db)):
    return repository.list_branches(db, session_id)

# (4) 특정 가지의 현재 줄기 보기 (= 화면에 뜨는 대화) — 기존 /chat/history 대체
@router.get("/branches/{branch_id}/thread", response_model=list[MessageOut])
def branch_thread(branch_id: str, db: Session = Depends(get_db)):
    branch = repository.get_branch(db, branch_id)
    if branch.head_id is None:
        return []
    return repository.get_thread(db, branch.head_id)