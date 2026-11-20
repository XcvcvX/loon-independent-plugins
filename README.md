# Loon Independent Plugins

A standalone Loon plugin snapshot assembled from independent app-specific sources. This build does **not** use the R-Store base plugin, inherited R-Store rules, or R-Store base MITM declarations.

## Install

Raw subscription URL:

`https://raw.githubusercontent.com/XcvcvX/loon-independent-plugins/main/plugins/independent-apps.plugin`

The bundle is a no-base extraction from the source project. It contains independent app rules from Romeo (including Kelee and other credited components), RuCu6 Amap, zirawell AlipayAdBlock, ddgksf2013 GuaZiVideoAds, and YouTube enhancement sources. Original script author notices are retained.

## Bundle inventory

- Argument: 18 entries
- Rule: 719 entries
- Rewrite: 563 entries
- Script: 80 entries
- MITM: 303 unique host entries (including one wildcard host)
- Runtime assets: 40 unique files (38 JavaScript + 2 jq), vendored or pinned to immutable commits in this repository.
- Generic GitHub request-header rewriting was removed. The bundle does not add GitHub domains to MITM.

## Independence and validation

- No R-Store base is loaded or inherited.
- All runtime script and jq dependencies are hosted in this repository and pinned to immutable commit SHAs.
- CI checks every active `script-path`, `script(...)`, and `jq_file(...)` asset with anonymous HTTPS requests. It rejects missing, empty, unpinned, oversized, or external resources.
- Static validation checks section structure, asset references, duplicate MITM declarations, and GitHub isolation.

## Device regression status

The migrated snapshot has static and public-asset checks, but it has **not yet been verified on a physical iPhone in Loon**. In particular, test Spotify launch/login/playback, Xianyu feed/search, Amap navigation/search, and other app flows before replacing an existing working setup. Device performance, battery impact, and real-world blocking effectiveness are not claimed as measured.

## Attribution

Original script headers and author notices are retained. Preserve upstream attribution and applicable licenses when redistributing.
