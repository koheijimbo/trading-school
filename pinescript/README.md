# TradingView PineScript Indicators

TradingViewのマルチタイムフレーム分析インジケーター集です。LuxAlgoの高度な実装手法を参考にしています。

## 📋 プロジェクト構成

```
pinescript/
├── README.md
├── docs/
│   ├── methodology.md
│   ├── naming.md
│   └── publishing.md
├── shared/
│   ├── colors.pine
│   ├── calculations.pine
│   ├── structure.pine
│   ├── liquidity.pine
│   └── sessions.pine
├── indicators/
│   ├── 01_trend_meter.pine
│   ├── 02_mtf_bias.pine
│   ├── 03_session_map.pine
│   ├── 04_key_levels.pine
│   ├── 05_liquidity_map.pine
│   ├── 06_liquidity_sweep.pine
│   ├── 07_market_structure.pine
│   ├── 08_fvg_map.pine
│   ├── 09_entry_radar.pine
│   └── 10_risk_manager.pine
└── tests/
    ├── test_structure.md
    ├── test_fvg.md
    └── test_repaint.md
```

## 🎯 主要機能

### セッション分析 (Session Map)
- 複数セッション時間帯の高値・安値ラインの描画
- セッション範囲の可視化
- リアルタイムセッション状態表示

### マルチタイムフレームバイアス (MTF Bias)
- 15分、60分、4時間、1日の4つの時間帯の方向性分析
- BUY/SELL シグナルダッシュボード
- トレンド強度の可視化

### その他インジケーター
- トレンド判定（Trend Meter）
- 主要レベル抽出（Key Levels）
- 流動性マップ（Liquidity Map）
- FVG検出（Fair Value Gap Map）
- エントリーレーダー（Entry Radar）
- リスク管理ツール（Risk Manager）

## 📄 ライセンス

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

© 2026 - Inspired by LuxAlgo

---

詳細は [methodology.md](./docs/methodology.md) をご参照ください。
