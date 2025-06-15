"""JSON形式での和声課題リポジトリの実装.

和声課題データをJSONファイルとして永続化する実装を提供する.
"""

import json
from datetime import datetime
from pathlib import Path

from models.harmony_task_model import HarmonyTask
from repositories.harmony_task_repository import (
    FileNotFoundError,
    HarmonyTaskRepository,
    PersistenceError,
    ValidationError,
)


class JsonHarmonyTaskRepository(HarmonyTaskRepository):
    """JSON形式での和声課題リポジトリ実装."""

    def __init__(self, file_path: str) -> None:
        """初期化.

        Args:
            file_path (str): JSONファイルの保存パス.
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """JSONファイルの存在確認と初期化.

        ファイルが存在しない場合、または不正な形式の場合は新規作成する.
        """
        needs_initialization = not Path(self.file_path).exists()

        if not needs_initialization:
            try:
                with Path(self.file_path).open(encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict) or "tasks" not in data or "metadata" not in data:
                    needs_initialization = True
            except json.JSONDecodeError:
                needs_initialization = True
            except Exception as e:
                msg = f"Failed to read JSON file: {e!s}"
                raise PersistenceError(msg) from e

        if needs_initialization:
            path = Path(self.file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            initial_data = {"tasks": [], "metadata": self._create_metadata(0)}
            self._save_json(initial_data)

    def _create_metadata(self, total_tasks: int) -> dict:
        """メタデータを作成する.

        Args:
            total_tasks (int): 全タスク数.

        Returns:
            dict: メタデータ辞書.
        """
        return {
            "version": "1.0",
            "lastUpdated": datetime.now().isoformat(),
            "totalTasks": total_tasks,
        }

    def _save_json(self, data: dict) -> None:
        """JSONファイルを保存する.

        Args:
            data (dict): 保存するデータ.

        Raises:
            PersistenceError: ファイルの保存に失敗した場合.
        """
        try:
            path = Path(self.file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            msg = f"Failed to save JSON file: {e!s}"
            raise PersistenceError(msg) from e

    def _load_json(self) -> dict:
        """JSONファイルを読み込む.

        Returns:
            dict: 読み込んだJSONデータ.

        Raises:
            PersistenceError: ファイルの読み込みに失敗した場合または不正な形式の場合.
        """
        try:
            with Path(self.file_path).open(encoding="utf-8") as f:
                data = json.load(f)

            # 厳格な検証
            error_prefix = "Invalid JSON format:"
            if not isinstance(data, dict):
                msg = f"{error_prefix} root must be an object"
                raise PersistenceError(msg)
            if "tasks" not in data:
                msg = f"{error_prefix} missing 'tasks' field"
                raise PersistenceError(msg)
            if "metadata" not in data:
                msg = f"{error_prefix} missing 'metadata' field"
                raise PersistenceError(msg)
            if not isinstance(data["tasks"], list):
                msg = f"{error_prefix} 'tasks' must be an array"
                raise PersistenceError(msg)
            if not isinstance(data["metadata"], dict):
                msg = f"{error_prefix} 'metadata' must be an object"
                raise PersistenceError(msg)

            return data
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON format: {e!s}"
            raise PersistenceError(msg) from e
        except OSError as e:
            msg = f"Failed to read JSON file: {e!s}"
            raise PersistenceError(msg) from e

    def save_task(self, task: HarmonyTask) -> None:
        """和声課題を保存する.

        Args:
            task (HarmonyTask): 保存する和声課題.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: タスクデータが不正な場合.
        """
        try:
            if not isinstance(task, HarmonyTask):
                msg = "Invalid task data"
                raise ValidationError(msg)

            # データの読み込み
            data = self._load_json()
            tasks = data["tasks"]

            # 既存のタスクを探す
            for i, t in enumerate(tasks):
                if t["id"] == task.id:
                    tasks[i] = task.model_dump()
                    self._save_json(data)
                    return

            # 新規タスクの追加
            tasks.append(task.model_dump())
            data["metadata"] = self._create_metadata(len(tasks))
            self._save_json(data)
        except (ValidationError, FileNotFoundError):
            raise
        except Exception as e:
            msg = f"Failed to save task: {e!s}"
            raise PersistenceError(msg) from e

    def get_task(self, task_id: str) -> HarmonyTask:
        """指定されたIDの和声課題を取得する.

        Args:
            task_id (str): 取得する和声課題のID.

        Returns:
            HarmonyTask: 読み込まれた和声課題.

        Raises:
            FileNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: 読み込んだデータが不正な場合.
        """
        try:
            data = self._load_json()
            for task_data in data["tasks"]:
                if task_data["id"] == task_id:
                    return HarmonyTask.model_validate(task_data)
            msg = f"Task not found: {task_id}"
            raise FileNotFoundError(msg)
        except ValidationError as e:
            msg = f"Invalid task data: {e!s}"
            raise ValidationError(msg) from e
        except FileNotFoundError:
            raise
        except Exception as e:
            msg = f"Failed to load task: {e!s}"
            raise PersistenceError(msg) from e

    def delete_task(self, task_id: str) -> None:
        """指定されたIDの和声課題を削除する.

        Args:
            task_id (str): 削除する和声課題のID.

        Raises:
            FileNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.
        """
        try:
            data = self._load_json()
            tasks = data["tasks"]
            original_length = len(tasks)
            tasks[:] = [t for t in tasks if t["id"] != task_id]

            if len(tasks) == original_length:
                msg = f"Task not found: {task_id}"
                raise FileNotFoundError(msg)

            data["metadata"] = self._create_metadata(len(tasks))
            self._save_json(data)
        except FileNotFoundError:
            raise
        except Exception as e:
            msg = f"Failed to delete task: {e!s}"
            raise PersistenceError(msg) from e

    def list_tasks(
        self,
        difficulty: str | None = None,
        tags: list[str] | None = None,
    ) -> list[HarmonyTask]:
        """和声課題の一覧を取得する.

        Args:
            difficulty (str | None, optional): 難易度でフィルタする場合の値.
            tags (list[str] | None, optional): タグでフィルタする場合の値のリスト.

        Returns:
            list[HarmonyTask]: フィルタ条件に合致する和声課題のリスト.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.
        """
        try:
            data = self._load_json()
            tasks = []

            for task_data in data["tasks"]:
                task = HarmonyTask.model_validate(task_data)

                # 難易度フィルタ
                if difficulty and task.difficulty != difficulty:
                    continue

                # タグフィルタ
                if tags and not all(tag in task.tags for tag in tags):
                    continue

                tasks.append(task)

            return tasks
        except Exception as e:
            msg = f"Failed to list tasks: {e!s}"
            raise PersistenceError(msg) from e
