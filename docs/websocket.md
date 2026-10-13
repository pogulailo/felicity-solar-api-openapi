# WebSocket (real-time energy flow)

Besides the REST API, the app opens JSON text WebSockets for live energy-flow data. This is **not** part of
`openapi.yaml` because OpenAPI 3.0 cannot describe WebSockets.

Base: `wss://shine-api.felicitysolar.com`

| Path | Purpose |
|---|---|
| `/socket/energy-flow/{deviceSn}` | Energy flow of one device |
| `/socket/energy-plant-flow/{plantId}` | Energy flow of a plant |
| `/socket/device-template-flow/{p1}/{p2}/{lang}` | Floating-window flow of a device template; `p1`/`p2` are two ids from the UI state, `lang` is the locale code |

* The handshake carries no `Authorization`, `Node` or `lang` headers and no auth message is sent afterwards.
* After connecting, the app periodically sends a command frame to request/refresh data and receives pushed JSON
  frames:
  * device: `{"type":"command","deviceCommand":{"deviceSn":"...","collectorSn":"..."}}`
  * plant: `{"type":"command","plant":true}` (optionally with a `deviceCommand`)
* Frame field names and units are not documented here; capture a few frames from your own device to inspect them.
