# UI/UXデザインガイドライン

このガイドラインは、Harmony Study Appのユーザーインターフェース設計における基本原則とベストプラクティスを定義します。

## 1. デザインシステム

### 基本原則
- 確立されたデザインシステム（Material Design/Ant Design）を基盤として採用
- コンポーネントの再利用性と一貫性を重視
- アクセシビリティ基準（WCAG 2.1）への準拠

### 視覚要素

#### カラートークン
```css
/* Primary Colors */
--color-primary:    #2E3E7E  /* 伝統的な和声学の雰囲気を表現する深い青 */
--color-secondary:  #E6B422  /* 音楽的な活気を表現する金色 */

/* Base Colors */
--color-background: #FFFFFF  /* 白 */
--color-surface:    #F5F7FA  /* 薄いグレー */
--color-text:       #1A1A1A  /* 濃いグレー */

/* Status Colors */
--color-error:      #DC2626  /* 赤 */
--color-success:    #16A34A  /* 緑 */
--color-warning:    #F59E0B  /* オレンジ */
```

#### タイポグラフィ
```css
/* Headings */
--font-h1: 700 32px/1.5 'Noto Sans JP';  /* Bold */
--font-h2: 700 24px/1.5 'Noto Sans JP';  /* Bold */
--font-h3: 700 20px/1.5 'Noto Sans JP';  /* Bold */

/* Body Text */
--font-body-1: 400 16px/1.5 'Noto Sans JP';  /* Regular */
--font-body-2: 400 14px/1.5 'Noto Sans JP';  /* Regular */
--font-caption: 400 12px/1.5 'Noto Sans JP';  /* Regular */

/* Interactive */
--font-button: 500 14px/1.5 'Noto Sans JP';  /* Medium */
```

#### スペーシング・グリッド
```css
/* Base Grid Unit: 8px */
--spacing-xs: 4px;   /* 0.5x */
--spacing-sm: 8px;   /* 1x */
--spacing-md: 16px;  /* 2x */
--spacing-lg: 24px;  /* 3x */
--spacing-xl: 32px;  /* 4x */
```

## 2. 和声課題リストのUIパターン

### レイアウト構成
- データテーブル/リスト形式での効率的な情報表示
- 重要情報の優先的な配置
  - タイトル
  - 進捗状況
  - 期限
  - その他のメタデータ

### 情報設計
- スキャナビリティを考慮した情報の階層化
- ソート機能の実装
- フィルター機能の実装
- 検索機能の配置

## 3. アクション設計

### 優先度に基づくアクション配置
- 主要アクション
  - 新規作成ボタン → 目立つ位置に配置
  - 一括操作 → ツールバーに配置
- 二次アクション
  - 編集・削除 → 各課題のコンテキストメニューに配置
  - 詳細表示 → クリック/タップで展開

### 操作安全性
- 危険な操作（削除等）には確認ダイアログを表示
- Undo/Redo機能の実装
- 操作の取り消し可能期間の設定

## 4. レスポンシブデザイン

### モバイルファースト設計
- ブレークポイント定義
  - モバイル: 320px-767px
  - タブレット: 768px-1023px
  - デスクトップ: 1024px以上

### 表示切替
- リストビュー/グリッドビューの切り替え機能
- デバイスサイズに応じた情報量の最適化
- タッチデバイスでの操作性考慮

## 5. インタラクションとフィードバック

### 視覚的フィードバック
- 明確なホバー状態
- 明確なアクティブ状態
- ローディング状態のスケルトンUI
- 成功/エラー時のトースト通知

### アニメーション
- 自然な状態遷移
- 適度なアニメーション時間（200-300ms推奨）
- 過度なアニメーションの抑制

## 6. パフォーマンス最適化

### データ読み込み
- 無限スクロールまたはページネーションの実装
- 遅延読み込みの適用
- プリフェッチの検討

### アセット最適化
- 画像の最適化
- アイコンのスプライト化
- キャッシュ戦略の検討

## 実装時の注意点

1. コンポーネントの再利用性を常に意識する
2. アクセシビリティを初期段階から考慮する
3. パフォーマンスへの影響を監視する
4. ユーザーテストによる検証を行う
5. フィードバックに基づく継続的な改善を行う
