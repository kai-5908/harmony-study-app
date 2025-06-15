import { validateHarmonyTask } from '../models/harmonyTaskModel';

describe('HarmonyTask バリデーション', () => {
  it('正常なデータはバリデーションを通過する', () => {
    const data = {
      id: 'task001',
      description: 'テスト課題',
      score: { type: 'musicxml', data: '<musicxml>...</musicxml>' },
      answer: [{ type: 'musicxml', data: '<musicxml>...</musicxml>' }],
      title: '課題タイトル',
      difficulty: 'easy',
      tags: ['初級', '二声'],
    };
    expect(() => validateHarmonyTask(data)).not.toThrow();
  });

  it('answerが空配列だとエラー', () => {
    const data = {
      id: 'task002',
      description: '解答なし',
      score: { type: 'image', data: 'img.png' },
      answer: [],
    };
    expect(() => validateHarmonyTask(data)).toThrow('answer must be a non-empty array');
  });

  it('difficultyが不正だとエラー', () => {
    const data = {
      id: 'task003',
      description: '難易度不正',
      score: { type: 'json', data: '{}' },
      answer: [{ type: 'json', data: '{}' }],
      difficulty: 'invalid',
    };
    expect(() => validateHarmonyTask(data)).toThrow('difficulty is invalid');
  });

  it('オプション項目がなくてもバリデーションを通過する', () => {
    const data = {
      id: 'task004',
      description: 'オプション省略',
      score: { type: 'image', data: 'img.png' },
      answer: [{ type: 'image', data: 'img.png' }],
    };
    expect(() => validateHarmonyTask(data)).not.toThrow();
  });
});
