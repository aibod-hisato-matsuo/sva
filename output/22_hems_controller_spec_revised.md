# 22. HEMSコントローラ（デバイス）仕様書（改訂版）

## 1. 文書情報
- project: i-Power Engine
- version: 0.2.0
- document_type: hems_controller_spec
- status: draft-revised

## 2. 目的
HEMSコントローラは、家庭内でスマートメーター、太陽光発電設備、蓄電池と接続し、差異吸収、ローカル安全動作、クラウド同期の責務を担う。
改訂版では、通信プロファイルと性能予算を反映し、通信品質、バッファ、再同期要件まで含めて定義する。

## 3. 接続対象
- スマートメーター（Bルート）
- 太陽光発電設備（ECHONET Lite）
- 蓄電池（ECHONET Lite）
- クラウド
- 保守 / 設定用インターフェース

## 4. デバイス責務
- 機器接続維持
- Wi-SUN / ECHONET Lite の吸収
- ローカルでの安全縮退
- 一部推定補助
- クラウドとの同期
- 状態監視と障害通知補助
- 通信断時のローカルキュー保持
- 復旧後の差分再同期

## 5. 通信プロファイル
### 5.1 Bルート入力
- channel_id: cp_001
- boundary_type: external_input
- source: smart_meter
- destination: hems_controller
- protocol: wi-sun-b-route
- communication_pattern: poll
- expected_update_cycle: 30s-300s
- max_payload_size_bytes: 256
- reliability_level: unstable
- timeout_ms: 5000
- retry_policy: timeout時は最大3回再試行し、失敗時は欠損マーク
- buffering_policy: 最新値優先、古い取得待ちは破棄
- notes: 速度は低く、通信品質も変動しやすい前提で設計する

### 5.2 ECHONET Lite 入力/制御
- channel_id: cp_002
- boundary_type: external_input
- source: pv_or_battery_device
- destination: hems_controller
- protocol: echonet-lite
- communication_pattern: request_response
- expected_update_cycle: 10s-60s
- max_payload_size_bytes: 512
- reliability_level: medium
- timeout_ms: 3000
- retry_policy: 取得系は2回再試行、制御系は1回のみ再送し失敗時は制御停止
- buffering_policy: 制御系コマンドは順序維持、計測系は最新値優先
- notes: メーカー差異により取得項目・制御項目が異なる

### 5.3 端末→クラウド同期
- channel_id: cp_003
- boundary_type: internal
- source: hems_controller
- destination: cloud
- protocol: https-json-api
- communication_pattern: batch_sync
- expected_update_cycle: 10s-60s
- max_payload_size_bytes: 4096
- reliability_level: high
- timeout_ms: 5000
- retry_policy: 送信失敗時はローカルキュー保持、指数バックオフで再送
- buffering_policy: 時系列データはキュー蓄積、イベントは優先送信
- security_requirements: TLS, 相互認証, 改ざん検知

## 6. 性能予算
### 6.1 買電/売電計測フロー
- flow_id: pf_001
- related_channel_id: cp_001
- average_message_size_bytes: 64
- peak_message_size_bytes: 128
- average_rate_per_sec: 0.05
- peak_rate_per_sec: 0.2
- required_latency_ms: 10000
- allowable_loss_rate_percent: 5.0
- buffer_size_bytes: 2048
- local_retention_seconds: 3600
- resync_policy: 最新値優先で時系列欠損は missing として記録

### 6.2 PV/蓄電池状態取得フロー
- flow_id: pf_002
- related_channel_id: cp_002
- average_message_size_bytes: 128
- peak_message_size_bytes: 256
- average_rate_per_sec: 0.2
- peak_rate_per_sec: 1.0
- required_latency_ms: 5000
- allowable_loss_rate_percent: 2.0
- buffer_size_bytes: 4096
- local_retention_seconds: 1800
- resync_policy: 取得失敗時は再試行し、それでも失敗なら stale/estimated へ遷移

### 6.3 端末→クラウド時系列同期
- flow_id: pf_003
- related_channel_id: cp_003
- average_message_size_bytes: 1024
- peak_message_size_bytes: 4096
- average_rate_per_sec: 0.1
- peak_rate_per_sec: 1.0
- required_latency_ms: 15000
- allowable_loss_rate_percent: 0.5
- buffer_size_bytes: 65536
- local_retention_seconds: 86400
- resync_policy: 送信失敗データをローカル保持し、復旧後バッチ再同期

### 6.4 イベント/異常通知フロー
- flow_id: pf_004
- related_channel_id: cp_003
- average_message_size_bytes: 256
- peak_message_size_bytes: 1024
- average_rate_per_sec: 0.01
- peak_rate_per_sec: 0.2
- required_latency_ms: 3000
- allowable_loss_rate_percent: 0.1
- buffer_size_bytes: 8192
- local_retention_seconds: 86400
- resync_policy: イベントは優先送信し、未送信時はFIFOキュー保持

### 6.5 OTA更新フロー
- flow_id: pf_007
- related_channel_id: cp_003
- average_message_size_bytes: 262144
- peak_message_size_bytes: 2097152
- required_latency_ms: 600000
- buffer_size_bytes: 4194304
- local_retention_seconds: 86400
- resync_policy: 分割転送・整合性検証・ロールバック前提

## 7. デバイス資源要求
- 受信バッファ: 最低 64KB（時系列同期キューを含む）
- イベント優先キュー: 最低 8KB
- OTA一時領域: 最低 4MB
- 設定 / ログ / 再送管理用の不揮発領域が必要
- 通信処理と再送制御が同時に走っても安全縮退処理を阻害しないCPU余裕が必要

## 8. フェイルセーフ
- クラウド未接続時は最後の安全設定を保持する
- 制御不能時は危険側の制御を停止し、提案表示へフォールバックする
- データ欠損は欠損または推定として扱い、実測と混同しない
- Bルート不安定時は計測欠損を許容し、系全体停止はしない
- ECHONET制御失敗時は再送を制限し、暴走的な再制御をしない

## 9. OTA / 保守
- OTA更新はロールバック可能であること
- 更新失敗時は保守運転へ移行すること
- 更新用空き領域は性能予算に基づき事前確保すること
- 設定変更・ログ取得・状態確認のための保守導線を持つこと

## 10. 未決事項
- 端末CPU/メモリ/ストレージの確定値
- 通信モジュール構成
- ローカルログ保持期間の最終決定
- OTA更新方式の詳細
- 筐体 / 設置条件
