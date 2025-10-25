# 開発タスク一覧（初期版）

本書は `docs/project/development-plan.md` をタスクレベルに分解した運用用のバックログです。  
GitHub Projects / Issues に登録する際のテンプレートとして利用してください。  
タスクIDは暫定ですので、実際のIssue番号に置き換えて構いません。

## 記法

- **ID**: フェーズ略称（PH0, PH1…）と連番。
- **カテゴリ**: `Backend`, `Frontend`, `DX`, `Docs`, `UX`, `Domain` など。
- **粒度**: 1タスクは原則1〜2日で終わる大きさを想定。
- **依存**: 先に完了させたいタスクID。複数可。

## フェーズ0: 足場固め

| ID | カテゴリ | タスク内容 | 成果物 | 依存 |
| --- | --- | --- | --- | --- |
| PH0-01 | DX | WSL2上で `npm ci` を実行し、`package-lock.json` と整合する環境を作る。失敗時はドキュメント化 | 手順メモ or docs更新 | - |
| PH0-02 | Frontend | `npm run build` が通るよう `HarmonyTaskListHeader` の props 未接続 (`onSortChange`, `onFilterChange`) を実装 | PR, 単体テスト更新 | PH0-01 |
| PH0-03 | Frontend | ルーティングを `MemoryRouter` から `BrowserRouter` へ移行し、ブラウザ履歴が使えることを確認 | PR + 動作確認記録 | PH0-02 |
| PH0-04 | Frontend | 不要な `*.ts.new` など重複ファイルを削除し、`git rm` + 追加テストでビルドが問題ないことを確認 | PR | PH0-02 |
| PH0-05 | Frontend | `HarmonyTaskListHeader` のフィルター／ソートUIが呼び出されていないため、ステートとハンドラを `HarmonyTaskList` に追加（現段階は状態保持のみでOK） | PR + Vitest | PH0-02 |
| PH0-06 | Backend | JSONリポジトリを利用するサービス層（例: `services/task_service.py`）を作成し、FastAPIルーターから利用する形に整理 | PR + pytest | - |
| PH0-07 | Backend | サンプル課題データを `backend/data` に追加・整備し、`json` スキーマ検証テストを作成 | データ更新 + pytest | PH0-06 |
| PH0-08 | Docs | フロント・バックエンドの起動手順（WSL/Windows両対応）を `README.md` か `docs/development/development-guidelines.md` に追記 | ドキュメント更新 | PH0-01 |
| PH0-09 | DX | GitHub Actions（存在する場合）でフロントビルド/テストをWSLまたはLinuxで走らせるようワークフロー追加 | `.github/workflows` 更新 | PH0-01 |

## フェーズ1: MVP完成

| ID | カテゴリ | タスク内容 | 成果物 | 依存 |
| --- | --- | --- | --- | --- |
| PH1-01 | Backend | 禁則判定用ドメインサービスの設計ADR作成（対象ルール、入力形式、出力形式を定義） | `docs/ADR/` へのADR | PH0-06 |
| PH1-02 | Backend | 禁則ロジック第1弾実装（例: 並行5度/8度、13音問題）とユニットテスト | サービスコード + pytest | PH1-01 |
| PH1-03 | Backend | 課題提出API（POST `/api/tasks/{task_id}/submissions`）を実装し、評価結果JSONを返却 | FastAPIルート + テスト | PH1-02 |
| PH1-04 | Frontend | 禁則評価APIに対応するリポジトリ/フックを実装し、提出フォームから呼び出す | Reactコンポーネント + テスト | PH1-03 |
| PH1-05 | Frontend | 音入力UI PoC: 五線譜表示ライブラリ候補( VexFlow, OpenSheetMusicDisplay 等 )を比較する ADR を作成 | ADR + 比較表 | PH0-05 |
| PH1-06 | Frontend | 選定した譜面ライブラリで課題譜面を描画するコンポーネントを実装 | コンポーネント + Storybook/Vitest | PH1-05 |
| PH1-07 | Frontend | 鍵盤UI（クリック操作で音入力）を実装し、音名入力→API送信まで繋ぐ | コンポーネント + テスト | PH1-04 |
| PH1-08 | Backend | ユーザー解答データ保存のための永続化層検討（JSON継続 or DB移行）のADR作成 | ADR | PH1-03 |
| PH1-09 | DX | Playwright または Cypress で「課題一覧→詳細→解答送信→評価結果表示」のE2Eテスト整備 | E2Eテスト + CI設定 | PH1-04 |
| PH1-10 | Docs | 評価アルゴリズムの使い方ドキュメント（入力形式、返却値、例）を `docs/domain/` に追加 | ドメイン資料更新 | PH1-03 |

## フェーズ2: UX向上・拡張

| ID | カテゴリ | タスク内容 | 成果物 | 依存 |
| --- | --- | --- | --- | --- |
| PH2-01 | Backend | 課題フィルタリングAPI（難易度・タグ・ステータス）実装 | API + pytest | PH1-03 |
| PH2-02 | Frontend | フィルタリング/ソートUIとAPIを接続し、結果をリストに反映 | React更新 + テスト | PH2-01 |
| PH2-03 | Backend | 学習履歴と進捗ステータス管理（ユーザー識別の方式を含む）を実装 | モデル/リポジトリ + テスト | PH1-08 |
| PH2-04 | Frontend | 課題カードに進捗ステータス表示と更新UIを追加 | React更新 + テスト | PH2-03 |
| PH2-05 | UX | 評価結果の視覚化（禁則ハイライト、推奨進行提示）UIを設計→実装 | デザイン案 + React実装 | PH1-07 |
| PH2-06 | Frontend | 音源再生（WebAudio/MIDI）機能を追加し、課題譜面と同期再生 | 機能実装 + テスト | PH1-06 |
| PH2-07 | Backend | 推奨進行ロジック／コメント生成のPoCを実装し、評価結果に同梱 | サービス + テスト | PH2-05 |
| PH2-08 | DX | デプロイ先(AWS/GCP)比較 ADR, インフラ構築スプリントの計画書作成 | ADR + 計画書 | PH0-09 |

## 継続タスク（フェーズ共通）

| ID | カテゴリ | タスク内容 | 成果物 | 備考 |
| --- | --- | --- | --- | --- |
| CT-01 | Docs | プルリクごとに `docs/ADR/` や `docs/project/` の関連資料を更新し履歴を残す | 各PR内 | 習慣化 |
| CT-02 | QA | 主要ルール追加時に回帰テストケースをE2Eに追加 | E2Eテスト増分 | PH1-02以降 |
| CT-03 | DX | フロント/バックエンドLint・テストをpre-pushで自動実行 (`husky` 更新) | Husky設定 | フェーズ0で開始 |
| CT-04 | Domain | 課題セット・評価ルールの優先順位見直しを毎スプリント実施し、`project-charter` の更新が必要なら反映 | 会議メモ + docs | PO/Domain担当 |

本リストは初期案のため、開発状況や学習成果に応じて随時見直してください。GitHub Projectsでは各タスクをカード化し、`phase` ラベル（phase0〜2）と `category` ラベルで絞り込めるようにすると運用しやすくなります。

