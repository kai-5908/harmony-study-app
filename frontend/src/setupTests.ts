import '@testing-library/jest-dom';
import { vi } from 'vitest';
import { beforeAll, afterEach, afterAll } from 'vitest';

// localStorageのモック
const localStorageMock = (() => {
  let store: { [key: string]: string } = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

// localStorageのグローバル設定
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// MSWのエラーを防ぐためのダミーのfetch実装
global.fetch = vi.fn();

// MSWのエラーハンドリング
global.Response = Response;
global.Request = Request;
global.Headers = Headers;

// グローバルなテスト設定やモックをここに追加
beforeAll(() => {
  // テスト全体の前に1回実行される
});

afterAll(() => {
  // テスト全体の後に1回実行される
});

beforeEach(() => {
  // 各テストの前に実行される
  vi.clearAllMocks();
});

afterEach(() => {
  // 各テストの後に実行される
});
