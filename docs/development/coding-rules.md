# コーディングルール

## 1. 言語ごとのスタイルガイド
- **Python**
  - PEP8に従う（ruffで自動チェック）
  - 1行の文字数上限は120文字（ruff設定に準拠）
- **TypeScript**
  - Airbnb JavaScript Style Guide（TypeScript対応）＋Prettier＋ESLintの組み合わせを推奨

## 2. 命名規則
### 2.1 使う単語の選び方（Qiita記事要約）
- 意味が明確で、誰が見ても誤解のない単語を選ぶ
- 英語として自然な単語・表現を使う（Google翻訳や英辞郎で確認）
- 略語や造語は避ける。使う場合はプロジェクト内で統一
- 単語の組み合わせは一般的な順序・文法に従う（例：getUserName, fetchData）
- ドメイン固有の用語は業界標準や公式ドキュメントに合わせる

### 2.2 表記法
- **Python**
  - 変数・関数：スネークケース（例：user_name, get_data）
  - クラス：パスカルケース（例：UserProfile）
  - 定数：全て大文字＋アンダースコア（例：MAX_COUNT）
  - モジュール・パッケージ：スネークケース
  - プライベート変数・関数：先頭にアンダースコア（例：_private_func）
- **TypeScript**
  - 変数・関数：キャメルケース（例：userName, fetchData）
  - クラス・インターフェース・型：パスカルケース（例：UserProfile, IUser）
  - 定数：全て大文字＋アンダースコア（例：MAX_COUNT）
  - ファイル名：キャメルケースまたはケバブケース（例：userProfile.ts, user-profile.ts）

## 3. コメント・docstring
- **Googleスタイルのdocstring**
  - 構造：短い説明文、引数（Args）、戻り値（Returns）、例外（Raises）、例（Examples）などを明示的に記載
  - 各セクションは空行で区切る
  - 例：
    ```python
    def func(arg1: int, arg2: str) -> bool:
        """短い説明文

        Args:
            arg1 (int): 説明
            arg2 (str): 説明

        Returns:
            bool: 説明

        Raises:
            ValueError: 条件に合わない場合

        Examples:
            >>> func(1, 'a')
            True
        """
    ```

## 4. 型安全性とエラー処理

### 4.1 型システムの利用
- **Python**
  - すべての関数・メソッドに型アノテーションを付与
  - mypyの厳格モードを使用（strict=true）
  - 型エイリアスを活用し、複雑な型は可読性を確保
  - Union型やOptional型は慎重に使用し、エッジケースを考慮
- **TypeScript**
  - strict modeを有効化
  - any型の使用は極力避ける
  - ジェネリクス型の活用で再利用性を向上
  - インターフェースと型エイリアスの使い分けを明確に

### 4.2 エッジケース処理
- **NULL/None値の処理**
  - Null安全性を常に意識
  - Optional型・Union型を使用する場合は、すべてのケースを網羅
  - 早期リターンパターンを活用し、ネストを避ける
- **エラー処理**
  - 例外クラスは具体的な粒度で定義
  - エラーメッセージは原因と対処方法を明確に
  - デバッグ情報は適切なログレベルで記録
- **入力値の検証**
  - すべての外部入力は適切にバリデーション
  - バリデーションは可能な限り型システムで強制

### 4.3 インターフェース設計
- **抽象基底クラス（ABC）の活用**
  - インターフェースは明確な責務を持つ
  - 実装クラスは単一責任の原則に従う
  - 継承階層は浅く保つ（3階層以内推奨）
- **メソッドシグネチャ**
  - パラメータは必要最小限に
  - オプショナルな引数は末尾に配置
  - 戻り値の型は具体的に指定

### 4.4 テスト駆動開発（TDD）の推奨
- エッジケースのテストを先に作成
- 型の整合性をテストで確認
- モック化する際も型安全性を確保

## 5. ドキュメンテーションの方針
- 設計上重要な決定はADR（Architecture Decision Record）として記録する
- テンプレートは `adr_template.md` を用意し、それに従う

## 6. Linter/Formatterの利用
- **Python**
  - ruffを利用し、すべてのルールを適用。無視したい規則があれば議論の上で決定
- **TypeScript**
  - ESLint（Airbnbベース推奨）＋Prettierを利用し、コード品質と整形を自動化

## 7. テスト実装のルール
- すべてのPull Requestでは、実装した関数・クラス等に対応するユニットテストの追加・修正が必須です。
    - テストが追加されていない場合、レビューで指摘し、原則としてマージ不可とします。
    - 例外的にテストが不要な場合は、PR本文で理由を明記してください。
- テストコードもコーディングルール・命名規則に従うこと。
- テストの粒度・カバレッジ目標はdevelopment-process.mdを参照。

## 8. CI/CD運用ルール
- 依存管理は `pyproject.toml` で一元管理し、dev依存（ruff, pytest等）は `[project.optional-dependencies.dev]` に明記する。
- Pythonバージョンや依存パッケージのバージョン指定は厳密に記述し、CI/CD環境とローカルで差異が出ないようにする。
- 仮想環境（venv）はCI/CDワークフロー内で明示的に作成・有効化し、`uv sync --extra dev` でdev依存も必ずインストールする。
- pytestの警告・エラーは事前にローカルで確認し、CIで失敗しないようにする。
- CIワークフロー（GitHub Actions等）では、パス指定やアクションの記法ミスに注意し、公式ガイドや他プロジェクト例を参考にする。
- CI/CDで検出された問題は、都度コーディングルールやドキュメントに反映し、運用ルールをアップデートする。
- ドキュメント（README, coding-rules.md等）と実装内容は常に同期し、ルール変更時は必ずドキュメントも修正する。

---

## TypeScript用 ESLint/Prettier 設定例

### .eslintrc.json
```json
{
  "extends": [
    "airbnb-typescript/base",
    "plugin:prettier/recommended"
  ],
  "parserOptions": {
    "project": "./tsconfig.json"
  },
  "rules": {
    "no-console": "warn",
    "import/prefer-default-export": "off"
  }
}
```

### .prettierrc
```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100
}
```

### 推奨パッケージ
- eslint
- prettier
- eslint-config-airbnb-typescript
- eslint-plugin-import
- eslint-plugin-prettier
- eslint-config-prettier
- typescript

---

