// 和声課題データモデル TypeScript定義

export type ScoreType = 'musicxml' | 'image' | 'json';
export type AnswerType = 'musicxml' | 'image' | 'json';
export type Difficulty = 'easy' | 'normal' | 'hard';

export interface Score {
  type: ScoreType;
  data: string; // 譜例データ本体またはパス
}

export interface Answer {
  type: AnswerType;
  data: string; // 解答データ本体またはパス
}

// 課題の種類
export type TaskType = 'bass' | 'soprano' | 'alternating';

// タスクのステータス
export type TaskStatus = 'not_started' | 'in_progress' | 'completed';

// 和声課題のインターフェース
export interface HarmonyTask {
  id: string;
  title?: string;
  description: string;
  score: Score;
  answer: Answer[];
  difficulty?: Difficulty;
  tags?: string[];
}

// HarmonyTask型のバリデーション関数
export function validateHarmonyTask(task: unknown): asserts task is HarmonyTask {
  if (!task || typeof task !== 'object') {
    throw new Error('Task must be an object');
  }

  const t = task as Partial<HarmonyTask>;

  if (!t.id || typeof t.id !== 'string') {
    throw new Error('Task must have a valid id');
  }

  if (t.title && typeof t.title !== 'string') {
    throw new Error('Task title must be a string if provided');
  }

  if (!t.description || typeof t.description !== 'string') {
    throw new Error('Task must have a valid description');
  }

  if (!t.score || typeof t.score !== 'object' || !t.score.type || !t.score.data) {
    throw new Error('Task must have a valid score');
  }

  if (!t.answer || !Array.isArray(t.answer) || t.answer.length === 0) {
    throw new Error('answer must be a non-empty array');
  }

  for (const answer of t.answer) {
    if (typeof answer !== 'object' || !answer.type || !answer.data) {
      throw new Error('Task must have valid answers');
    }
  }

  if (t.difficulty !== undefined && !['easy', 'normal', 'hard'].includes(t.difficulty)) {
    throw new Error('difficulty is invalid');
  }

  if (t.tags !== undefined && !Array.isArray(t.tags)) {
    throw new Error('tags must be an array if provided');
  }
}
