# ADR: 和声課題データモデル設計

## 文書の目的
和声課題（問題・解答・譜例・メタ情報）を一貫して管理・拡張できるデータモデルの設計方針を記録する。

## 背景
- 今後のUI・採点ロジック・永続化・拡張（複数解答・タグ付け等）に耐えうる柔軟なモデルが必要
- Python/TypeScript両方で扱える構造とする

## 要件
- 必須属性: ID, 問題文, 譜例, 解答
- 任意属性: タイトル, 難易度, タグ, 複数解答
- 譜例・解答は五線譜で表示できること（MVPは画像URLやBase64、将来はMusicXML/JSON等も拡張可能な構造）
- バリデーションはMVPでは必須項目のみ
- データ量は10万件未満を想定
- 拍子・調性・音符の多様性に対応

## モデル設計方針
- "譜例"・"解答"は柔軟な型（例: 画像URL, JSON, MusicXML等）で保持し、型情報で区別できるようにする
- 難易度・タグ・複数解答はOptional
- Python: Pydanticモデルで型・バリデーションを実装
- TypeScript: interface/typeで型定義

## モデル構造（共通イメージ）
```yaml
HarmonyTask:
  id: string
  title: string (optional)
  description: string
  score: ScoreData
  answer: AnswerData | AnswerData[]
  difficulty: string (optional)
  tags: string[] (optional)

ScoreData:
  type: "image" | "musicxml" | "json" | ...
  data: string (URL, Base64, XML, JSON等)

AnswerData:
  type: "image" | "musicxml" | "json" | ...
  data: string
```

## 今後の拡張例
- answerを配列化し複数解答に対応
- tags/difficultyをenum化
- ScoreData/AnswerDataのtype追加（例: MIDI, SVG等）

## 採用理由
- 柔軟な型で将来の拡張・多様な譜例/解答形式に対応しやすい
- Python/TypeScript両方で同じ構造を表現しやすい
- バリデーション・型安全性も担保できる

## 却下案
- "譜例"・"解答"を画像URLやテキストに固定 → 将来の拡張性に乏しいため

---

このADRに基づき、Python/TypeScript両方でHarmonyTaskモデルを実装する。
