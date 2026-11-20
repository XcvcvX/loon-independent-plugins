# Loon Independent Plugins

A standalone Loon plugin bundle built from independent app-specific sources only.

## Scope

- No R-Store base plugin, rules, rewrites, scripts, or inherited MITM declarations.
- Independent app-specific sources are reviewed and merged into a single generated Loon plugin.
- First-party scripts should be vendored in this repository and referenced through immutable commit URLs or release assets.
- Third-party script dependencies must be checked for anonymous availability before release.

## Repository layout

- `plugins/`: source app plugins and source snapshots.
- `scripts/`: locally maintained or mirrored JavaScript assets.
- `dist/`: generated distributable plugin and build reports.
- `sources/`: source manifest and provenance records.
- `.github/workflows/`: validation and build automation.

## Build and release policy

A build must fail if any active `script-path` cannot be fetched anonymously, returns an HTTP error, is empty, or references an untracked/missing local asset. The generated plugin must pass syntax/structure audits and an explicit no-R-Store-base check.

Do not treat a successful GitHub-authenticated API fetch as proof that a Loon client can anonymously download a script.

## Current status

Repository initialized. Source migration and first reproducible build are the next steps. The previous no-base preview is a starting snapshot, not yet considered production-ready: its script delivery paths still require end-to-end validation in Loon.

## License and attribution

Each imported source retains its upstream author attribution and applicable license. Do not remove source notices when mirroring or transforming scripts.
