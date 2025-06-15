"""HarmonyTaskリポジトリインターフェース定義.

和声課題データの永続化層のインターフェースを提供する.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from models.harmony_task_model import HarmonyTask


class PersistenceError(Exception):
    """永続化層の基底例外クラス."""


class TaskNotFoundError(PersistenceError):
    """ファイルが見つからない場合の例外."""


class ValidationError(PersistenceError):
    """データバリデーションエラーの例外."""


class HarmonyTaskRepository(ABC):
    """和声課題リポジトリのインターフェース.

    全ての永続化実装(JSON, DB等)はこのインターフェースを実装する必要がある.
    """

    @abstractmethod
    def save_task(self, task: HarmonyTask) -> None:
        """和声課題を保存する.

        Args:
            task (HarmonyTask): 保存する和声課題.        Raises:

            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: タスクデータが不正な場合.

        """

    @abstractmethod
    def load_task(self, task_id: str) -> HarmonyTask:
        """指定されたIDの和声課題を取得する.

        Args:
            task_id (str): 取得する和声課題のID.

        Returns:
            HarmonyTask: 読み込まれた和声課題.

        Raises:
            TaskNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: 読み込んだデータが不正な場合.

        """

    @abstractmethod
    def list_tasks(
        self,
        difficulty: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> list[HarmonyTask]:
        """和声課題の一覧を取得する.

        Args:
            difficulty (str | None): 難易度でフィルタする場合の値.
            tags (Sequence[str] | None): タグでフィルタする場合の値のリスト.

        Returns:
            list[HarmonyTask]: フィルタ条件に合致する和声課題のリスト.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.

        """

    @abstractmethod
    def delete_task(self, task_id: str) -> None:
        """指定されたIDの和声課題を削除する.

        Args:
            task_id (str): 削除する和声課題のID.

        Raises:
            TaskNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.

        """
