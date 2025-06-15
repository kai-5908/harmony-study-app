# ADR: 和声課題データの永続化層設計

## ステータス
承認済み

承認日: 2025-06-15
決定者: プロジェクトオーナー

## コンテキスト
- MVP段階で和声課題データを永続的に保存・読み込みできる仕組みが必要
- 将来的なWeb API化やDB移行を見据えた設計が望ましい
- プロジェクトの開発思想（「関心の分離」「誤用しにくい設計」「モジュール化」）に従う必要がある

## 決定事項

### 1. 永続化方式: JSONファイル
- **決定理由**:
  - MVPの要件（データの保存・読み込み）を最小限の複雑さで満たせる
  - Pydantic/TypeScriptのシリアライズ機能と相性が良い
  - ファイルベースで人間が読み書き可能、デバッグや初期データ作成が容易
  - SQLiteと比較して、スキーママイグレーション等の複雑さがない
  - 課題データは頻繁な更新がなく、トランザクション管理の必要性が低い

### 2. アーキテクチャ: レイヤードアーキテクチャ + リポジトリパターン
```
Domain Layer
    │
Repository Layer (Interface)
    │
Infrastructure Layer
```

- **構成要素**:
  1. ドメイン層
     - `HarmonyTask`、`HarmonyAnswer` などのモデルクラス（既存）
  2. リポジトリ層
     - インターフェース: `HarmonyTaskRepository`
     - 抽象メソッド: `save`, `load`, `list`, `delete` など
  3. インフラ層
     - 実装クラス: `JsonHarmonyTaskRepository`
     - ファイルI/O、シリアライズ処理の実装

- **決定理由**:
  - 関心の分離が明確（ドメインロジック、永続化インターフェース、実装の分離）
  - 将来的なDB移行やWeb API化が容易（実装クラスの差し替えで対応可能）
  - テスト容易性（インターフェースを利用したモック化が可能）

### 3. エラーハンドリング戦略
- カスタム例外クラスの定義
  ```python
  class PersistenceError(Exception): pass
  class FileNotFoundError(PersistenceError): pass
  class ValidationError(PersistenceError): pass
  ```
- Result型パターンの採用（エラーを戻り値として表現）
  ```typescript
  type Result<T, E> = Success<T> | Failure<E>;
  ```

- **決定理由**:
  - エラーの種類と原因を明確に特定可能
  - 呼び出し元でのエラーハンドリングが強制される
  - 開発思想の「エラーは早く・目立つ形で失敗させる」に合致

### 4. シリアライズ戦略
- Python: Pydanticの機能を活用
  ```python
  class HarmonyTask(BaseModel):
      model_config = ConfigDict(json_encoders={...})
  ```
- TypeScript: カスタムシリアライザ + 型安全性
  ```typescript
  interface Serializer<T> {
    serialize(data: T): string;
    deserialize(data: string): T;
  }
  ```

- **決定理由**:
  - 既存のモデル定義との整合性維持
  - バリデーションとシリアライズの一体化
  - 型安全性の確保

### 5. JSONデータ構造例
```json
{
  "tasks": [
    {
      "id": "task001",
      "description": "バスが与えられた和声課題（バロック様式）",
      "title": "バロック課題 #1",
      "difficulty": "normal",
      "tags": ["baroque", "given-bass"],
      "score": {
        "type": "musicxml",
        "data": "scores/task001/score.musicxml"
      },
      "answer": [
        {
          "type": "musicxml",
          "data": "answers/task001/answer1.musicxml"
        },
        {
          "type": "musicxml",
          "data": "answers/task001/answer2.musicxml"
        }
      ]
    }
  ],
  "metadata": {
    "version": "1.0",
    "lastUpdated": "2025-06-15T10:00:00Z",
    "totalTasks": 1
  }
}
```

このJSONデータ構造の特徴:
- タスクの配列とメタデータを含むルート構造
- 各タスクは必須フィールド（id, description, score, answer）と任意フィールド（title, difficulty, tags）を持つ
- スコアと解答は、データのパスまたは直接のデータを格納可能
- メタデータセクションでバージョン管理やタスク数の追跡が可能

### 6. MusicXML構造例
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
  <movement-title>Harmony Exercise - Given Bass</movement-title>
  <identification>
    <creator type="composer">Harmony Study App</creator>
    <encoding>
      <software>Manual Example</software>
      <encoding-date>2025-06-15</encoding-date>
    </encoding>
  </identification>
  <part-list>
    <score-part id="P1">
      <part-name>Soprano</part-name>
    </score-part>
    <score-part id="P2">
      <part-name>Alto</part-name>
    </score-part>
    <score-part id="P3">
      <part-name>Tenor</part-name>
    </score-part>
    <score-part id="P4">
      <part-name>Bass</part-name>
    </score-part>
  </part-list>
  <part id="P1">
    <measure number="1">
      <attributes>
        <divisions>1</divisions>
        <key>
          <fifths>0</fifths>
          <mode>major</mode>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step>C</step>
          <octave>5</octave>
        </pitch>
        <duration>4</duration>
        <type>whole</type>
      </note>
    </measure>
  </part>
  <!-- 他のパート (Alto, Tenor) も同様の構造 -->
  <part id="P4">
    <measure number="1">
      <attributes>
        <divisions>1</divisions>
        <key>
          <fifths>0</fifths>
          <mode>major</mode>
        </key>
        <time>
          <beats>4</beats>
          <beat-type>4</beat-type>
        </time>
        <clef>
          <sign>F</sign>
          <line>4</line>
        </clef>
      </attributes>
      <note>
        <pitch>
          <step>C</step>
          <octave>3</octave>
        </pitch>
        <duration>4</duration>
        <type>whole</type>
      </note>
    </measure>
  </part>
</score-partwise>
```

このMusicXML構造の特徴:
1. **基本情報**
   - バージョン: MusicXML 4.0
   - エンコーディング: UTF-8
   - メタデータ（タイトル、作成者、作成日）

2. **パート構成**
   - 4声体和声用の4つのパート定義
   - 各パートにID（P1～P4）と名前を付与
   - ソプラノ、アルト、テナー、バスの標準的な配置

3. **記譜情報**
   - 調号（key）: C durの場合は fifths=0
   - 拍子（time）: 4/4拍子の例
   - 適切な音部記号（ト音記号・ヘ音記号）

4. **音符データ**
   - pitch要素で音高を指定（step: 音名, octave: オクターブ）
   - duration, typeで音価を指定
   - 臨時記号や装飾音符にも対応可能

注: 実際の和声課題では、通常複数の小節が含まれ、より複雑な音楽的要素（強弱記号、アーティキュレーション等）も含まれる可能性があります。

## 影響範囲
- 新規作成されるファイル:
  - `backend/repositories/harmony_task_repository.py`
  - `backend/repositories/json_harmony_task_repository.py`
  - `frontend/src/repositories/harmonyTaskRepository.ts`
  - `frontend/src/repositories/jsonHarmonyTaskRepository.ts`
- テストファイル:
  - `backend/tests/repositories/test_json_harmony_task_repository.py`
  - `frontend/src/__tests__/repositories/jsonHarmonyTaskRepository.test.ts`
- 設定ファイル:
  - アプリケーション設定にJSONファイルの保存パスを追加

## 代替案

### 1. SQLiteの採用
- **メリット**:
  - リレーショナルデータ構造の活用
  - トランザクション管理
  - SQL練習の機会
- **デメリット**:
  - MVPには過剰な機能
  - スキーマ管理・マイグレーションの複雑さ
  - 開発効率の低下

### 2. 単純なファイル読み書き
- **メリット**:
  - 実装の単純さ
  - 学習コストの低さ
- **デメリット**:
  - コードの再利用性の低下
  - 将来の拡張性の制限
  - エラーハンドリングの不十分さ

### 3. NoSQL（LevelDB等）の採用
- **メリット**:
  - キーバリューストアの単純さ
  - 高速なアクセス
- **デメリット**:
  - 追加の依存関係
  - 過剰な機能セット
  - デバッグの複雑さ

## 妥協点
- JSONファイルでの管理は、データ量が増えた場合にパフォーマンス面での課題が出る可能性がある
- 同時アクセス制御が必要な場合は、追加の仕組みが必要
- ファイルパスの管理や権限の考慮が必要

## 参考文献
- [リポジトリパターン](https://martinfowler.com/eaaCatalog/repository.html)
- [Result型パターン](https://fsharpforfunandprofit.com/rop/)
