#!/usr/bin/env python3
"""Fail CI unless every active or inventoried runtime asset is anonymously downloadable."""
import re
import sys
import time
import urllib.request
from pathlib import Path

PLUGIN = Path("plugins/independent-apps.plugin")
source = PLUGIN.read_text(encoding="utf-8")
urls = set(re.findall(r"script-path=(https?://[^,\\s]+)", source))
urls.update(re.findall(r"""script\\(\\s*["'](https?://[^"']+)["']""", source))
urls.update(re.findall(r"""jq_file\\(\\s*["'](https?://[^"']+)["']""", source))

inventory_path = Path("sources/script-assets.txt")
inventory = {
    line.strip()
    for line in inventory_path.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
}
if not urls:
    raise SystemExit("FAIL: no active runtime assets found")
missing = urls - inventory
if missing:
    raise SystemExit("FAIL: active assets missing from inventory: " + ", ".join(sorted(missing)))
urls |= inventory

failed = []
for url in sorted(urls):
    if "raw.githubusercontent.com/XcvcvX/loon-independent-plugins/" not in url:
        failed.append((url, "external/non-vendored asset URL remains"))
        continue
    if not re.search(r"/[0-9a-f]{40}/", url):
        failed.append((url, "asset URL is not pinned to immutable commit"))
        continue
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "loon-independent-plugins-asset-check/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read(2 * 1024 * 1024 + 1)
                if response.status != 200:
                    raise RuntimeError("HTTP " + str(response.status))
                if not data:
                    raise RuntimeError("empty response")
                if len(data) > 2 * 1024 * 1024:
                    raise RuntimeError("asset exceeds 2 MiB safety limit")
                last = None
                print("OK", len(data), url)
                break
        except Exception as exc:
            last = str(exc)
            time.sleep(attempt + 1)
    if last:
        failed.append((url, last))
for url, reason in failed:
    print("FAIL", reason, url, file=sys.stderr)
if failed:
    raise SystemExit(1)
print("PASS:", len(urls), "unique runtime assets anonymously fetched")
