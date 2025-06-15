import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import type { HarmonyTask } from '../models/harmonyTaskModel';
import type { HarmonyTaskRepository } from '../repositories/harmonyTaskRepository';
import { JsonHarmonyTaskRepository } from '../repositories/jsonHarmonyTaskRepository';
import { FileNotFoundError } from '../repositories/harmonyTaskRepository';

describe('JsonHarmonyTaskRepository', () => {
  let repository: HarmonyTaskRepository;
  const storagePath = 'test-harmony-tasks.json';

  const sampleTask: HarmonyTask = {
    id: 'test001',
    description: 'テスト課題',
    title: 'テスト #1',
    difficulty: 'normal',
    tags: ['test', 'example'],
    score: {
      type: 'musicxml',
      data: 'test/score.musicxml',
    },
    answer: [
      {
        type: 'musicxml',
        data: 'test/answer.musicxml',
      },
    ],
  };

  beforeEach(() => {
    localStorage.clear();
    repository = new JsonHarmonyTaskRepository(storagePath);
  });

  afterEach(() => {
    localStorage.clear();
  });

  it('should initialize with empty tasks', async () => {
    const tasks = await repository.listTasks();
    expect(tasks).toHaveLength(0);
  });

  it('should save and load a task', async () => {
    await repository.saveTask(sampleTask);
    const loadedTask = await repository.loadTask(sampleTask.id);
    expect(loadedTask).toEqual(sampleTask);
  });

  it('should throw FileNotFoundError when loading non-existent task', async () => {
    await expect(repository.loadTask('nonexistent')).rejects.toThrow(FileNotFoundError);
  });

  it('should list tasks with filters', async () => {
    await repository.saveTask(sampleTask);

    // 難易度フィルタ
    let tasks = await repository.listTasks({ difficulty: 'normal' });
    expect(tasks).toHaveLength(1);
    expect(tasks[0]).toEqual(sampleTask);

    tasks = await repository.listTasks({ difficulty: 'hard' });
    expect(tasks).toHaveLength(0);

    // タグフィルタ
    tasks = await repository.listTasks({ tags: ['test'] });
    expect(tasks).toHaveLength(1);
    expect(tasks[0]).toEqual(sampleTask);

    tasks = await repository.listTasks({ tags: ['nonexistent'] });
    expect(tasks).toHaveLength(0);
  });

  it('should delete a task', async () => {
    await repository.saveTask(sampleTask);
    await repository.deleteTask(sampleTask.id);
    await expect(repository.loadTask(sampleTask.id)).rejects.toThrow(FileNotFoundError);
  });

  it('should update metadata after operations', async () => {
    await repository.saveTask(sampleTask);
    const data = JSON.parse(localStorage.getItem(storagePath) || '{}');
    expect(data.metadata).toBeDefined();
    expect(data.metadata.version).toBe('1.0');
    expect(data.metadata.totalTasks).toBe(1);
  });
});
