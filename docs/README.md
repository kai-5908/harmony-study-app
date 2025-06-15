# docs ディレクトリ構成

プロジェクトのドキュメントは以下のディレクトリ構造で管理されています：

```
docs/
  ├── development/          # 開発関連文書
  │   ├── coding-rules.md       # コーディング規約
  │   ├── development-process.md # 開発プロセス・フロー
  │   ├── development-guidelines.md # 開発ガイドライン
  │   └── design-philosophy.md  # 設計思想・原則
  │
  ├── ADR/                 # アーキテクチャ決定記録
  │   ├── adr_template.md      # ADRテンプレート
  │   └── adr_harmony_task_model.md  # 和声課題モデルのADR
  │
  ├── domain/             # ドメイン知識・定義
  │   └── harmony_domain_knowledge.md  # 和声学のドメイン知識
  │
  └── project/            # プロジェクト全般
      ├── project-charter.md    # プロジェクト憲章
      └── tech-stack.md        # 技術スタック
```

## 各ディレクトリの役割

### development/
開発に関する各種ガイドライン・規約・プロセスを格納します。
- コーディング規約
- 開発プロセス
- 設計ガイドライン
- 設計思想・原則

### ADR/
Architecture Decision Record（アーキテクチャ上の重要な決定）を記録します。
- 各機能・コンポーネントの設計決定
- 技術選定の理由
- トレードオフの検討記録

### domain/
プロジェクトのドメイン（業務）知識を整理します。
- 用語定義
- 業務ルール
- 概念モデル

### project/
プロジェクト全般に関する文書を管理します。
- プロジェクト憲章
- 技術スタック
- ロードマップ
