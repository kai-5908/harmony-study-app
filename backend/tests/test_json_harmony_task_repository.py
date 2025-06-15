"""JsonHarmonyTaskRepositoryのテスト."""
import json
import os
import tempfile
from typing import Generator

import pytest

from models.harmony_task_model import Answer, AnswerType, HarmonyTask, Score, ScoreType
from repositories.harmony_task_repository import (
    FileNotFoundError,
    PersistenceError,
    ValidationError,
)
from repositories.json_harmony_task_repository import JsonHarmonyTaskRepository


@pytest.fixture
def temp_json_path() -> Generator[str, None, None]:
    """テスト用の一時JSONファイルパスを提供する."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        yield tmp.name
    os.unlink(tmp.name)


@pytest.fixture
def sample_task() -> HarmonyTask:
    """テスト用の和声課題サンプルを提供する."""
    return HarmonyTask(
        id="test001",
        description="テスト課題",
        title="テスト #1",
        difficulty="normal",
        tags=["test", "example"],
        score=Score(type=ScoreType.musicxml, data="test/score.musicxml"),
        answer=[Answer(type=AnswerType.musicxml, data="test/answer.musicxml")],
    )


def test_repository_initialization(temp_json_path: str) -> None:
    """リポジトリの初期化テスト."""
    repo = JsonHarmonyTaskRepository(temp_json_path)
    assert os.path.exists(temp_json_path)

    with open(temp_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "tasks" in data
        assert "metadata" in data
        assert data["metadata"]["version"] == "1.0"
        assert data["metadata"]["totalTasks"] == 0


def test_save_and_load_task(temp_json_path: str, sample_task: HarmonyTask) -> None:
    """タスクの保存と読み込みテスト."""
    repo = JsonHarmonyTaskRepository(temp_json_path)

    # 保存
    repo.save_task(sample_task)

    # 読み込み
    loaded_task = repo.load_task(sample_task.id)
    assert loaded_task == sample_task

    # メタデータの確認
    with open(temp_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["metadata"]["totalTasks"] == 1


def test_load_nonexistent_task(temp_json_path: str) -> None:
    """存在しないタスクの読み込みテスト."""
    repo = JsonHarmonyTaskRepository(temp_json_path)
    with pytest.raises(FileNotFoundError):
        repo.load_task("nonexistent")


def test_list_tasks_with_filters(temp_json_path: str, sample_task: HarmonyTask) -> None:
    """タスク一覧のフィルタリングテスト."""
    repo = JsonHarmonyTaskRepository(temp_json_path)
    repo.save_task(sample_task)

    # 難易度フィルタ
    tasks = repo.list_tasks(difficulty="normal")
    assert len(tasks) == 1
    assert tasks[0] == sample_task

    tasks = repo.list_tasks(difficulty="hard")
    assert len(tasks) == 0

    # タグフィルタ
    tasks = repo.list_tasks(tags=["test"])
    assert len(tasks) == 1
    assert tasks[0] == sample_task

    tasks = repo.list_tasks(tags=["nonexistent"])
    assert len(tasks) == 0


def test_delete_task(temp_json_path: str, sample_task: HarmonyTask) -> None:
    """タスクの削除テスト."""
    repo = JsonHarmonyTaskRepository(temp_json_path)
    repo.save_task(sample_task)

    # 削除
    repo.delete_task(sample_task.id)

    # 確認
    with pytest.raises(FileNotFoundError):
        repo.load_task(sample_task.id)

    # メタデータの確認
    with open(temp_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["metadata"]["totalTasks"] == 0


def test_invalid_json(temp_json_path: str) -> None:
    """不正なJSONファイルの処理テスト."""
    # まず正しいJSONで初期化
    repo = JsonHarmonyTaskRepository(temp_json_path)
    
    # 不正なJSONを書き込む
    with open(temp_json_path, "w", encoding="utf-8") as f:
        f.write("invalid json")
    
    # list_tasks()呼び出し時にPersistenceErrorが発生することを確認
    with pytest.raises(PersistenceError):
        repo.list_tasks()
