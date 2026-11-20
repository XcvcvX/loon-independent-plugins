# Installed-app ad-block source audit

Audit basis: the installed-app names and Bundle IDs supplied by the user; Romeo snapshot `318cef4811f8402b92cfd0a886f9ebdcf99a3732` (2026-11-20). Only ad-block entries were considered. Sign-in, membership, unlock, pricing, routing, and general enhancement plugins were excluded.

## Added in the companion plugin

The companion file is `plugins/installed-app-adblock-addon.plugin`. It is intentionally static: 5 domain rules, 20 exact URL request matchers, 14 MITM host declarations, and **zero scripts / zero response-body parsers**.

| Installed app | Bundle ID | Added coverage |
|---|---|---|
| 美团 | `com.meituan.imeituan` | Explicit ad domains and marketing-resource endpoint |
| 美团外卖 | `com.meituan.itakeaway` | Shared Meituan ad domains only; Romeo's separate Waimai module had hostname declarations only |
| 携程旅行 | `ctrip.com` | Ad-list request and Baidu feed-ad endpoint; the main plugin already handled one Ctrip ad endpoint |
| 飞猪旅行 | `com.taobao.travel` | Fliggy pop-resource endpoint; the existing bundle already handles its screen-resource endpoint |
| 滴滴 | `com.xiaojukeji.didi` | Homepage dialog and activity resource endpoints; no Didi response script copied |
| 百度地图 | `com.baidu.map` | Ad-config domain and one precise promoted-feed endpoint; no 80 KB protobuf/body script copied |
| 百度网盘 | `com.baidu.netdisk` | Explicit ad, welfare and activity API paths; no configuration/body script copied |
| 菜鸟 | `com.cainiao.cnwireless` | Ad-keyword, ad-feed and fly-ad endpoints; no response parser copied |
| 中国人保 | `com.picc.piccinsurance` | Startup ad-page and popup-ad endpoints; no response script copied |
| 途虎养车 | `tuhu.cn.main` | Marketing-circle and homepage-banner endpoints; no broad recommendation catch-all |
| 中国建设银行 | `com.ccb.ccbDemo` | Explicit ad-resource domain `adv.ccb.com` |

These are supplemental filters, not a claim that every ad placement in those apps is removed. The companion MITM list is limited to the exact hosts needed by its request matchers.

## Already covered by the primary plugin — do not stack another copy

- 闲鱼 — `com.taobao.fleamarket`
- 淘宝 — `com.taobao.taobao4iphone`
- 拼多多 — `com.xunmeng.pinduoduo`
- 高德地图 — `com.autonavi.amap`
- YouTube — `com.google.ios.youtube`
- Spotify — `com.spotify.client`

The source audit avoided adding duplicate or conflicting plugin copies for these apps.

## Romeo matches found but not re-hosted into the public fusion repository

### 可莉 / Kelee

Romeo contains ad-specific modules for several more installed apps, including:

- 网易邮箱大师: `Modules/Loon/Kelee/MailMaster_remove_ads.lpx`
- 京东: `Modules/Loon/Kelee/JD_remove_ads.lpx`
- 夸克: `Modules/Loon/Kelee/QuarkBrowser_remove_ads.lpx`
- 得物: `Modules/Loon/Kelee/Dewu_remove_ads.lpx`
- 微店: `Modules/Loon/Kelee/Weidian_remove_ads.lpx`
- 123云盘: `Modules/Loon/Kelee/123NetWorkDisk_remove_ads.lpx`
- 嘀嗒出行: `Modules/Loon/Kelee/DidaPincheTaxi_remove_ads.lpx`
- 酷安: `Modules/Loon/Kelee/CoolApk_remove_ads.lpx`

These were not copied or modified because the Kelee official hub explicitly prohibits scraping, secondary modification, and public redistribution. The upstream import should be done directly by the user from the source, not by re-hosting it here. The Kelee Baidu Map module is explicitly unsuitable for this user's App Store installation because it requires a signed IPA.

### ZenmoFeiShi

Romeo contains `Didichuxing.lpx`, `MeiTuanNoAd.lpx`, `Pinduoduo.lpx`, and `Youtube.lpx`. The original QX repository has no declared redistribution license and labels itself personal-use oriented, so these files were not copied into the public fusion repository.

### ddgksf2013

Romeo contains `123pan.ads.lpx`, `AmapAds.lpx`, `CainiaoAds.lpx`, `Didichuxing.lpx`, `YoutubeAds.lpx`, and `coolapk.lpx`. The upstream repository has no declared license, so no code was re-hosted. The Baidu Maps adblock file is marked as deprecated upstream and was not selected.

## Other exact-name matches excluded for lack of effective ad rules or high body-processing cost

- e充电: the zirawell Loon file contains a hostname declaration only; no active ad rule.
- 肯德基: the zirawell Loon file contains a hostname declaration only; no active ad rule.
- 美团外卖's standalone zirawell file contains only MITM host declarations; the small shared Meituan domain coverage above is kept instead.
- 得物 and 微店: the zirawell files contain hostname declarations only; the Kelee alternatives remain upstream-only.
- 建行生活: the matching zirawell module depends on response-body JavaScript; excluded from this low-overhead static batch.
- 夸克: the matching zirawell module depends on a large response-body configuration transformation; excluded.
- 酷安: the matching module touches multiple feed/detail response bodies; excluded to avoid adding high-frequency parsing.
- 百度地图's 80 KB protobuf script, Baidu Netdisk/Cainiao/Didi response scripts, and other body-processing modules were deliberately excluded from this batch.

No sign-in, VIP unlock, subscription, app-function enhancement, or unrelated traffic-routing modules were migrated.
