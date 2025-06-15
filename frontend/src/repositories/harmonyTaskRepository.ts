import { HarmonyTask } from '../models/harmonyTaskModel';

/**
 * 永続化層のエラー定義
 */
export class PersistenceError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'PersistenceError';
  }
}

export class FileNotFoundError extends PersistenceError {
  constructor(message: string) {
    super(message);
    this.name = 'FileNotFoundError';
  }
}

export class ValidationError extends PersistenceError {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

/**
 * Result型の定義
 */
export type Result<T, E> = Success<T> | Failure<E>;

export class Success<T> {
  readonly value: T;
  readonly isSuccess = true;
  
  constructor(value: T) {
    this.value = value;
  }
}

export class Failure<E> {
  readonly error: E;
  readonly isSuccess = false;
  
  constructor(error: E) {
    this.error = error;
  }
}

/**
 * 和声課題リポジトリのインターフェース
 */
export interface HarmonyTaskRepository {
  /**
   * 和声課題を保存する
   * @param task 保存する和声課題
   * @throws PersistenceError 永続化処理でエラーが発生した場合
   * @throws ValidationError タスクデータが不正な場合
   */
  saveTask(task: HarmonyTask): Promise<void>;

  /**
   * 指定されたIDの和声課題を読み込む
   * @param taskId 読み込む和声課題のID
   * @returns 読み込まれた和声課題
   * @throws FileNotFoundError 指定されたIDのタスクが存在しない場合
   * @throws PersistenceError 永続化処理でエラーが発生した場合
   * @throws ValidationError 読み込んだデータが不正な場合
   */
  loadTask(taskId: string): Promise<HarmonyTask>;

  /**
   * 和声課題の一覧を取得する
   * @param options フィルタオプション
   * @returns フィルタ条件に合致する和声課題のリスト
   * @throws PersistenceError 永続化処理でエラーが発生した場合
   */
  listTasks(options?: {
    difficulty?: string;
    tags?: string[];
  }): Promise<HarmonyTask[]>;

  /**
   * 指定されたIDの和声課題を削除する
   * @param taskId 削除する和声課題のID
   * @throws FileNotFoundError 指定されたIDのタスクが存在しない場合
   * @throws PersistenceError 永続化処理でエラーが発生した場合
   */
  deleteTask(taskId: string): Promise<void>;
}
