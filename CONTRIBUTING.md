# Contributing

Thanks for helping improve this documentation. Corrections based on **your own** observations are the most valuable.

## Ground rules

* Document only what you can support: your own account, your own devices, or analysis of the public app.
* **Never** include real tokens, passwords, e-mail addresses, phone numbers, serial numbers, plant names, or
  captured traffic containing them. Replace values with placeholders.
* Do not add vendor binaries (APKs), decompiled source, or embedded keys/secrets.
* Mark anything you have not confirmed as such in the `description` rather than guessing.

## Workflow

1. Fork and branch from `main`.
2. Edit the files in `src/` - **not** `openapi.yaml`, which is generated.
   * Endpoints live in `src/fragments/*.yaml`; shared info, servers and common schemas in `src/base.yaml`.
   * Every operation needs an `operationId` (camelCase, unique), `summary`, `description`, `tags` and responses
     wrapped with the `ApiEnvelope` schema, matching the existing entries.
   * Keep field names exactly as the server expects them, including typos.
3. Set up and run the checks:
   ```bash
   pip install -r requirements.txt
   python scripts/build.py
   openapi-spec-validator openapi.yaml
   ```
4. Commit both `src/` changes and the regenerated `openapi.yaml`, add a line to `CHANGELOG.md`, and open a pull
   request using the template.

## Reporting problems

Use the issue templates: *Spec correction* for a wrong or missing field/endpoint, *Bug report* for build or
tooling problems. For a rights-holder concern, open an issue titled "Rights holder notice".
