# Loon Independent Plugins

A standalone Loon plugin collection built from independent app-specific sources. **No R-Store base plugin, inherited R-Store rules, or R-Store base MITM declaration is included.**

## First usable bundle

- [Independent Apps plugin](plugins/independent-apps.plugin)
- Subscription URL:
  `https://raw.githubusercontent.com/XcvcvX/loon-independent-plugins/main/plugins/independent-apps.plugin`

The initial bundle currently includes Spotify, Xianyu, Qunar, and Chelaile handlers. This is a staged first release, not yet the complete migration of every independent source from the previous no-base preview. Other planned sources remain marked as pending in `sources/manifest.json`.

## Script delivery

- First-party scripts are vendored under `scripts/`.
- Plugin script URLs are pinned to an immutable Git commit, not a moving branch.
- GitHub Actions anonymously fetches every active `script-path` URL and fails on non-200, empty, oversized, or unpinned assets.
- Third-party scripts are not copied or claimed as verified until their licensing, attribution, and anonymous availability are checked.

## Install

In Loon: Configuration → Plugins → Add → paste the subscription URL above. Enable only after checking the plugin's app scope and MITM domains. Completely quit and reopen the target app to test.

## Validation status

The repository's automated anonymous-download check is the delivery gate. It does not replace on-device Loon testing. In particular, Spotify startup/playback, Xianyu feed/search, Qunar pages, and Chelaile traffic positions still require real-device regression checks.

## Attribution

Original script headers and author notices are retained. Please preserve upstream attribution and applicable licenses when redistributing.
