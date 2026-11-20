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
- MITM: 302 unique host entries (including wildcard host patterns)
- Runtime assets: 40 unique files (38 JavaScript + 2 jq), vendored or pinned to immutable commits in this repository.
- Generic GitHub request-header rewriting was removed. The bundle does not add GitHub domains to MITM.

## Independence and validation

- No R-Store base is loaded or inherited.
- All runtime script and jq dependencies are hosted in this repository and pinned to immutable commit SHAs.
- CI checks every active `script-path`, `script(...)`, and `jq_file(...)` asset with anonymous HTTPS requests. It rejects missing, empty, unpinned, oversized, or external resources.
- Static validation checks section structure, asset references, duplicate MITM declarations, and GitHub isolation.

## Device regression status

The migrated snapshot has static and public-asset checks, but it has **not yet been verified on a physical iPhone in Loon**. In particular, test Spotify launch/login/playback, Xianyu feed/search, Amap navigation/search, and other app flows before replacing an existing working setup. Device performance, battery impact, and real-world blocking effectiveness are not claimed as measured.


## Additional upstream source audit

- Audited Romeo's [Keli ad filter](https://github.com/ifflagged/Romeo/blob/318cef4811f8402b92cfd0a886f9ebdcf99a3732/Modules/Loon/fking/Beta/Remove_ads_by_keli.lpx) at immutable commit `318cef4811f8402b92cfd0a886f9ebdcf99a3732` (credited to 可莉).
- Its 24 Rule lines contain one duplicate; all 23 unique rules are already covered by the current bundle. The `sdkconfig.ad.xiaomi.com` rule is already covered by the existing `ad.xiaomi.com` suffix rule.
- All 82 Rewrite entries are already present, so no duplicate Rule or Rewrite entries were added.
- MITM was consolidated from two exact Mi Fit hosts into `api-mifit*.huami.com`, matching the source's broader URL matchers while reducing the declaration count from 303 to 302. Nine other source MITM declarations were not imported because this source's Rule/Rewrite sections do not reference them.

## Attribution

Original script headers and author notices are retained. Preserve upstream attribution and applicable licenses when redistributing.

## Installed-app coverage supplement

A second, standalone low-overhead companion plugin was added from the installed-app audit:

`https://raw.githubusercontent.com/XcvcvX/loon-independent-plugins/main/plugins/installed-app-adblock-addon.plugin`

- 5 domain rules, 20 exact request URL filters, 14 unique MITM hosts.
- No JavaScript, no response-body parsing, and no broad catch-all app rules.
- Covers selected ad endpoints for Meituan/Meituan Waimai, Ctrip, Fliggy, Didi, Baidu Maps, Baidu Netdisk, Cainiao, PICC, Tuhu and China Construction Bank.
- This companion is a separate GPL-3.0 artifact derived from zirawell's R-Store ad-block rules. Its attribution and license are in `LICENSES/`.
- The original primary plugin is unchanged. Install the companion as a second Loon plugin if these additional app filters are needed.

See [the installed-app matching audit](sources/installed-app-match-audit.md) for Bundle ID matching, upstream priority results, skipped modules, and the reason high-cost body scripts were excluded.
