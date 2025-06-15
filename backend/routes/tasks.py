"""Tasks(和声課題)に関するルート定義."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from models.harmony_task_model import HarmonyTask
from repositories.harmony_task_repository import (
    HarmonyTaskRepository,
    TaskNotFoundError,
)
from repositories.json_harmony_task_repository import JsonHarmonyTaskRepository

router = APIRouter()


def get_repository() -> HarmonyTaskRepository:
    """リポジトリのインスタンスを取得する."""
    # TASKS_FILEをimportするとcircular importになるため、ここで直接定義する
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    tasks_file = data_dir / "tasks.json"
    return JsonHarmonyTaskRepository(str(tasks_file))


@router.get("/tasks")
def list_tasks(
    repository: Annotated[
        HarmonyTaskRepository,
        Depends(get_repository),
    ],
) -> list[HarmonyTask]:
    """課題の一覧を取得する.

    Returns:
        list[HarmonyTask]: 和声課題のリスト

    """
    try:
        return repository.load_tasks()
    except TaskNotFoundError as err:
        raise HTTPException(status_code=404, detail="Tasks not found") from err


@router.get("/tasks/{task_id}")
def get_task(
    task_id: str,
    repository: Annotated[
        HarmonyTaskRepository,
        Depends(get_repository),
    ],
) -> HarmonyTask:
    """指定されたIDの課題を取得する.

    Args:
        task_id: 課題のID
        repository: 和声課題リポジトリ

    Returns:
        HarmonyTask: 和声課題

    Raises:
        HTTPException: 課題が見つからない場合は404を返す

    """
    try:
        return repository.load_task(task_id)
    except TaskNotFoundError as err:
        raise HTTPException(status_code=404, detail="Task not found") from err
