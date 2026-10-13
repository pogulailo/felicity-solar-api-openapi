# Changelog

All notable changes to this specification are documented here. The version number follows the app version the
spec was derived from.

## [4.1.0] - 2026-10-14

### Added
- Initial public release: 246 paths and ~490 schemas covering authentication, plants, devices, realtime and
  history data, commands and settings, alarms, messages, finance, points, service orders and eco strategies.
- Documentation of authentication, password encryption, captcha, envelope codes and pagination.
- WebSocket notes and methodology.

### Fixed
- Push-token request field is `fcmToken` (was documented as `channel`).
- `/aliyun/file/other_upload` accepts repeated `file` parts.
- `Node` header is only sent by a few calls; `lang` carries locale codes such as `en_US`.
