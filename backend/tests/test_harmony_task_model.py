"""HarmonyTaskモデルのユニットテスト.

pytestで実行可能.
"""

import pytest
from pydantic import ValidationError

from models.harmony_task_model import AnswerType, Difficulty, HarmonyTask, ScoreType


def test_valid_harmony_task():
    data = {
        "id": "task001",
        "description": "テスト課題",
        "score": {"type": "musicxml", "data": "<musicxml>...</musicxml>"},
        "answer": [
            {"type": "musicxml", "data": "<musicxml>...</musicxml>"},
        ],
        "title": "課題タイトル",
        "difficulty": "easy",
        "tags": ["初級", "二声"],
    }
    task = HarmonyTask.validate_task(data)
    assert task.id == "task001"
    assert task.difficulty == Difficulty.easy
    assert task.score.type == ScoreType.musicxml
    assert task.answer[0].type == AnswerType.musicxml


def test_empty_answer():
    data = {
        "id": "task002",
        "description": "解答なし",
        "score": {"type": "image", "data": "img.png"},
        "answer": [],
    }
    with pytest.raises(ValueError, match="answer must be a non-empty list"):
        HarmonyTask.validate_task(data)


def test_invalid_difficulty():
    data = {
        "id": "task003",
        "description": "難易度不正",
        "score": {"type": "json", "data": "{}"},
        "answer": [{"type": "json", "data": "{}"}],
        "difficulty": "invalid",
    }
    with pytest.raises(ValidationError, match="Input should be 'easy', 'normal' or 'hard'"):
        HarmonyTask.validate_task(data)


def test_optional_fields():
    data = {
        "id": "task004",
        "description": "オプション省略",
        "score": {"type": "image", "data": "img.png"},
        "answer": [{"type": "image", "data": "img.png"}],
    }
    task = HarmonyTask.validate_task(data)
    assert task.title is None
    assert task.difficulty is None
    assert task.tags is None
