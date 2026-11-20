# Loon Independent Plugins

A standalone Loon plugin collection built from independent app-specific sources. No R-Store base plugin, inherited R-Store rules, or R-Store base MITM declarations are included.

## Current installable bundle

- [Independent Apps plugin](plugins/independent-apps.plugin)
- Subscription URL:
  `https://raw.githubusercontent.com/XcvcvX/loon-independent-plugins/main/plugins/independent-apps.plugin`

The currently published plugin is the staged first bundle (Spotify, Xianyu, Qunar, and Chelaile). It is not yet the complete no-base preview migration.

## Migration inventory

- 39 runtime script assets from the no-base preview have been vendored into `scripts/`.
- The vendored set includes first-party scripts, Romeo/Kelee assets, Amap/YouTube assets, and the initial four-app scripts.
- Script assets are intended to be referenced through immutable commit URLs.
- The full merged rules/plugin snapshot still needs to be published and validated against these 39 assets.

## Important build constraint

The source repository `XcvcvX/loon-change` is private. GitHub Actions in this public destination repository cannot anonymously check it out, so the cross-repository build workflow was removed rather than leaving a permanently failing pipeline or embedding private credentials. The no-base build snapshot can still be migrated using the authorized GitHub connection, then rebuilt and verified here.

## Delivery policy

- First-party and approved upstream scripts are vendored.
- Runtime URLs must point to this repository and an immutable 40-character commit.
- CI anonymously fetches every active `script-path` and `script(...)` URL, rejecting external, unpinned, empty, or unavailable assets.
- Loon device regression is still required for Spotify startup/playback, Xianyu feed/search, and other app flows.

## Attribution

Original script headers and author notices are retained. Preserve upstream attribution and applicable licenses when redistributing.
