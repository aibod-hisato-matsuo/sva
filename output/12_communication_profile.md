# 12. Communication Profile

## 目的
系の入力通信・内部通信・出力通信を定義し、後段の性能設計、ファーム設計、基板要求に接続する。

## チャネル一覧

## Bルート入力
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
- security_requirements:
  - Bルート認証情報の保護
- notes: 速度は低く、通信品質も変動しやすい前提で設計する。

## ECHONET Lite入力/制御
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
- security_requirements:
  - 家庭内ネットワーク前提のアクセス制御
- notes: メーカー差異により取得項目・制御項目が異なる。

## 端末→クラウド同期
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
- security_requirements:
  - TLS
  - 相互認証
  - 署名または改ざん検知
- notes: クラウド断時もローカル継続を前提とする。

## クラウド→アプリ配信
- channel_id: cp_004
- boundary_type: internal
- source: cloud
- destination: user_app
- protocol: https-json-api
- communication_pattern: request_response
- expected_update_cycle: on_demand_and_push
- max_payload_size_bytes: 8192
- reliability_level: high
- timeout_ms: 3000
- retry_policy: アプリ側再取得と通知再配信で補完
- buffering_policy: 最新集計と通知状態をサーバ側保持
- security_requirements:
  - TLS
  - トークン認証
  - ユーザー権限制御
- notes: 可視化・提案・通知を扱う。

## アプリ設定→クラウド→端末
- channel_id: cp_005
- boundary_type: internal
- source: user_app
- destination: hems_controller_via_cloud
- protocol: https-json-api + edge_sync
- communication_pattern: request_response
- expected_update_cycle: on_change
- max_payload_size_bytes: 1024
- reliability_level: high
- timeout_ms: 5000
- retry_policy: クラウド側で永続化し、端末復旧後に再同期
- buffering_policy: 最後に承認された設定を正本とする
- security_requirements:
  - TLS
  - 承認操作の監査ログ
  - 権限制御
- notes: モード設定や承認操作などを想定。

## 外部出力予約領域
- channel_id: cp_006
- boundary_type: external_output
- source: cloud
- destination: reserved_external_system
- protocol: reserved
- communication_pattern: mixed
- expected_update_cycle: reserved
- max_payload_size_bytes: 0
- reliability_level: low
- timeout_ms: 0
- retry_policy: TBD
- buffering_policy: TBD
- security_requirements:
  - なし
- notes: 現フェーズでは外部出力なし。将来連携用に予約。
