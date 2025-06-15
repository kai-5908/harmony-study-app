import { HarmonyTaskAPI } from '../api/harmonyTaskApi';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const mockTasks = [
  {
    id: '1',
    title: 'Test Task',
    description: 'Test Description',
    difficulty: 'easy',
    score: {
      type: 'musicxml' as const,
      data: 'test.musicxml',
    },
    answer: [
      {
        type: 'musicxml' as const,
        data: 'answer.musicxml',
      },
    ],
  },
];

const handlers = [
  http.get('http://localhost:8000/api/tasks', () => {
    return HttpResponse.json(mockTasks);
  }),
  http.get('http://localhost:8000/api/tasks/:id', ({ params }) => {
    const task = mockTasks.find((t) => t.id === params.id);
    if (task) {
      return HttpResponse.json(task);
    }
    return new HttpResponse(null, { status: 404 });
  }),
];

const server = setupServer(...handlers);

beforeAll(() => {
  server.listen();
});

afterEach(() => {
  server.resetHandlers();
});

afterAll(() => {
  server.close();
});

describe('HarmonyTaskAPI', () => {
  test('getTasks returns tasks list', async () => {
    const tasks = await HarmonyTaskAPI.getTasks();
    expect(tasks).toEqual(mockTasks);
  });

  test('getTask returns a single task', async () => {
    const task = await HarmonyTaskAPI.getTask('1');
    expect(task).toEqual(mockTasks[0]);
  });

  test('getTask throws error for non-existent task', async () => {
    await expect(HarmonyTaskAPI.getTask('999')).rejects.toThrow();
  });
});
