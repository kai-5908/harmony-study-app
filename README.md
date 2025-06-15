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
