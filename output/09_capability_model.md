# 09. Capability Model

## スマートメーター Capability
- group_id: cg_001
- target_type: smart_meter
- 説明: Bルート経由で買電・売電・一部瞬時値を取得する。

### 買電電力取得
- capability_id: cap_sm_001
- category: measurement
- availability: required
- 説明: 瞬時買電電力を取得する。
- related_measurement_ids: m_001
- related_command_ids: なし
- update_cycle: near-real-time
- protocols: wi-sun-b-route
- constraints:
- 取得粒度はメーター仕様に依存する
- failure_behavior: なし

### 売電電力取得
- capability_id: cap_sm_002
- category: measurement
- availability: required
- 説明: 瞬時売電電力を取得する。
- related_measurement_ids: m_002
- related_command_ids: なし
- update_cycle: near-real-time
- protocols: wi-sun-b-route
- constraints:
- 取得粒度はメーター仕様に依存する
- failure_behavior: なし

## 蓄電池 Capability
- group_id: cg_002
- target_type: battery_system
- 説明: ECHONET Liteで蓄電池状態を取得し、一部制御を行う。

### SOC取得
- capability_id: cap_bt_001
- category: measurement
- availability: required
- 説明: 蓄電池残量を取得する。
- related_measurement_ids: m_004
- related_command_ids: なし
- update_cycle: 1-5min
- protocols: echonet-lite
- constraints:
- なし
- failure_behavior: なし

### 充放電電力取得
- capability_id: cap_bt_002
- category: measurement
- availability: preferred
- 説明: 充放電電力を取得する。
- related_measurement_ids: m_005
- related_command_ids: なし
- update_cycle: 1-5min
- protocols: echonet-lite
- constraints:
- メーカー差異により取得不可の場合がある
- failure_behavior: なし

### 備え優先制御
- capability_id: cap_bt_003
- category: control
- availability: preferred
- 説明: 放電抑制やSOC下限制御を行う。
- related_measurement_ids: なし
- related_command_ids: cmd_battery_reserve_mode
- update_cycle: なし
- protocols: echonet-lite
- constraints:
- メーカーによって制御可能範囲が異なる
- failure_behavior: 制御不可時は提案表示へフォールバックする

## HEMSコントローラ Capability
- group_id: cg_003
- target_type: hems_controller
- 説明: 機器接続・差異吸収・ローカル安全動作を担う。

### プロトコル吸収
- capability_id: cap_edge_001
- category: communication
- availability: required
- 説明: Wi-SUN/ECHONET Lite の差異を吸収する。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: wi-sun-b-route, echonet-lite
- constraints:
- メーカー固有差分はアダプタで管理する
- failure_behavior: なし

### ローカル安全縮退
- capability_id: cap_edge_002
- category: diagnostics
- availability: required
- 説明: 通信断時に安全側動作へ移行する。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: 最後の安全設定を保持し、危険側制御を停止する

### OTA更新
- capability_id: cap_edge_003
- category: ota
- availability: preferred
- 説明: ファームウェア更新を受け付ける。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- 失敗時ロールバックが必要
- failure_behavior: なし

## クラウド Capability
- group_id: cg_004
- target_type: cloud
- 説明: 蓄積・集計・提案生成・通知連携を担う。

### 時系列蓄積
- capability_id: cap_cloud_001
- category: storage
- availability: required
- 説明: 取得データを時系列で保存する。
- related_measurement_ids: m_001, m_002, m_003, m_004, m_005
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: なし

### 提案生成
- capability_id: cap_cloud_002
- category: analytics
- availability: required
- 説明: 節約や備えに関する提案を生成する。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- 提案根拠を説明可能にする
- failure_behavior: なし

### 通知配信
- capability_id: cap_cloud_003
- category: communication
- availability: preferred
- 説明: 提案や異常をユーザーへ通知する。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: なし

## 家庭内アプリ Capability
- group_id: cg_005
- target_type: user_app
- 説明: 可視化・設定・承認を担う。

### ダッシュボード表示
- capability_id: cap_app_001
- category: ui
- availability: required
- 説明: 現在値と履歴を表示する。
- related_measurement_ids: m_001, m_002, m_003, m_004, m_005, m_006, m_007
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: なし

### モード設定
- capability_id: cap_app_002
- category: ui
- availability: required
- 説明: 見える化・提案・自動実行などのモードを設定する.
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: なし

### 提案承認
- capability_id: cap_app_003
- category: ui
- availability: preferred
- 説明: 提案の採用可否をユーザーが選択する。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: なし

## 管理者アプリ Capability
- group_id: cg_006
- target_type: admin_app
- 説明: 運用監視・障害把握・サポート補助を担う。

### 接続監視
- capability_id: cap_admin_001
- category: diagnostics
- availability: required
- 説明: 端末・クラウド・機器の接続状態を監視する。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: なし

### 障害分類表示
- capability_id: cap_admin_002
- category: ui
- availability: required
- 説明: 障害の種類と影響範囲を表示する。
- related_measurement_ids: なし
- related_command_ids: なし
- update_cycle: なし
- protocols: なし
- constraints:
- なし
- failure_behavior: なし
