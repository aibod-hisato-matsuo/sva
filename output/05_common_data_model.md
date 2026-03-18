# 05. 共通データモデル

## チャネル
### wi-sun-b-route
- ID: ch_001
- 方向: ingress
- 説明: スマートメーターからの買電・売電・消費関連データ取得

### echonet-lite
- ID: ch_002
- 方向: bidirectional
- 説明: 太陽光発電・蓄電池の状態取得および制御

### edge-internal
- ID: ch_003
- 方向: ingress
- 説明: 端末内部推定値・中間計算値

### cloud-api
- ID: ch_004
- 方向: bidirectional
- 説明: クラウドとの同期、外部料金/通知API連携

### user-input
- ID: ch_005
- 方向: ingress
- 説明: ユーザー設定・契約料金・方針入力

## 計測値
### grid_import_power
- ID: m_001
- 区分: metering
- 単位: W
- 取得チャネル: wi-sun-b-route
- 推定許可: いいえ
- 推定フラグ必須: いいえ
- 備考: 瞬時買電電力

### grid_export_power
- ID: m_002
- 区分: metering
- 単位: W
- 取得チャネル: wi-sun-b-route
- 推定許可: いいえ
- 推定フラグ必須: いいえ
- 備考: 瞬時売電電力

### pv_generation_power
- ID: m_003
- 区分: pv
- 単位: W
- 取得チャネル: echonet-lite
- 推定許可: はい
- 推定フラグ必須: はい
- 備考: 太陽光発電出力

### battery_soc
- ID: m_004
- 区分: battery
- 単位: %
- 取得チャネル: echonet-lite
- 推定許可: いいえ
- 推定フラグ必須: いいえ
- 備考: 蓄電池残量

### battery_charge_discharge_power
- ID: m_005
- 区分: battery
- 単位: W
- 取得チャネル: echonet-lite
- 推定許可: はい
- 推定フラグ必須: はい
- 備考: 正負で充放電を表現

### estimated_daily_cost
- ID: m_006
- 区分: billing
- 単位: JPY/day
- 取得チャネル: cloud-api, user-input, edge-internal
- 推定許可: はい
- 推定フラグ必須: はい
- 備考: 契約プランと時系列消費から算出

### estimated_co2_reduction
- ID: m_007
- 区分: environmental_value
- 単位: kg-CO2/day
- 取得チャネル: cloud-api, edge-internal
- 推定許可: はい
- 推定フラグ必須: はい
- 備考: 基準係数に基づく推定値

### user_policy_mode
- ID: m_008
- 区分: user_setting
- 単位: enum
- 取得チャネル: user-input
- 推定許可: いいえ
- 推定フラグ必須: いいえ
- 備考: 見える化/提案/自動実行 など

### communication_status
- ID: m_009
- 区分: derived
- 単位: enum
- 取得チャネル: edge-internal
- 推定許可: いいえ
- 推定フラグ必須: いいえ
- 備考: 正常/劣化/断

## イベント
### power_outage_detected
- ID: e_001
- 重大度: critical
- 説明: 停電発生

### power_restored
- ID: e_002
- 重大度: info
- 説明: 停電復旧

### communication_lost
- ID: e_003
- 重大度: warning
- 説明: クラウドまたは機器との通信断

### device_fault_detected
- ID: e_004
- 重大度: critical
- 説明: PVまたは蓄電池の機器異常

### recommendation_generated
- ID: e_005
- 重大度: info
- 説明: 新しい提案が生成された

## 推定値ルール
- 推定値フラグ必須: はい
- UI区別必須: はい
- 備考: 推定値は必ずフラグを持ち、UI上で実測値と明確に区別する。
