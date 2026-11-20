#!/usr/bin/env python3
"""Fail CI when an active Loon script-path cannot be fetched anonymously."""
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PLUGIN = Path("plugins/independent-apps.plugin")
text = PLUGIN.read_text(encoding="utf-8")
urls = re.findall(r"script-path=(https?://[^,\s]+)", text)
if not urls:
    raise SystemExit("FAIL: no script-path URLs found")

failed = []
for url in sorted(set(urls)):
    if not re.search(r"/[0-9a-f]{40}/", url):
        failed.append((url, "not pinned to an immutable 40-character commit"))
        continue
    last = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "loon-independent-plugins-asset-check/1.0"})
            with urllib.request.urlopen(req, timeout=25) as response:
                data = response.read(2 * 1024 * 1024 + 1)
                if response.status != 200:
                    raise RuntimeError("HTTP " + str(response.status))
                if not data:
                    raise RuntimeError("empty response")
                if len(data) > 2 * 1024 * 1024:
                    raise RuntimeError("script exceeds 2 MiB safety limit")
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
print("PASS:", len(set(urls)), "unique script assets fetched anonymously")
