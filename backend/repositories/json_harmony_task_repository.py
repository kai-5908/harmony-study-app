"""JSON形式での和声課題リポジトリの実装.

和声課題データをJSONファイルとして永続化する実装を提供する.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

from models.harmony_task_model import HarmonyTask
from repositories.harmony_task_repository import (
    FileNotFoundError,
    HarmonyTaskRepository,
    PersistenceError,
    ValidationError,
)


class JsonHarmonyTaskRepository(HarmonyTaskRepository):
    """JSON形式での和声課題リポジトリ実装."""

    def __init__(self, file_path: str):
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
        needs_initialization = not os.path.exists(self.file_path)
        
        if not needs_initialization:
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, dict) or "tasks" not in data or "metadata" not in data:
                    needs_initialization = True
            except json.JSONDecodeError:
                needs_initialization = True
            except Exception as e:
                msg = f"Failed to read JSON file: {str(e)}"
                raise PersistenceError(msg) from e
        
        if needs_initialization:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            initial_data = {"tasks": [], "metadata": self._create_metadata(0)}
            self._save_json(initial_data)

    def _create_metadata(self, total_tasks: int) -> Dict:
        """メタデータを作成する.

        Args:
            total_tasks (int): 全タスク数.

        Returns:
            Dict: メタデータ辞書.
        """
        return {
            "version": "1.0",
            "lastUpdated": datetime.now(timezone.utc).isoformat(),
            "totalTasks": total_tasks,
        }

    def _save_json(self, data: Dict) -> None:
        """JSONファイルを保存する.

        Args:
            data (Dict): 保存するデータ.

        Raises:
            PersistenceError: ファイルの保存に失敗した場合.
        """
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            msg = f"Failed to save JSON file: {str(e)}"
            raise PersistenceError(msg) from e

    def _load_json(self) -> Dict:
        """JSONファイルを読み込む.

        Returns:
            Dict: 読み込んだJSONデータ.

        Raises:
            PersistenceError: ファイルの読み込みに失敗した場合または不正な形式の場合.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 厳格な検証
            if not isinstance(data, dict):
                raise PersistenceError("Invalid JSON format: root must be an object")
            if "tasks" not in data:
                raise PersistenceError("Invalid JSON format: missing 'tasks' field")
            if "metadata" not in data:
                raise PersistenceError("Invalid JSON format: missing 'metadata' field")
            if not isinstance(data["tasks"], list):
                raise PersistenceError("Invalid JSON format: 'tasks' must be an array")
            if not isinstance(data["metadata"], dict):
                raise PersistenceError("Invalid JSON format: 'metadata' must be an object")
            
            return data
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON format: {str(e)}"
            raise PersistenceError(msg) from e
        except IOError as e:
            msg = f"Failed to read JSON file: {str(e)}"
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
            # タスクの検証
            if not isinstance(task, HarmonyTask):
                msg = "Invalid task data"
                raise ValidationError(msg)

            # データの読み込み
            data = self._load_json()
            tasks = data.get("tasks", [])

            # 既存タスクの更新または新規追加
            task_dict = task.model_dump()  # dict()はdeprecatedなのでmodel_dump()を使用
            for i, existing_task in enumerate(tasks):
                if existing_task["id"] == task.id:
                    tasks[i] = task_dict
                    break
            else:
                tasks.append(task_dict)

            # メタデータの更新
            data["tasks"] = tasks
            data["metadata"] = self._create_metadata(len(tasks))
            self._save_json(data)
        except ValidationError:
            raise
        except Exception as e:
            msg = f"Failed to save task: {str(e)}"
            raise PersistenceError(msg) from e

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
        try:
            data = self._load_json()
            for task_data in data["tasks"]:
                if task_data["id"] == task_id:
                    return HarmonyTask.model_validate(task_data)
            msg = f"Task not found: {task_id}"
            raise FileNotFoundError(msg)
        except ValidationError as e:
            msg = f"Invalid task data: {str(e)}"
            raise ValidationError(msg) from e
        except FileNotFoundError:
            raise
        except Exception as e:
            msg = f"Failed to load task: {str(e)}"
            raise PersistenceError(msg) from e

    def delete_task(self, task_id: str) -> None:
        """和声課題を削除する.

        Args:
            task_id (str): 削除する和声課題のID.

        Raises:
            FileNotFoundError: 指定されたIDのタスクが存在しない場合.
            PersistenceError: 永続化処理でエラーが発生した場合.
        """
        try:
            data = self._load_json()
            tasks = data["tasks"]

            for i, task in enumerate(tasks):
                if task["id"] == task_id:
                    tasks.pop(i)
                    data["metadata"] = self._create_metadata(len(tasks))
                    self._save_json(data)
                    return

            msg = f"Task not found: {task_id}"
            raise FileNotFoundError(msg)
        except FileNotFoundError:
            raise
        except Exception as e:
            msg = f"Failed to delete task: {str(e)}"
            raise PersistenceError(msg) from e

    def list_tasks(
        self,
        difficulty: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[HarmonyTask]:
        """和声課題の一覧を取得する.

        Args:
            difficulty (Optional[str]): フィルタする難易度.
            tags (Optional[List[str]]): フィルタするタグのリスト.

        Returns:
            List[HarmonyTask]: フィルタ条件に合致する和声課題のリスト.

        Raises:
            PersistenceError: 永続化処理でエラーが発生した場合.
        """
        try:
            data = self._load_json()
            tasks = []

            for task_data in data.get("tasks", []):
                # 難易度フィルタ
                if difficulty and task_data.get("difficulty") != difficulty:
                    continue

                # タグフィルタ
                if tags:
                    task_tags = task_data.get("tags", [])
                    if not all(tag in task_tags for tag in tags):
                        continue

                try:
                    tasks.append(HarmonyTask.model_validate(task_data))
                except ValidationError:
                    # 不正なタスクはスキップ
                    continue

            return tasks
        except Exception as e:
            msg = f"Failed to list tasks: {str(e)}"
            raise PersistenceError(msg) from e
