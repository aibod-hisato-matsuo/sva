# 10. Data Model

## measurement_record
- entity_id: ent_001
- category: measurement
- 説明: 計測値および推定値の共通レコード。

### Fields

#### measurement_id
- data_type: string
- required: true
- source_type: system
- 説明: 計測項目ID
- example: m_004
- enum_values: なし
- notes: なし

#### timestamp
- data_type: datetime
- required: true
- source_type: system
- 説明: 計測時刻
- example: なし
- enum_values: なし
- notes: なし

#### value
- data_type: number
- required: true
- source_type: measured
- 説明: 値
- example: 78.4
- enum_values: なし
- notes: なし

#### unit
- data_type: string
- required: true
- source_type: system
- 説明: 単位
- example: %
- enum_values: なし
- notes: なし

#### source_type
- data_type: string
- required: true
- source_type: system
- 説明: 実測/推定など
- example: なし
- enum_values: measured, estimated, user_input, external_api, derived
- notes: なし

#### quality_flag
- data_type: string
- required: false
- source_type: system
- 説明: 品質フラグ
- example: なし
- enum_values: ok, estimated, missing, stale
- notes: なし

## event_record
- entity_id: ent_002
- category: event
- 説明: 停電・通信断・機器異常などのイベント。

### Fields

#### event_id
- data_type: string
- required: true
- source_type: system
- 説明: イベントID
- example: e_003
- enum_values: なし
- notes: なし

#### occurred_at
- data_type: datetime
- required: true
- source_type: system
- 説明: 発生時刻
- example: なし
- enum_values: なし
- notes: なし

#### severity
- data_type: string
- required: true
- source_type: system
- 説明: 重大度
- example: なし
- enum_values: info, warning, critical
- notes: なし

#### message
- data_type: string
- required: true
- source_type: derived
- 説明: 表示メッセージ
- example: なし
- enum_values: なし
- notes: なし

## control_command
- entity_id: ent_003
- category: command
- 説明: クラウドまたは端末が扱う制御コマンド。

### Fields

#### command_id
- data_type: string
- required: true
- source_type: system
- 説明: コマンドID
- example: cmd_battery_reserve_mode
- enum_values: なし
- notes: なし

#### target_device
- data_type: string
- required: true
- source_type: system
- 説明: 対象デバイス
- example: battery_system
- enum_values: なし
- notes: なし

#### parameters
- data_type: object
- required: false
- source_type: user_input
- 説明: 制御パラメータ
- example: なし
- enum_values: なし
- notes: なし

#### approved_by_user
- data_type: boolean
- required: false
- source_type: system
- 説明: ユーザー承認有無
- example: なし
- enum_values: なし
- notes: なし

## user_policy
- entity_id: ent_004
- category: policy
- 説明: ユーザーが選択した運用方針。

### Fields

#### policy_id
- data_type: string
- required: true
- source_type: system
- 説明: 方針ID
- example: mode_recommend
- enum_values: なし
- notes: なし

#### mode_name
- data_type: string
- required: true
- source_type: user_input
- 説明: 方針名
- example: なし
- enum_values: なし
- notes: なし

#### effective_from
- data_type: datetime
- required: false
- source_type: system
- 説明: 適用開始時刻
- example: なし
- enum_values: なし
- notes: なし

#### user_note
- data_type: string
- required: false
- source_type: user_input
- 説明: ユーザーメモ
- example: なし
- enum_values: なし
- notes: なし

## alert_notification
- entity_id: ent_005
- category: alert
- 説明: ユーザーまたは管理者向け通知。

### Fields

#### alert_id
- data_type: string
- required: true
- source_type: system
- 説明: 通知ID
- example: なし
- enum_values: なし
- notes: なし

#### channel
- data_type: string
- required: true
- source_type: system
- 説明: 通知チャネル
- example: なし
- enum_values: in_app, push, email
- notes: なし

#### title
- data_type: string
- required: true
- source_type: derived
- 説明: 通知タイトル
- example: なし
- enum_values: なし
- notes: なし

#### body
- data_type: string
- required: true
- source_type: derived
- 説明: 通知本文
- example: なし
- enum_values: なし
- notes: なし

## device_state
- entity_id: ent_006
- category: device_state
- 説明: HEMS端末または接続機器の状態。

### Fields

#### device_id
- data_type: string
- required: true
- source_type: system
- 説明: デバイスID
- example: なし
- enum_values: なし
- notes: なし

#### status
- data_type: string
- required: true
- source_type: system
- 説明: 状態
- example: なし
- enum_values: normal, degraded, offline, fault
- notes: なし

#### last_seen_at
- data_type: datetime
- required: false
- source_type: system
- 説明: 最終観測時刻
- example: なし
- enum_values: なし
- notes: なし

## sync_status
- entity_id: ent_007
- category: sync_status
- 説明: エッジとクラウドの同期状態。

### Fields

#### sync_id
- data_type: string
- required: true
- source_type: system
- 説明: 同期ID
- example: なし
- enum_values: なし
- notes: なし

#### last_sync_at
- data_type: datetime
- required: true
- source_type: system
- 説明: 最終同期時刻
- example: なし
- enum_values: なし
- notes: なし

#### sync_result
- data_type: string
- required: true
- source_type: system
- 説明: 同期結果
- example: なし
- enum_values: success, partial, failed
- notes: なし

## audit_log
- entity_id: ent_008
- category: audit_log
- 説明: 重要操作の監査ログ。

### Fields

#### log_id
- data_type: string
- required: true
- source_type: system
- 説明: ログID
- example: なし
- enum_values: なし
- notes: なし

#### actor_type
- data_type: string
- required: true
- source_type: system
- 説明: 操作者種別
- example: なし
- enum_values: user, admin, system
- notes: なし

#### action
- data_type: string
- required: true
- source_type: system
- 説明: 実行操作
- example: なし
- enum_values: なし
- notes: なし

#### action_at
- data_type: datetime
- required: true
- source_type: system
- 説明: 操作時刻
- example: なし
- enum_values: なし
- notes: なし

## derived_metric
- entity_id: ent_009
- category: derived_metric
- 説明: 日次費用やCO2削減量などの派生指標。

### Fields

#### metric_id
- data_type: string
- required: true
- source_type: system
- 説明: 指標ID
- example: なし
- enum_values: なし
- notes: なし

#### metric_name
- data_type: string
- required: true
- source_type: system
- 説明: 指標名
- example: なし
- enum_values: なし
- notes: なし

#### value
- data_type: number
- required: true
- source_type: derived
- 説明: 指標値
- example: なし
- enum_values: なし
- notes: なし

#### calculation_basis
- data_type: string
- required: false
- source_type: derived
- 説明: 算出根拠
- example: なし
- enum_values: なし
- notes: なし
