"""HarmonyTaskモデル定義モジュール.

和声課題データモデルおよびバリデーションを提供する。
"""

from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, Field


class ScoreType(str, Enum):
    """譜例データのタイプ."""

    musicxml = "musicxml"
    image = "image"
    json = "json"
    # 必要に応じて拡張


class AnswerType(str, Enum):
    """解答データのタイプ."""

    musicxml = "musicxml"
    image = "image"
    json = "json"
    # 必要に応じて拡張


class Score(BaseModel):
    """譜例データモデル."""

    type: ScoreType = Field(..., description="譜例データのタイプ")
    data: str = Field(..., description="譜例データ本体またはパス")


class Answer(BaseModel):
    """解答データモデル."""

    type: AnswerType = Field(..., description="解答データのタイプ")
    data: str = Field(..., description="解答データ本体またはパス")


class Difficulty(str, Enum):
    """課題の難易度."""

    easy = "easy"
    normal = "normal"
    hard = "hard"


class HarmonyTask(BaseModel):
    """和声課題データモデル.

    Attributes:
        id (str): 一意な課題ID.
        description (str): 課題の説明文.
        score (Score): 譜例データ.
        answer (list[Answer]): 解答データ(1つ以上).
        title (str | None): タイトル.
        difficulty (Difficulty | None): 難易度.
        tags (list[str] | None): タグ.

    """

    id: str
    description: str
    score: Score
    answer: list[Answer]
    title: str | None = None
    difficulty: Difficulty | None = None
    tags: list[str] | None = None

    @classmethod
    def validate_task(cls, data: dict) -> "HarmonyTask":
        """HarmonyTaskデータのバリデーションとインスタンス生成.

        Args:
            data (dict): 入力データ。

        Returns:
            HarmonyTask: バリデーション済みインスタンス。

        Raises:
            ValueError: answerが空、またはdifficultyが不正な場合。

        """
        obj = cls.parse_obj(data)
        if not obj.answer or len(obj.answer) == 0:
            msg = "answer must be a non-empty list"
            raise ValueError(msg)
        if obj.difficulty and obj.difficulty not in Difficulty.__members__.values():
            msg = "difficulty is invalid"
            raise ValueError(msg)
        return obj

    class Config:
        """Pydantic設定."""

        schema_extra: ClassVar[dict] = {
            "example": {
                "id": "task001",
                "description": "和声課題の説明文",
                "score": {"type": "musicxml", "data": "<musicxml>...</musicxml>"},
                "answer": [
                    {"type": "musicxml", "data": "<musicxml>...</musicxml>"},
                ],
                "title": "課題タイトル",
                "difficulty": "easy",
                "tags": ["初級", "二声"],
            },
        }
