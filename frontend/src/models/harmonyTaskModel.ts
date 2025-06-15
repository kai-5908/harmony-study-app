// 和声課題データモデル TypeScript定義

export type ScoreType = 'musicxml' | 'image' | 'json';
export type AnswerType = 'musicxml' | 'image' | 'json';

export interface Score {
  type: ScoreType;
  data: string; // 譜例データ本体またはパス
}

export interface Answer {
  type: AnswerType;
  data: string; // 解答データ本体またはパス
}

// 難易度はenumで厳格化
export type Difficulty = 'easy' | 'normal' | 'hard';

// HarmonyTask型のバリデーション関数
export function validateHarmonyTask(task: unknown): asserts task is HarmonyTask {
  if (typeof task !== 'object' || task === null) throw new Error('task must be an object');
  const t = task as Partial<HarmonyTask>;
  if (typeof t.id !== 'string' || !t.id) throw new Error('id is required');
  if (typeof t.description !== 'string' || !t.description)
    throw new Error('description is required');
  if (!t.score || typeof t.score !== 'object') throw new Error('score is required');
  const score = t.score as Score;
  if (!['musicxml', 'image', 'json'].includes(score.type)) throw new Error('score.type is invalid');
  if (typeof score.data !== 'string' || !score.data) throw new Error('score.data is required');
  if (!Array.isArray(t.answer) || t.answer.length === 0)
    throw new Error('answer must be a non-empty array');
  for (const a of t.answer) {
    const ans = a as Answer;
    if (!['musicxml', 'image', 'json'].includes(ans.type))
      throw new Error('answer.type is invalid');
    if (typeof ans.data !== 'string' || !ans.data) throw new Error('answer.data is required');
  }
  if (t.difficulty && !['easy', 'normal', 'hard'].includes(t.difficulty))
    throw new Error('difficulty is invalid');
  if (t.tags && !Array.isArray(t.tags)) throw new Error('tags must be an array');
}

export interface HarmonyTask {
  id: string;
  description: string;
  score: Score;
  answer: Answer[];
  title?: string;
  difficulty?: Difficulty;
  tags?: string[];
}
