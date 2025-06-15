# 開発環境セットアップガイド

このガイドでは、ローカル開発環境のセットアップ手順を説明します。

## 必要なツール

- Node.js v20.x以上
- Python 3.12以上
- Git
- Visual Studio Code

## VSCode拡張機能

以下の拡張機能をインストールしてください：

- ESLint (`dbaeumer.vscode-eslint`)
- Prettier (`esbenp.prettier-vscode`)
- Python (`ms-python.python`)
- Ruff (`charliermarsh.ruff`)
- Jest (`orta.vscode-jest`)

## 環境構築手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/kai-5908/harmony-study-app.git
cd harmony-study-app
```

### 2. フロントエンド環境のセットアップ

```bash
cd frontend
npm install
```

### 3. バックエンド環境のセットアップ

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 4. 開発用コマンド

フロントエンド:
- 開発サーバー起動: `npm run dev`
- テスト実行: `npm test`
- リント実行: `npm run lint`

バックエンド:
- テスト実行: `pytest`
- リント実行: `ruff check .`
- フォーマット: `ruff format .`

## コミット前のチェック

以下の項目を確認してください：

1. 全てのテストが通過すること
2. リントエラーがないこと
3. コードフォーマットが正しいこと
4. 変更に関連するドキュメントが更新されていること

## コーディング規約

- [ESLint](https://eslint.org/)と[Prettier](https://prettier.io/)の設定に従うこと
- Pythonコードは[ruff](https://github.com/astral-sh/ruff)の規約に従うこと
- コミットメッセージは[Conventional Commits](https://www.conventionalcommits.org/)の形式に従うこと

## トラブルシューティング

### よくある問題と解決方法

1. npm installでエラーが発生する場合
   ```bash
   npm install --legacy-peer-deps
   ```

2. huskyのhookが実行されない場合
   ```bash
   npx husky init
   ```

3. VSCodeの拡張機能が正しく動作しない場合
   - ワークスペースを再読み込み
   - 拡張機能の再インストール

## 参考文献

- [Node.js Documentation](https://nodejs.org/docs)
- [Python Documentation](https://docs.python.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
