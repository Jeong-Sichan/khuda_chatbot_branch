import models
import uuid
import models

def save_message(db, session_id, role, content, parent_id=None):
    msg = models.Message(session_id=session_id, role=role, content=content, parent_id=parent_id)
    db.add(msg)
    db.flush()
    return msg

def get_history(db, session_id):
    """특정 대화방의 메시지를 시간순으로 전부 꺼낸다."""
    return (
        db.query(models.Message)
        .filter(models.Message.session_id == session_id)
        .order_by(models.Message.id)
        .all()
    )


def list_conversations(db):
    return (
        db.query(models.Conversation)
        .order_by(models.Conversation.created_at.desc())   # 최신 대화가 위로
        .all()
    )

def get_thread(db, leaf_id):
    chain = []
    msg = db.query(models.Message).filter(models.Message.id == leaf_id).first()
    while msg is not None:
        chain.append(msg)
        if msg.parent_id is None:
            break
        msg = db.query(models.Message).filter(models.Message.id == msg.parent_id).first()
    chain.reverse()
    return chain

def create_conversation(db, title="새 대화"):
    conv = models.Conversation(id=str(uuid.uuid4()), title=title)
    db.add(conv)
    main = models.Branch(id=str(uuid.uuid4()), session_id=conv.id, name="main", head_id=None)
    db.add(main)
    db.commit()
    return conv, main


def create_branch(db, session_id, from_message_id, name="새 가지"):
    branch = models.Branch(id=str(uuid.uuid4()), session_id=session_id,
                           name=name, head_id=from_message_id)
    db.add(branch)
    db.commit()
    return branch

def get_branch(db, branch_id):
    return db.query(models.Branch).filter(models.Branch.id == branch_id).first()

def list_branches(db, session_id):
    return db.query(models.Branch).filter(models.Branch.session_id == session_id).all()