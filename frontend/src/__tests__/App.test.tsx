import { vi } from 'vitest';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
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
      },
    ];

    vi.mocked(HarmonyTaskAPI.getTasks).mockResolvedValue(mockTasks);

    render(<App />);

    // ローディングが終わってタスクが表示されることを確認
    const taskTitle = await screen.findByText('Test Task');
    expect(taskTitle).toBeInTheDocument();
  });
});
