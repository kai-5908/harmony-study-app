import { vi } from 'vitest';
import '@testing-library/jest-dom';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../App';
import { HarmonyTaskAPI } from '../api/harmonyTaskApi';
import { type HarmonyTask, type Score, type Answer } from '../models/harmonyTaskModel';

vi.mock('../api/harmonyTaskApi', () => ({
  HarmonyTaskAPI: {
    getTasks: vi.fn(),
  },
}));

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('初期状態でローディング表示をする', async () => {
    // APIレスポンスを遅延させる
    vi.mocked(HarmonyTaskAPI.getTasks).mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve([]), 100)),
    );

    render(<App />);

    // ローディング表示のテスト（progress roleを持つ要素を探す）
    const loading = screen.getByRole('progressbar');
    expect(loading).toBeInTheDocument();
  });

  it('データ取得後にタスクリストを表示する', async () => {
    const mockScore: Score = {
      type: 'musicxml',
      data: 'test.musicxml',
    };

    const mockAnswer: Answer = {
      type: 'musicxml',
      data: 'answer.musicxml',
    };

    const mockTasks: HarmonyTask[] = [
      {
        id: '1',
        title: 'Test Task',
        description: 'Test Description',
        difficulty: 'easy',
        score: mockScore,
        answer: [mockAnswer],
        tags: ['test'],
      },
    ];

    // モックの実装
    vi.mocked(HarmonyTaskAPI.getTasks).mockResolvedValue(mockTasks);

    render(<App />);

    // データが取得されて表示されるのを待つ
    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    }, { timeout: 2000 });

    // 課題の詳細が表示されていることを確認
    expect(screen.getByText('Test Task')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByText('難易度: easy')).toBeInTheDocument();
  });
});
