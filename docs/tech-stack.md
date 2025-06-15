# 技術選定方針（2025年6月版）

## バックエンド
- **言語・フレームワーク**
  - Python（FastAPI推奨。API設計・拡張性・非同期対応が容易。Flaskでも可）
- **DB**
  - SQLite（ローカル開発・MVPに最適。将来はPostgreSQL等に移行も容易）
- **ORM**
  - SQLAlchemy（Python標準的。FastAPI/Flask両対応）

## フロントエンド
- **フレームワーク**
  - React（TypeScript推奨。保守性・型安全性向上）
- **UIライブラリ**
  - MUI（Material UI）やChakra UI（シンプルなUI構築が容易）
- **五線譜描画**
  - VexFlow（TypeScript/JS製。和声課題や入力内容の五線譜表示に最適）
- **ピアノ鍵盤UI**
  - 画像＋クリックマッピング、またはReact用ピアノ鍵盤コンポーネント（npmで公開されているもの）

## API通信
- **REST API**（FastAPIでAPIサーバー、Reactでフロント）

## サウンド再生
- **Tone.js**（JS/TS製。Web Audio APIラッパー。和音や音階の再生が簡単）

## 開発・運用
- **ローカル開発**：Docker（任意）、venv、npm/yarn
- **デプロイ**：ローカル→AWS（EC2, ECS, Lightsail等）を想定。GCPも比較検討可
- **バージョン管理**：GitHub

## 今後の拡張性
- モバイル対応：Reactのレスポンシブ設計＋PWA化も視野
- ユーザー認証：Auth0, Firebase Auth, Cognito等
- MIDI対応：Web MIDI API（JS/TSで利用可）

---

### 推奨構成まとめ

- バックエンド：**FastAPI（Python）＋SQLAlchemy＋SQLite**
- フロントエンド：**React（TypeScript）＋MUI or Chakra UI＋VexFlow＋Tone.js**
- API通信：**REST API**
- サウンド：**Tone.js**
- デプロイ：**ローカル→AWS（将来的に）**
- バージョン管理：**GitHub**
