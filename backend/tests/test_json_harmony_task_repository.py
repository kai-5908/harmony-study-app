"""JsonHarmonyTaskRepositoryのテスト."""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from repositories.harmony_task_repository import PersistenceError
from repositories.json_harmony_task_repository import JsonHarmonyTaskRepository


@pytest.fixture
def temp_json_path() -> Generator[str, None, None]:
    """テスト用の一時JSONファイルパスを提供する.

    Yields:
        一時ファイルのパス.

    """
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        yield tmp.name
    Path(tmp.name).unlink()


def test_invalid_json(temp_json_path: str) -> None:
    """不正なJSONファイルの処理テスト.

    Args:
        temp_json_path: テスト用の一時ファイルパス.

    """
    # まず正しいJSONで初期化
    repo = JsonHarmonyTaskRepository(temp_json_path)

    # 不正なJSONを書き込む
    with Path(temp_json_path).open("w", encoding="utf-8") as f:
        f.write("invalid json")

    # list_tasks()呼び出し時にPersistenceErrorが発生することを確認
    with pytest.raises(PersistenceError):
        repo.list_tasks()
