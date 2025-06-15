"""Tasksルーターのテスト."""

import json
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from main import app
from routes.tasks import get_repository


@pytest.fixture
def temp_json_path() -> Generator[str, None, None]:
    """テスト用の一時JSONファイルパスを提供する.

    Yields:
        str: 一時JSONファイルのパス

    """
    with tempfile.NamedTemporaryFile(suffix=".json", mode="w", encoding="utf-8", delete=False) as tmp:
        # サンプルデータを書き込む
        data = {
            "tasks": [
                {
                    "id": "1",
                    "title": "バッハコラール バス課題 No.1",
                    "description": "バッハコラールのバス声部が与えられています。上三声を完成させてください。",
                    "score": {"type": "musicxml", "data": "scores/bach_chorale_bass_1.musicxml"},
                    "answer": [{"type": "musicxml", "data": "answers/bach_chorale_bass_1_answer.musicxml"}],
                    "difficulty": "normal",
                    "tags": ["バッハコラール", "バス課題"],
                },
            ],
            "metadata": {
                "version": "1.0",
                "lastUpdated": "2025-06-16T10:00:00",
                "totalTasks": 1,
            },
        }
        json.dump(data, tmp, ensure_ascii=False)
        tmp.flush()  # ファイルに確実に書き込む
        yield tmp.name
    Path(tmp.name).unlink()


@pytest.fixture
def test_client(temp_json_path: str) -> Generator[TestClient, None, None]:
    """テスト用のFastAPIクライアントを提供する.

    Args:
        temp_json_path: 一時JSONファイルのパス

    Yields:
        TestClient: テスト用のFastAPIクライアント
    """
    from repositories.json_harmony_task_repository import JsonHarmonyTaskRepository

    def get_test_repository() -> JsonHarmonyTaskRepository:
        return JsonHarmonyTaskRepository(temp_json_path)

    app.dependency_overrides[get_repository] = get_test_repository
    try:
        client = TestClient(app)
        yield client
    finally:
        app.dependency_overrides.clear()


def test_list_tasks(test_client: TestClient) -> None:
    """課題一覧の取得テスト."""
    response = test_client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1  # テストデータの課題数
    assert tasks[0]["id"] == "1"
    assert tasks[0]["title"] == "バッハコラール バス課題 No.1"
    assert tasks[0]["difficulty"] == "normal"


def test_get_task(test_client: TestClient) -> None:
    """個別課題の取得テスト."""
    response = test_client.get("/api/tasks/1")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == "1"
    assert task["title"] == "バッハコラール バス課題 No.1"
    assert task["difficulty"] == "normal"


def test_get_task_not_found(test_client: TestClient) -> None:
    """存在しない課題の取得テスト."""
    response = test_client.get("/api/tasks/999")
    assert response.status_code == 404
