#!/usr/bin/env python3
"""Rewrite all plugin-level script URLs to immutable self-hosted assets."""
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: rewrite-script-assets.py PLUGIN ASSET_COMMIT")
path = Path(sys.argv[1])
commit = sys.argv[2]
if not re.fullmatch(r"[0-9a-f]{40}", commit):
    raise SystemExit("invalid immutable asset commit")
repo = "XcvcvX/loon-independent-plugins"
prefix = f"https://raw.githubusercontent.com/{repo}/{commit}/"
text = path.read_text(encoding="utf-8")

def rewrite(url):
    marker = "raw.githubusercontent.com/XcvcvX/loon-change/main/scripts/"
    if marker in url:
        rel = url.split("/scripts/", 1)[1]
        if rel == "maidanba.js":
            rel = "first-party/maidanba.js"
        return prefix + "scripts/" + rel
    if "raw.githubusercontent.com/XcvcvX/loon-change/main/sources/amap/rucu6_amap.js" in url:
        return prefix + "scripts/first-party/rucu6_amap.js"
    m = re.match(r"https://raw\.githubusercontent\.com/ifflagged/Romeo/[0-9a-f]{40}/Modules/JavaScript/(.+)$", url)
    if m:
        return prefix + "scripts/vendor/romeo/" + m.group(1)
    m = re.match(r"https://raw\.githubusercontent\.com/devchristian1337/loon-plugins/(?:refs/heads/main|main)/Scripts/YouTube/(request|response)\.min\.js$", url)
    if m:
        return prefix + "scripts/vendor/youtube/" + m.group(1) + ".min.js"
    return url

urls = set(re.findall(r"""https?://[^ \t\r\n"'(),]+""", text))
for url in sorted(urls, key=len, reverse=True):
    new_url = rewrite(url)
    if new_url != url:
        text = text.replace(url, new_url)
path.write_text(text, encoding="utf-8")

references = set(re.findall(r"script-path=(https?://[^,\s]+)", text))
references.update(re.findall(r"""script\(\s*["'](https?://[^"']+)["']""", text))
external = [url for url in references if f"raw.githubusercontent.com/{repo}/" not in url]
if external:
    raise SystemExit("external script references remain:\n" + "\n".join(sorted(external)))
print(f"rewrote plugin assets; {len(references)} unique self-hosted references")
