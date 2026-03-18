# 21. バックエンド（クラウド）仕様書（たたき台）

## 1. 文書情報
- project: i-Power Engine
- version: 0.1.0
- document_type: cloud_backend_spec
- status: draft

## 2. 目的
クラウドは、HEMSコントローラから取得したデータを蓄積・集計し、ユーザー向け可視化、提案生成、通知連携、運用監視を担う。

## 3. 責務
- データ蓄積
- 可視化向け集計
- 提案生成
- モード管理
- 通知配信
- 運用監視支援
- 監査ログ保持

## 4. 機能要件
### 時系列蓄積
- capability_id: cap_cloud_001
- category: storage
- availability: required
- 説明: 取得データを時系列で保存する。
- 関連計測: m_001, m_002, m_003, m_004, m_005
- 関連コマンド: なし
- 更新周期: なし
- プロトコル: なし
- 制約:
- なし
- 障害時挙動: なし

### 提案生成
- capability_id: cap_cloud_002
- category: analytics
- availability: required
- 説明: 節約や備えに関する提案を生成する。
- 関連計測: なし
- 関連コマンド: なし
- 更新周期: なし
- プロトコル: なし
- 制約:
- 提案根拠を説明可能にする
- 障害時挙動: なし

### 通知配信
- capability_id: cap_cloud_003
- category: communication
- availability: preferred
- 説明: 提案や異常をユーザーへ通知する。
- 関連計測: なし
- 関連コマンド: なし
- 更新周期: なし
- プロトコル: なし
- 制約:
- なし
- 障害時挙動: なし

## 5. 関連ユースケース
### ユーザーが家庭エネルギー状態を確認する
- usecase_id: uc_001
- goal: PV・蓄電池・買電/売電の現在値と推移を理解する
- actors: user, user_app, cloud, edge_controller, smart_meter, pv_system, battery_system
- 前提条件:
- HEMS端末が機器と接続済みである
- 少なくとも1つ以上の計測チャネルが有効である
- 事後条件:
- ユーザーは実測/推定を区別して状態把握できる
- データは履歴として参照可能である

### ユーザーが節約提案を確認し設定する
- usecase_id: uc_002
- goal: 契約料金・発電状況・蓄電池状態に応じた推奨を受け取り、モードを選択する
- actors: user, user_app, cloud, external_api, battery_system
- 前提条件:
- ユーザー契約情報が登録されている
- 料金関連情報または既知の料金テーブルが利用可能である
- 事後条件:
- ユーザー方針が保存される
- 次回以降の提案・制御に反映される

### 停電リスク時に備え優先へ移行する
- usecase_id: uc_003
- goal: 停電・災害リスクがある場合に蓄電池残量確保を優先する
- actors: cloud, edge_controller, user_app, battery_system, external_api
- 前提条件:
- 備え優先ポリシーが有効化可能である
- 蓄電池制御機能が利用可能である
- 事後条件:
- 備え優先の運転方針が適用される
- ユーザーは変更理由を理解できる

## 6. データ仕様
### measurement_record
- entity_id: ent_001
- category: measurement
- 説明: 計測値および推定値の共通レコード。
- 主なフィールド:
  - measurement_id (string, required=true, source=system)
  - timestamp (datetime, required=true, source=system)
  - value (number, required=true, source=measured)
  - unit (string, required=true, source=system)
  - source_type (string, required=true, source=system)
  - quality_flag (string, required=false, source=system)

### event_record
- entity_id: ent_002
- category: event
- 説明: 停電・通信断・機器異常などのイベント。
- 主なフィールド:
  - event_id (string, required=true, source=system)
  - occurred_at (datetime, required=true, source=system)
  - severity (string, required=true, source=system)
  - message (string, required=true, source=derived)

### control_command
- entity_id: ent_003
- category: command
- 説明: クラウドまたは端末が扱う制御コマンド。
- 主なフィールド:
  - command_id (string, required=true, source=system)
  - target_device (string, required=true, source=system)
  - parameters (object, required=false, source=user_input)
  - approved_by_user (boolean, required=false, source=system)

### user_policy
- entity_id: ent_004
- category: policy
- 説明: ユーザーが選択した運用方針。
- 主なフィールド:
  - policy_id (string, required=true, source=system)
  - mode_name (string, required=true, source=user_input)
  - effective_from (datetime, required=false, source=system)
  - user_note (string, required=false, source=user_input)

### alert_notification
- entity_id: ent_005
- category: alert
- 説明: ユーザーまたは管理者向け通知。
- 主なフィールド:
  - alert_id (string, required=true, source=system)
  - channel (string, required=true, source=system)
  - title (string, required=true, source=derived)
  - body (string, required=true, source=derived)

### device_state
- entity_id: ent_006
- category: device_state
- 説明: HEMS端末または接続機器の状態。
- 主なフィールド:
  - device_id (string, required=true, source=system)
  - status (string, required=true, source=system)
  - last_seen_at (datetime, required=false, source=system)

### sync_status
- entity_id: ent_007
- category: sync_status
- 説明: エッジとクラウドの同期状態。
- 主なフィールド:
  - sync_id (string, required=true, source=system)
  - last_sync_at (datetime, required=true, source=system)
  - sync_result (string, required=true, source=system)

### audit_log
- entity_id: ent_008
- category: audit_log
- 説明: 重要操作の監査ログ。
- 主なフィールド:
  - log_id (string, required=true, source=system)
  - actor_type (string, required=true, source=system)
  - action (string, required=true, source=system)
  - action_at (datetime, required=true, source=system)

### derived_metric
- entity_id: ent_009
- category: derived_metric
- 説明: 日次費用やCO2削減量などの派生指標。
- 主なフィールド:
  - metric_id (string, required=true, source=system)
  - metric_name (string, required=true, source=system)
  - value (number, required=true, source=derived)
  - calculation_basis (string, required=false, source=derived)

## 7. API/内部機能の観点
- Edge からのデータ受信API
- ユーザーアプリ向け参照API
- モード設定API
- 提案取得API
- 通知生成/配信連携
- 運用監視API
- 監査ログ参照機能

## 8. 障害時動作
- Edge 側の継続動作を前提とし、復旧後に差分同期する。
- 提案生成が停止しても、可視化と履歴参照は可能な限り維持する。
- 外部APIが異常な場合は、暫定値や既知値を用いて推定扱いで表示する。

## 9. セキュリティ・監査
- 認証・認可を分離する。
- 閲覧系と制御系の権限を分離する。
- ユーザー・管理者・システム操作を監査ログへ記録する。
- 提案や制御判断の根拠を追跡できるようにする。

## 10. 非機能要件
### 通信断時継続性
- nfr_id: nfr_001
- category: availability
- requirement: クラウド接続断が発生しても端末は最低限の安全動作を継続できること。
- target_value: 主要安全機能はローカル継続
- verification_method: ネットワーク遮断試験

### 実測/推定区分
- nfr_id: nfr_002
- category: data_quality
- requirement: 推定値は必ずフラグを持ち、UI上で実測値と明確に区別されること。
- target_value: 100%識別可能
- verification_method: UIレビューおよびAPI検証

### 機器・クラウド間セキュリティ
- nfr_id: nfr_003
- category: security
- requirement: 端末・クラウド間の通信は認証され、改ざん耐性を持つこと。
- target_value: 相互認証および暗号化通信
- verification_method: セキュリティレビュー・ペネトレーション試験

### 提案の説明可能性
- nfr_id: nfr_004
- category: ux
- requirement: 提案表示には根拠と期待効果を併記し、ユーザーが理由を理解できること。
- target_value: 主要提案100%に根拠表示
- verification_method: UXレビュー

### OTA更新の安全性
- nfr_id: nfr_005
- category: ota
- requirement: OTA更新は失敗時にロールバック可能であり、更新中に危険側へ遷移しないこと。
- target_value: 失敗時ロールバック
- verification_method: OTA障害注入試験

## 11. リスク・留意事項
### 推定値が実測値のように誤解される
- risk_id: r_002
- category: data_integrity_quality
- probability: medium
- impact: high
- priority: ★★★★☆
- mitigation: 推定フラグ、UI区別、注釈、提案根拠表示を必須化する。
- poc_validation: UXモックで認知負荷テストを行う。

### 遠隔制御経路のセキュリティ不足
- risk_id: r_005
- category: security
- probability: medium
- impact: critical
- priority: ★★★★★
- mitigation: 権限分離、監査ログ、相互認証、制御系と閲覧系の責務分離を行う。
- poc_validation: 権限逸脱シナリオのセキュリティ試験を行う。

## 12. 未決事項
- API詳細設計
- DB論理設計 / 物理設計
- データ保持期間
- 通知基盤の採用方式
- 提案ロジックのバージョン管理
