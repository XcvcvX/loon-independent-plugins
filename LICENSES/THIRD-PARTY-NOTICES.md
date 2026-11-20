# Third-party notices

## GPL-3.0 companion add-on

`plugins/installed-app-adblock-addon.plugin` contains a small set of app-specific ad-blocking rules adapted from the Loon modules attributed to **zirawell** in Romeo and the corresponding GPL-3.0-licensed rule collection:

- Romeo snapshot: https://github.com/ifflagged/Romeo/tree/318cef4811f8402b92cfd0a886f9ebdcf99a3732/Modules/Loon/zirawell
- Upstream rule collection: https://github.com/zirawell/R-Store/tree/d0f4dd305bade7cc6a38e3445a768d72aaea0e5b
- Upstream license: GPL-3.0 (see [GPL-3.0.txt](GPL-3.0.txt))

The companion plugin is a separate file and is provided under GPL-3.0. It contains only static domain rules and exact URL-request rejection rules. No upstream JavaScript or response-body transformation code was copied into it.

The main `plugins/independent-apps.plugin` file is a separate artifact with its own sources and is not relicensed by this notice.
