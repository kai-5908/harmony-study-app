import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { HarmonyTaskListItem } from '../components/harmony-task/HarmonyTaskListItem';
import { HarmonyTaskGridItem } from '../components/harmony-task/HarmonyTaskGridItem';
import { HarmonyTask } from '../models/harmonyTaskModel';

const sampleTask: HarmonyTask = {
  id: '1',
  title: 'テスト課題1',
  description: 'テスト用の課題です',
  score: { type: 'musicxml', data: 'test.musicxml' },
  answer: [{ type: 'musicxml', data: 'answer.musicxml' }],
  difficulty: 'normal',
  tags: ['テスト'],
};

describe('HarmonyTaskListItem', () => {
  it('課題の情報が正しく表示される', () => {
    render(
      <MemoryRouter>
        <HarmonyTaskListItem task={sampleTask} />
      </MemoryRouter>,
    );

    expect(screen.getByText('テスト課題1')).toBeInTheDocument();
    expect(screen.getByText('テスト用の課題です')).toBeInTheDocument();
    expect(screen.getByText('難易度: normal')).toBeInTheDocument();
    expect(screen.getByText('テスト')).toBeInTheDocument();
  });

  it('タイトルがない場合は「無題の課題」と表示される', () => {
    const taskWithoutTitle = { ...sampleTask, title: undefined };
    render(
      <MemoryRouter>
        <HarmonyTaskListItem task={taskWithoutTitle} />
      </MemoryRouter>,
    );

    expect(screen.getByText('無題の課題')).toBeInTheDocument();
  });
});

describe('HarmonyTaskGridItem', () => {
  it('課題の情報が正しく表示される', () => {
    render(
      <MemoryRouter>
        <HarmonyTaskGridItem task={sampleTask} />
      </MemoryRouter>,
    );

    expect(screen.getByText('テスト課題1')).toBeInTheDocument();
    expect(screen.getByText('テスト用の課題です')).toBeInTheDocument();
    expect(screen.getByText('難易度: normal')).toBeInTheDocument();
    expect(screen.getByText('テスト')).toBeInTheDocument();
  });

  it('タイトルがない場合は「無題の課題」と表示される', () => {
    const taskWithoutTitle = { ...sampleTask, title: undefined };
    render(
      <MemoryRouter>
        <HarmonyTaskGridItem task={taskWithoutTitle} />
      </MemoryRouter>,
    );

    expect(screen.getByText('無題の課題')).toBeInTheDocument();
  });
});
