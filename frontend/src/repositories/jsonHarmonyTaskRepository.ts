import { HarmonyTask, validateHarmonyTask } from '../models/harmonyTaskModel';
import {
  FileNotFoundError,
  HarmonyTaskRepository,
  PersistenceError,
  ValidationError,
} from './harmonyTaskRepository';

interface StorageData {
  tasks: HarmonyTask[];
  metadata: {
    version: string;
    lastUpdated: string;
    totalTasks: number;
  };
}

/**
 * JSON形式での和声課題リポジトリ実装
 */
export class JsonHarmonyTaskRepository implements HarmonyTaskRepository {
  private storagePath: string;

  constructor(storagePath = 'harmony-tasks.json') {
    this.storagePath = storagePath;
    this.ensureStorageExists();
  }

  private async ensureStorageExists(): Promise<void> {
    try {
      await this.loadJson();
    } catch {
      await this.saveJson({
        tasks: [],
        metadata: this.createMetadata(0),
      });
    }
  }

  private createMetadata(totalTasks: number) {
    return {
      version: '1.0',
      lastUpdated: new Date().toISOString(),
      totalTasks,
    };
  }

  private async loadJson(): Promise<StorageData> {
    try {
      const data = localStorage.getItem(this.storagePath);
      if (!data) {
        throw new Error('Storage not found');
      }
      return JSON.parse(data) as StorageData;
    } catch (e) {
      throw new PersistenceError(`Failed to load JSON: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  private async saveJson(data: StorageData): Promise<void> {
    try {
      localStorage.setItem(this.storagePath, JSON.stringify(data, null, 2));
    } catch (e) {
      throw new PersistenceError(`Failed to save JSON: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  async saveTask(task: HarmonyTask): Promise<void> {
    try {
      validateHarmonyTask(task);
      const data = await this.loadJson();

      // 既存タスクの更新または新規追加
      const index = data.tasks.findIndex((t) => t.id === task.id);
      if (index !== -1) {
        data.tasks[index] = task;
      } else {
        data.tasks.push(task);
      }

      // メタデータの更新
      data.metadata = this.createMetadata(data.tasks.length);
      await this.saveJson(data);
    } catch (e) {
      if (e instanceof ValidationError) {
        throw e;
      }
      throw new PersistenceError(`Failed to save task: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  async loadTask(taskId: string): Promise<HarmonyTask> {
    try {
      const data = await this.loadJson();
      const task = data.tasks.find((t) => t.id === taskId);
      if (!task) {
        throw new FileNotFoundError(`Task not found: ${taskId}`);
      }
      validateHarmonyTask(task);
      return task;
    } catch (e) {
      if (e instanceof FileNotFoundError || e instanceof ValidationError) {
        throw e;
      }
      throw new PersistenceError(
        `Failed to load task: ${e instanceof Error ? e.message : String(e)}`,
      );
    }
  }

  async listTasks(options?: { difficulty?: string; tags?: string[] }): Promise<HarmonyTask[]> {
    try {
      const data = await this.loadJson();
      let tasks = data.tasks;

      // フィルタリング
      if (options) {
        if (options.difficulty) {
          tasks = tasks.filter((t) => t.difficulty === options.difficulty);
        }
        if (options.tags) {
          tasks = tasks.filter((t) => {
            if (!t.tags) return false;
            return options.tags?.every((tag) => t.tags?.includes(tag));
          });
        }
      }

      // 各タスクのバリデーション
      return tasks.filter((task) => {
        try {
          validateHarmonyTask(task);
          return true;
        } catch {
          return false;
        }
      });
    } catch (e) {
      throw new PersistenceError(
        `Failed to list tasks: ${e instanceof Error ? e.message : String(e)}`,
      );
    }
  }

  async deleteTask(taskId: string): Promise<void> {
    try {
      const data = await this.loadJson();
      const originalLength = data.tasks.length;
      data.tasks = data.tasks.filter((t) => t.id !== taskId);

      if (data.tasks.length === originalLength) {
        throw new FileNotFoundError(`Task not found: ${taskId}`);
      }

      // メタデータの更新
      data.metadata = this.createMetadata(data.tasks.length);
      await this.saveJson(data);
    } catch (e) {
      if (e instanceof FileNotFoundError) {
        throw e;
      }
      throw new PersistenceError(
        `Failed to delete task: ${e instanceof Error ? e.message : String(e)}`,
      );
    }
  }
}
