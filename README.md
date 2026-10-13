# Felicity Solar (Shine) API - unofficial OpenAPI specification

[![Validate OpenAPI](../../actions/workflows/validate.yml/badge.svg)](../../actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![OpenAPI 3.0.3](https://img.shields.io/badge/OpenAPI-3.0.3-6BA539)

A community-maintained [OpenAPI 3.0.3](https://spec.openapis.org/oas/v3.0.3) description of the REST API used
by the **Felicity Solar "Shine"** Android app (v4.1.0), the app for Felicity Solar inverters, batteries and
monitoring plants.

> **Unofficial.** This project is not affiliated with, endorsed by or supported by Felicity Solar. The API is
> private and undocumented by its vendor and can change or disappear without notice. See [Disclaimer](#disclaimer).

## At a glance

| | |
|---|---|
| Spec | [`openapi.yaml`](openapi.yaml) (generated, 246 paths, ~490 schemas) |
| Base URL | `https://shine-api.felicitysolar.com` |
| Auth | Session token in the `Authorization` header (obtained from `POST /app/base/userlogin`) |
| Format | JSON, mostly `POST`; every response wrapped in `{code, message, data}` |
| Covered areas | Auth and accounts, plants, devices, realtime data and charts, device commands and settings, warnings, firmware updates, plant electricity prices, eco and green-power plans, messages, feedback, finance and points, service (complaint) orders |

## Quick start

1. Open [`openapi.yaml`](openapi.yaml) in [Swagger Editor](https://editor.swagger.io/), Redoc, Postman or Insomnia,
   or generate a client with [openapi-generator](https://openapi-generator.tech/).
2. Read [docs/authentication.md](docs/authentication.md) - passwords are RSA-encrypted client-side, so a plain
   login request will not work without that step.
3. Log in, then send the returned token as the raw `Authorization` header (no `Bearer` prefix).

```http
POST https://shine-api.felicitysolar.com/app/base/userlogin
Content-Type: application/json
lang: en_US
source: ANDROID
version: 4.1.0

{"userName": "<account>", "password": "<RSA+Base64 encrypted password>", "version": "4.1.0"}
```

Always check `code` in the body: HTTP status is `200` even for errors (`998` = token invalid, `1017` = maintenance).

## Repository layout

```
openapi.yaml          Generated, ready-to-use specification (do not edit by hand)
src/base.yaml         Info, servers, security schemes, shared parameters and schemas
src/fragments/*.yaml  Endpoint definitions grouped by area
scripts/build.py      Merges src/ into openapi.yaml (and checks it is up to date)
docs/                 Authentication, WebSocket and methodology notes
```

## Building

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python scripts/build.py                      # regenerate openapi.yaml
python scripts/build.py --check              # fail if openapi.yaml is stale
openapi-spec-validator openapi.yaml          # validate against the OpenAPI schema
```

## How reliable is it?

The spec was derived by static analysis of the publicly distributed app, then cross-checked: endpoint paths
against every URL the app uses, and a sample of endpoints (methods, content types, required fields, response
models) against the client code. Details are in [docs/methodology.md](docs/methodology.md).

Known limits:

* **Nothing was tested against the live service.** Server behaviour that the client does not reveal is not documented.
* **Units and enum meanings** (work modes, battery status codes, and so on) are often not stated in the client.
  Where they are unknown the description says so.
* Fields marked "not confirmed" are inferred from client models rather than observed in responses.
* Only endpoints the app **actually calls** are included. The app also contains roughly 50 unused path constants
  whose request/response shapes cannot be recovered from the client; they are intentionally omitted.
* Regional accounts may be served from a different host (`apiAddress` in the login response).

Corrections from real traffic are very welcome - see [CONTRIBUTING.md](CONTRIBUTING.md).

## Responsible use

* Use the API only with **your own account and devices**, and respect the vendor's terms of service.
* Be gentle: avoid aggressive polling, since the service is shared with other users.
* Do not use this material to access accounts or data that are not yours.
* Never commit real tokens, passwords, serial numbers or captured traffic to this repository.

## Disclaimer

This is an independent, community project created for interoperability and educational purposes. It contains no
code, binaries or credentials from the vendor. "Felicity Solar", "Shine" and related names are trademarks of their
respective owners and are used only to identify the product this documentation describes. The specification is
provided "as is" without warranty of any kind; the authors are not liable for any damage resulting from its use.
If you are a rights holder and have a concern, please open an issue.

## License

[MIT](LICENSE) (c) 2026 Andrii Pohuliailo
