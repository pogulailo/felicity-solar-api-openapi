# Authentication

All details below were derived from the Android app v4.1.0 and describe client behaviour.

## Session token

1. `POST /app/base/userlogin` (JSON) with `userName`, `password` (encrypted, see below), `version` (app version,
   e.g. `4.1.0`) and optionally `registrationId` (JPush id) and `fcmToken` (push token).
2. The response `data` (`UserEntity`) contains an opaque `token`, user and role information and `nodeList[]`.
3. Send the token unchanged in the `Authorization` header of every later request. There is **no** `Bearer` prefix.
4. There is **no refresh endpoint**. When any call returns `code: 998` (invalid, expired or logged in elsewhere), the
   app clears its session and shows the login screen; your client should log in again.

Related calls: `POST /app/base/demoUserlogin` (demo account), `POST /app/base/userLogout`,
`POST /app/base/switchUsers` (installer/agent switching to a managed account, returns a new token).

## Password encryption

Passwords are not sent in clear text. The client encrypts them with a public key embedded in the app:

| Step | Value |
|---|---|
| Algorithm | RSA, `RSA/ECB/PKCS1Padding`, 2048-bit public key |
| Chunking | plaintext split into 117-byte blocks, each encrypted separately |
| Output | ciphertext blocks concatenated, Base64 encoded (no line breaks) |

The same scheme applies to `password`, `passwordConfirm` and `oldPassword` in registration and password
change/reset calls, to the device-settings password, and to `keyword` / `switchUserId` in `switchUsers`.

The public key is part of the app package and is **not reproduced here**; extract it from your own copy of the
app if you need it.

## Captcha (SMS / e-mail codes)

Requesting a verification code is gated by a slider (block-puzzle) captcha:

1. `POST /verification/captcha/get` returns `repData.token`, `repData.secretKey` and the two images.
2. `POST /verification/captcha/check` with `pointJson` = AES-encrypted JSON of the slider position.
3. `POST /verification/code` with `captchaVerification` = AES-encrypted `token + "---" + <plain pointJson>`.

AES is `AES/ECB/PKCS7Padding` with the server-provided `secretKey` as key, output Base64 encoded.

## What is *not* there

There is no request signing (`sign`, `timestamp`, `nonce`, HMAC) and no body encryption other than the fields
above.

## Request headers

| Header | Value |
|---|---|
| `Authorization` | raw token; omitted before login |
| `lang` | locale code such as `en_US`, `zh_CN`, `de_DE`, `pl_PL`, `cs_CZ`, `es_ES`, `uk_UK`, `it_IT`, `fr_FR`, `my_MM`, `ar_SA`, `pt_BR`, `ru_RU`, `ro_RO`, `vi_VN` |
| `source` | `ANDROID` |
| `version` | app version name, e.g. `4.1.0` |
| `Node` | node code (default `INT`); sent only by a few calls such as the registration country list |

## Regions

The login response lists `nodeList[]` (`nodeCode`, `nodeName`, `apiAddress`, `mqAddress`). After a node is selected
the app uses its `apiAddress` as the base URL for all later REST calls and falls back to
`https://shine-api.felicitysolar.com` when none is stored. These addresses come from the server.
