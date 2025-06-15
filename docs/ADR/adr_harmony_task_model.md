# 和声課題データモデル設計

## 1. タイトル
和声課題データモデルの設計・実装

## 2. ステータス
承認

## 3. コンテキスト
- 今後のUI・採点ロジック・永続化・拡張（複数解答・タグ付け等）に耐えうる柔軟なモデルが必要。
- Python/TypeScript両方で扱える構造とする。
- 4声体和声（ソプラノ・アルト・テナー・バス）に限定し、課題はソプラノまたはバスの声部1つが与えられ、実施は残り3声を作成する形式とする。

## 4. 決定
- 必須属性: ID, 問題文, 譜例, 解答
- 任意属性: タイトル, 難易度, タグ, 複数解答
- 譜例・解答は五線譜で表示できること（MVPは画像URLやBase64、将来はMusicXML/JSON等も拡張可能な構造）
- バリデーションはMVPでは必須項目のみ
- データ量は10万件未満を想定
- 拍子・調性・音符の多様性に対応
- 4声体の和声のみに対応（ソプラノ、アルト、テナー、バス）
- 課題はソプラノ、またはバスの声部１つが与えられる。実施はそれ以外の3声を作成する。
- モデル例:
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

## 5. 根拠
- 柔軟な型で将来の拡張・多様な譜例/解答形式に対応しやすい
- Python/TypeScript両方で同じ構造を表現しやすい
- バリデーション・型安全性も担保できる
- 4声体課題の教育的・実務的要請

## 6. 結果
- Python/TypeScript両方でHarmonyTaskモデルを実装する
- answerを配列化し複数解答に対応
- tags/difficultyをenum化可能な設計
- ScoreData/AnswerDataのtype追加（例: MIDI, SVG等）も容易

## 7. 参考
- Issue #2
- docs/adr_template.md

---
