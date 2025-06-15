# harmony-study-app
和声学習アプリの開発用リポジトリ

## ディレクトリ構成（推奨）

```
harmony-study-app/
├── backend/                # Pythonバックエンド（API・ロジック）
│   ├── app/                # アプリ本体（ビジネスロジック・API等）
│   │   ├── __init__.py
│   │   ├── models/         # ドメインモデル
│   │   ├── services/       # サービス層
│   │   ├── api/            # FastAPI等のエンドポイント
│   │   └── ...             # その他（utils等）
│   ├── tests/              # テストコード
│   ├── pyproject.toml
│   ├── pytest.ini
│   └── ...                 # その他設定ファイル
├── frontend/               # TypeScriptフロントエンド（React等）
│   ├── src/                # ソースコード
│   ├── public/             # 静的ファイル
│   ├── tests/              # テストコード
│   ├── package.json
│   └── ...                 # その他設定ファイル
├── docs/                   # ドキュメント
├── .github/                # GitHub関連（Actions, Issueテンプレ等）
└── README.md
```

- backend: Python（FastAPI等）でAPI・ロジックを実装
- frontend: TypeScript（React等）でUIを実装
- docs: 設計・運用・技術ドキュメント
- .github: CI/CDやテンプレート

---

## CI/CD・Lint・テスト運用ガイド

### 概要
- 本リポジトリはフロントエンド（TypeScript/React）・バックエンド（Python/FastAPI等）の両方に対して、GitHub ActionsによるCI/CDを導入しています。
- 各ディレクトリごとにLint・Format・テスト・型チェックが自動実行され、品質を担保します。

### フロントエンド（frontend/）
- 主なコマンド:
    - Lint: `npm run lint`
    - フォーマット: `npx prettier --write .`
    - テスト: `npm test` または `npm run test`
- CIで実行される内容:
    - ESLint（コード規約チェック）
    - Prettier（コード整形チェック）
    - Jest（ユニットテスト・カバレッジ）
- 注意点:
    - push前に必ず `npx prettier --write .` で整形してください
    - Jestの設定ファイルは `jest.config.cjs` に統一
    - 詳細は `frontend/README.md` 参照

### バックエンド（backend/）
- 主なコマンド:
    - Lint: `ruff .`
    - 型チェック: `mypy .`
    - テスト: `pytest`
- 依存管理:
    - すべて `pyproject.toml` の `[project.optional-dependencies]` で一元管理
    - `uv` コマンドでインストール・ロックファイル管理（`uv pip install -r requirements.txt` など）
- CIで実行される内容:
    - ruff（静的解析・Lint）
    - mypy（型チェック）
    - pytest（ユニットテスト）
- 注意点:
    - テスト・型チェック・Lintが全てパスしていることを確認してからPRを作成してください
    - 依存追加時は `pyproject.toml` を編集し、`uv lock` で `uv.lock` を更新
    - 詳細は `backend/` 配下のドキュメントや `pyproject.toml` 参照

### 共通の開発フロー・ルール
- ブランチ運用やPR作成の流れは `docs/development-process.md` を参照
- コミット前にLint/Format/Test/型チェックを必ず実行
- CIエラー時はエラーメッセージ・設定ファイルの重複等を確認

### 参考
- 各種詳細ルールや設定例は `docs/` 配下や各ディレクトリのREADMEを参照してください
