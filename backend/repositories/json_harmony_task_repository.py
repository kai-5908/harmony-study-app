"""JSON形式での和声課題リポジトリの実装.

和声課題データをJSONファイルとして永続化する実装を提供する.
"""

import json
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from models.harmony_task_model import HarmonyTask
from repositories.harmony_task_repository import (
    HarmonyTaskRepository,
    PersistenceError,
    TaskNotFoundError,
    ValidationError,
)


class JsonHarmonyTaskRepository(HarmonyTaskRepository):
    """JSON形式での和声課題リポジトリ実装.

    Attributes:
        file_path (str): JSONファイルの保存パス.

    """

    def __init__(self, file_path: str) -> None:
        """イニシャライザ.

        Args:
            file_path: JSONファイルの保存パス.

        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """JSONファイルの存在確認と初期化.

        ファイルが存在しない場合、または不正な形式の場合は新規作成する.

        Raises:
            PersistenceError: ファイルの読み書きに失敗した場合.

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
            total_tasks: 全タスク数.

        Returns:
            メタデータ辞書.

        """
        return {
            "version": "1.0",
            "lastUpdated": datetime.now().isoformat(),
            "totalTasks": total_tasks,
        }

    def _save_json(self, data: dict) -> None:
        """JSONファイルを保存する.

        Args:
            data: 保存するデータ.

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

    def _read_json(self) -> dict:
        """JSONファイルを読み込む.

        Returns:
            JSONデータ.

        Raises:
            PersistenceError: ファイルの読み込みに失敗した場合.

        """
        try:
            with Path(self.file_path).open(encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON format: {e!s}"
            raise PersistenceError(msg) from e
        except OSError as e:
            msg = f"Failed to read JSON file: {e!s}"
            raise PersistenceError(msg) from e

    def _load_json(self) -> dict:
        """JSONファイルを読み込んで検証する.

        Returns:
            検証済みのJSONデータ.

        Raises:
            PersistenceError: ファイルの読み込みに失敗した場合または不正な形式の場合.

        """
        try:
            data = self._read_json()
            error_prefix = "Invalid JSON format:"

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

            return data  # noqa: TRY300
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON format: {e!s}"
            raise PersistenceError(msg) from e
        except OSError as e:
            msg = f"Failed to read JSON file: {e!s}"
            raise PersistenceError(msg) from e

    def _validate_task_data(self, task: object) -> None:
        """タスクデータを検証する.

        Args:
            task: 検証するタスクデータ.

        Raises:
            ValidationError: タスクデータが不正な場合.

        """
        if not isinstance(task, HarmonyTask):
            msg = "Invalid task data"
            raise ValidationError(msg)

    def _handle_missing_task(self, task_id: str) -> None:
        """存在しないタスクに対するエラーを発生させる.

        Args:
            task_id: タスクID.

        Raises:
            TaskNotFoundError: 常に発生する.

        """
        msg = f"Task not found: {task_id}"
        raise TaskNotFoundError(msg)

    def save_task(self, task: HarmonyTask) -> None:
        """和声課題を保存する.

        Args:
            task: 保存する和声課題.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: タスクデータが不正な場合.

        """
        try:
            self._validate_task_data(task)

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
        except (ValidationError, TaskNotFoundError):
            raise
        except Exception as e:
            msg = f"Failed to save task: {e!s}"
            raise PersistenceError(msg) from e

    def load_task(self, task_id: str) -> HarmonyTask:
        """指定されたIDの和声課題を取得する.

        Args:
            task_id: 取得する和声課題のID.

        Returns:
            読み込まれた和声課題.

        Raises:
            TaskNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.
            ValidationError: 読み込んだデータが不正な場合.

        """
        try:
            data = self._load_json()
            for task_data in data["tasks"]:
                if task_data["id"] == task_id:
                    return HarmonyTask.model_validate(task_data)
            # unreachable 警告を避けるため、直接例外を発生させる
            msg = f"Task not found: {task_id}"
            raise TaskNotFoundError(msg)  # noqa: TRY301
        except ValidationError as e:
            msg = f"Invalid task data: {e!s}"
            raise ValidationError(msg) from e
        except TaskNotFoundError:
            raise
        except Exception as e:
            msg = f"Failed to load task: {e!s}"
            raise PersistenceError(msg) from e

    def delete_task(self, task_id: str) -> None:
        """指定されたIDの和声課題を削除する.

        Args:
            task_id: 削除する和声課題のID.

        Raises:
            TaskNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.

        """
        try:
            data = self._load_json()
            tasks = data["tasks"]
            original_length = len(tasks)
            tasks[:] = [t for t in tasks if t["id"] != task_id]

            if len(tasks) == original_length:
                self._handle_missing_task(task_id)
            else:
                data["metadata"] = self._create_metadata(len(tasks))
                self._save_json(data)
        except TaskNotFoundError:
            raise
        except Exception as e:
            msg = f"Failed to delete task: {e!s}"
            raise PersistenceError(msg) from e

    def list_tasks(
        self,
        difficulty: str | None = None,
        tags: Sequence[str] | None = None,
    ) -> list[HarmonyTask]:
        """和声課題の一覧を取得する.

        Args:
            difficulty: 難易度でフィルタする場合の値.
            tags: タグでフィルタする場合の値のリスト.

        Returns:
            フィルタ条件に合致する和声課題のリスト.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.

        """
        try:
            data = self._load_json()
            tasks: list[HarmonyTask] = []

            for task_data in data["tasks"]:
                try:
                    task = HarmonyTask.model_validate(task_data)

                    # 難易度フィルタ
                    if difficulty is not None and task.difficulty != difficulty:
                        continue

                    # タグフィルタ
                    if tags:  # tagsがNoneまたは空のリストでない場合のみフィルタリング
                        if not task.tags:  # タスクにタグがない場合はスキップ
                            continue
                        if not all(t in task.tags for t in tags):
                            continue

                    tasks.append(task)
                except Exception:  # noqa: BLE001, S112
                    # 無効なタスクはログに記録してスキップ
                    continue
            return tasks  # noqa: TRY300
        except Exception as e:
            msg = f"Failed to list tasks: {e!s}"
            raise PersistenceError(msg) from e

    def load_tasks(self) -> list[HarmonyTask]:
        """全ての和声課題を取得する.

        Returns:
            list[HarmonyTask]: 読み込まれた和声課題のリスト.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.
            TaskNotFoundError: 課題が見つからない場合.

        """
        def validate_data(data: dict) -> None:
            """データの形式を検証する.

            Args:
                data: 検証するデータ

            Raises:
                ValidationError: データ形式が不正な場合

            """
            if not isinstance(data, dict) or "tasks" not in data:
                msg = "Invalid JSON format: missing 'tasks' field"
                raise ValidationError(msg)

        try:
            with Path(self.file_path).open(encoding="utf-8") as f:
                data = json.load(f)

            validate_data(data)
            tasks = data["tasks"]
            return [HarmonyTask(**task) for task in tasks]

        except json.JSONDecodeError as e:
            msg = f"Invalid JSON format: {e!s}"
            raise ValidationError(msg) from e
        except Exception as e:
            msg = f"Failed to read tasks from JSON file: {e!s}"
            raise PersistenceError(msg) from e
