# Methodology

## Source

The specification was derived from the publicly distributed Felicity Solar Android app, version 4.1.0 (package
`com.felicity.solar`), by **static analysis only**: the app package was decompiled with
[jadx](https://github.com/skylot/jadx) and its networking layer, request builders and data models were read.
No vendor server was attacked, no authentication was bypassed, and no traffic of other users was observed. The
app package and decompiled sources are deliberately **not** part of this repository.

## What was extracted

* Endpoint paths from the app's URL constant table.
* HTTP method, content type, query/body fields and required-ness from the request builders.
* Response structures from the client's data classes (`@SerializedName`, field types, nesting).
* Global behaviour (headers, envelope codes, pagination, password encryption, captcha) from the HTTP layer.

## Verification performed

1. **Coverage:** every URL constant in the app was compared with the paths in the spec. All endpoints the
   app actually calls are present; the remaining constants have no call site in the release build and are omitted.
2. **Global behaviour:** headers, timeouts, envelope codes, token handling and encryption were re-read against the
   code and corrected where needed.
3. **Spot check:** about 33 endpoints across auth, plants, devices, finance and service areas were compared field
   by field with the client code. Two discrepancies were found and fixed (push-token field `fcmToken`; multi-file
   upload).

## Limits

* Behaviour that only the server knows (validation rules, enum meanings, units, rate limits) cannot be derived
  from the client. Descriptions say "not confirmed" instead of guessing.
* Nothing was exercised against the live service.
* The spec describes version 4.1.0. Later app versions may add or change endpoints.
