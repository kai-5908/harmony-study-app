# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
});
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x';
import reactDom from 'eslint-plugin-react-dom';

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    'react-x': reactX,
    'react-dom': reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs['recommended-typescript'].rules,
    ...reactDom.configs.recommended.rules,
  },
});
```

---

## フロントエンド開発・CI/CD運用のベストプラクティス

### 設定ファイルの一元管理・命名統一
- JestやESLintなどの設定ファイルは、形式（.js/.cjs/.json）や命名を早い段階で統一し、不要な重複を避けましょう。
- 例：Jestは `jest.config.cjs` に統一。

### Prettier/ESLint自動整形・チェックの推奨
- PrettierやESLintによる自動整形・チェックをpre-commit hookやCIで自動化すると、ヒューマンエラーを防げます。
- 例：`npx prettier --write .` や `npx eslint . --fix` をコミット前に実行。

### クロスプラットフォーム対応
- コマンドやスクリプトはOS依存を避け、npm-scriptsやタスクランナー（例：`npm run lint`, `npm run test`）を活用しましょう。
- これにより、全員が同じ手順で作業できます。

### CI/CDワークフロー設計の明文化
- どのコマンド・設定ファイルを使うか、READMEやドキュメントに明記しておくと、チーム全体での認識ズレを防げます。
- 例：CIでは `npx prettier --check .`、`npx eslint .`、`npx jest --ci --coverage` を実行。

### エラー発生時の切り分け・早期修正
- エラーが出た際は、設定ファイルやコマンドの重複・競合を疑い、早めに整理・統一しましょう。

### ドキュメント充実の重要性
- 設定や運用ルール、CIの使い方などをREADME等にまとめておくと、今後の開発や新メンバー参加時にも役立ちます。

---
