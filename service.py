import os
from openai import OpenAI
from dotenv import load_dotenv

import repository

load_dotenv()              
client = OpenAI()          


SYSTEM_PROMPT = "너는 친절한 한국어 챗봇이야. 질문에 간결하고 정확하게 답해줘."

def generate_reply(history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in history:                                  # DB의 과거 대화를 전부
        messages.append({"role": m.role, "content": m.content})   # messages에 쌓음
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

def handle_chat(db, req):
    branch = repository.get_branch(db, req.branch_id)
    # 사용자의 메시지를 DB에 저장
    user_msg = repository.save_message(db, branch.session_id, "user", req.message,
                                       parent_id=branch.head_id)
    # 뿌리~방금 메시지까지 한 줄기만 LLM에 전달
    thread = repository.get_thread(db, user_msg.id)
    answer = generate_reply(thread)
    # AI 답변을 그 밑에 매달고, 가지 포인터를 새 끝으로 이동
    bot_msg = repository.save_message(db, branch.session_id, "assistant", answer,
                                      parent_id=user_msg.id)
    branch.head_id = bot_msg.id
    db.commit()
    return answer