# 13. Performance Budget

## 目的
通信路ごとのデータフローについて、データレート、遅延、欠損許容、バッファ、保持時間を定義し、端末・ファーム・基板・クラウドの性能要求に接続する。

## フロー一覧

## 買電/売電計測フロー
- flow_id: pf_001
- related_channel_id: cp_001
- data_type: measurement_record
- average_message_size_bytes: 64
- peak_message_size_bytes: 128
- average_rate_per_sec: 0.05
- peak_rate_per_sec: 0.2
- required_latency_ms: 10000
- allowable_loss_rate_percent: 5.0
- buffer_size_bytes: 2048
- local_retention_seconds: 3600
- resync_policy: 最新値優先で時系列欠損は missing として記録
- design_notes: Bルートは低頻度・不安定前提。帯域より欠損耐性が重要。

## PV/蓄電池状態取得フロー
- flow_id: pf_002
- related_channel_id: cp_002
- data_type: measurement_record
- average_message_size_bytes: 128
- peak_message_size_bytes: 256
- average_rate_per_sec: 0.2
- peak_rate_per_sec: 1.0
- required_latency_ms: 5000
- allowable_loss_rate_percent: 2.0
- buffer_size_bytes: 4096
- local_retention_seconds: 1800
- resync_policy: 取得失敗時は再試行し、それでも失敗なら stale/estimated へ遷移
- design_notes: メーカー差異に備え、プロパティごとに取得成功率を監視する。

## 端末→クラウド時系列同期
- flow_id: pf_003
- related_channel_id: cp_003
- data_type: measurement_record_batch
- average_message_size_bytes: 1024
- peak_message_size_bytes: 4096
- average_rate_per_sec: 0.1
- peak_rate_per_sec: 1.0
- required_latency_ms: 15000
- allowable_loss_rate_percent: 0.5
- buffer_size_bytes: 65536
- local_retention_seconds: 86400
- resync_policy: 送信失敗データをローカル保持し、復旧後バッチ再同期
- design_notes: 基板/端末側ではバッファと不揮発領域が必要。

## イベント/異常通知フロー
- flow_id: pf_004
- related_channel_id: cp_003
- data_type: event_record
- average_message_size_bytes: 256
- peak_message_size_bytes: 1024
- average_rate_per_sec: 0.01
- peak_rate_per_sec: 0.2
- required_latency_ms: 3000
- allowable_loss_rate_percent: 0.1
- buffer_size_bytes: 8192
- local_retention_seconds: 86400
- resync_policy: イベントは優先送信し、未送信時はFIFOキュー保持
- design_notes: 異常通知は時系列計測より低遅延を要求する。

## クラウド→アプリ可視化応答
- flow_id: pf_005
- related_channel_id: cp_004
- data_type: dashboard_payload
- average_message_size_bytes: 4096
- peak_message_size_bytes: 8192
- average_rate_per_sec: 0.05
- peak_rate_per_sec: 0.5
- required_latency_ms: 2000
- allowable_loss_rate_percent: 1.0
- buffer_size_bytes: 16384
- local_retention_seconds: 0
- resync_policy: アプリ再取得で補完、サーバ側キャッシュを活用
- design_notes: アプリUX上、体感速度を意識する。

## 設定/承認操作フロー
- flow_id: pf_006
- related_channel_id: cp_005
- data_type: control_command_or_policy_update
- average_message_size_bytes: 512
- peak_message_size_bytes: 1024
- average_rate_per_sec: 0.005
- peak_rate_per_sec: 0.05
- required_latency_ms: 5000
- allowable_loss_rate_percent: 0.0
- buffer_size_bytes: 4096
- local_retention_seconds: 604800
- resync_policy: 最後に承認された設定をクラウド正本として保持し、端末復帰時に再配信
- design_notes: 設定変更は欠落不可。監査ログと再同期が必要。

## OTA更新フロー
- flow_id: pf_007
- related_channel_id: cp_003
- data_type: firmware_package
- average_message_size_bytes: 262144
- peak_message_size_bytes: 2097152
- average_rate_per_sec: 0.0001
- peak_rate_per_sec: 0.001
- required_latency_ms: 600000
- allowable_loss_rate_percent: 0.0
- buffer_size_bytes: 4194304
- local_retention_seconds: 86400
- resync_policy: 分割転送・整合性検証・ロールバック前提
- design_notes: 基板/端末には更新用空き領域と検証処理能力が必要。

## 設計上の見方
- まず流れるデータを定義し、その次に周期・遅延・欠損許容を定義する。
- 回線速度の議論は最後であり、先に性能予算を決める。
- Bルートのような不安定低速系では、帯域より欠損耐性と再同期が重要。
- OTAやイベント通知は通常計測とは別の優先度で扱う。
