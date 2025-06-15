import '@testing-library/jest-dom';
import { vi } from 'vitest';

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

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

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
