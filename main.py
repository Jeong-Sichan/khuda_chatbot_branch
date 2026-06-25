from fastapi import FastAPI

from database import engine, Base
import models                  # 테이블이 Base에 등록되도록 불러오기만 함
from router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)     # router.py에 모아둔 엔드포인트를 통째로 장착