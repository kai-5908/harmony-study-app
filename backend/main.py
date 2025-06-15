"""アプリケーションのエントリーポイント.

FastAPIアプリケーションのインスタンスと設定を提供する.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import tasks

# データファイルのパス設定
TASKS_FILE = Path(__file__).parent / "data" / "tasks.json"

# FastAPIアプリケーションの作成
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # フロントエンドのオリジン
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(
    tasks.router,
    prefix="/api",
    tags=["tasks"],
)


# 依存性の注入
def create_repository() -> tasks.JsonHarmonyTaskRepository:
    """タスクリポジトリを作成する."""
    return tasks.JsonHarmonyTaskRepository(str(TASKS_FILE))


app.dependency_overrides[tasks.get_repository] = create_repository

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
