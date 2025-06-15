"""HarmonyTaskリポジトリインターフェース定義.

和声課題データの永続化層のインターフェースを提供する.
"""

from abc import ABC, abstractmethod
from typing import Sequence

from models.harmony_task_model import HarmonyTask


class PersistenceError(Exception):
    """永続化層の基底例外クラス."""

    pass


class FileNotFoundError(PersistenceError):
    """ファイルが見つからない場合の例外."""

    pass


class ValidationError(PersistenceError):
    """データバリデーションエラーの例外."""

    pass


class HarmonyTaskRepository(ABC):
    """和声課題リポジトリのインターフェース.

    全ての永続化実装（JSON, DB等）はこのインターフェースを実装する必要がある.
    """

    @abstractmethod
    def save_task(self, task: HarmonyTask) -> None:
        """和声課題を保存する.

        Args:
            task (HarmonyTask): 保存する和声課題.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: タスクデータが不正な場合.
        """
        pass

    @abstractmethod
    def load_task(self, task_id: str) -> HarmonyTask:
        """指定されたIDの和声課題を読み込む.

        Args:
            task_id (str): 読み込む和声課題のID.

        Returns:
            HarmonyTask: 読み込まれた和声課題.

        Raises:
            FileNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: 読み込んだデータが不正な場合.
        """
        pass

    @abstractmethod
    def list_tasks(
        self,
        difficulty: str = None,
        tags: Sequence[str] = None,
    ) -> list[HarmonyTask]:
        """和声課題の一覧を取得する.

        Args:
            difficulty (Optional[str]): フィルタする難易度.
            tags (Optional[List[str]]): フィルタするタグのリスト.

        Returns:
            List[HarmonyTask]: フィルタ条件に合致する和声課題のリスト.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> None:
        """指定されたIDの和声課題を削除する.

        Args:
            task_id (str): 削除する和声課題のID.

        Raises:
            FileNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.
        """
        pass
