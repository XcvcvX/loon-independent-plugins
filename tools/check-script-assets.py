#!/usr/bin/env python3
"""Validate the standalone Loon bundle and anonymously fetch every vendored runtime asset."""
import re
import sys
import time
import urllib.request
from pathlib import Path

PLUGIN = Path("plugins/independent-apps.plugin")
source = PLUGIN.read_text(encoding="utf-8")
expected_sections = ["Argument", "Rule", "Rewrite", "Script", "MITM"]
lines = source.splitlines()
sections = {}
for name in expected_sections:
    marker = f"[{name}]"
    if lines.count(marker) != 1:
        raise SystemExit(f"FAIL: expected exactly one {marker}")
    start = lines.index(marker) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("[") and lines[i].endswith("]")), len(lines))
    sections[name] = [line for line in lines[start:end] if line.strip() and not line.lstrip().startswith("#")]

expected_counts = {"Argument": 18, "Rule": 719, "Rewrite": 563, "Script": 80}
for name, count in expected_counts.items():
    if len(sections[name]) != count:
        raise SystemExit(f"FAIL: {name} count {len(sections[name])}, expected {count}")
if "XcvcvX/loon-change" in source:
    raise SystemExit("FAIL: private source repository reference remains")
if "Script-Hub-Org_replace-header.js" in source:
    raise SystemExit("FAIL: generic GitHub header rewrite remains")

host_line = next((line for line in sections["MITM"] if line.strip().lower().startswith("hostname") and "=" in line), None)
if not host_line:
    raise SystemExit("FAIL: MITM hostname declaration missing")
hosts = [host.strip() for host in host_line.split("=", 1)[1].split(",") if host.strip()]
if len(hosts) != 302 or len(hosts) != len(set(hosts)):
    raise SystemExit(f"FAIL: MITM hosts count/uniqueness mismatch: {len(hosts)}")
if any("github.com" in host.lower() or "githubusercontent.com" in host.lower() for host in hosts):
    raise SystemExit("FAIL: GitHub host remains in MITM")

urls = set(re.findall(r"script-path=(https?://[^,\s]+)", source))
urls.update(re.findall(r"""(?:script|jq_file)\(\s*["'](https?://[^"']+)["']""", source))
if len(urls) != 40:
    raise SystemExit(f"FAIL: expected 40 unique runtime assets, found {len(urls)}")

pins = set()
pattern = re.compile(r"^https://raw\.githubusercontent\.com/XcvcvX/loon-independent-plugins/([0-9a-f]{40})/.+")
for url in urls:
    match = pattern.match(url)
    if not match:
        raise SystemExit(f"FAIL: non-vendored or unpinned runtime URL: {url}")
    pins.add(match.group(1))
if len(pins) != 1:
    raise SystemExit(f"FAIL: mixed asset commit pins: {sorted(pins)}")

inventory_path = Path("sources/script-assets.txt")
inventory = {
    line.strip()
    for line in inventory_path.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.lstrip().startswith("#")
}
if urls != inventory:
    raise SystemExit(f"FAIL: asset inventory mismatch; missing={sorted(urls-inventory)}, stale={sorted(inventory-urls)}")

failed = []
for url in sorted(urls):
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
print("PASS:", len(urls), "unique runtime assets anonymously fetched; pin:", next(iter(pins)))


# Validate the installed-app companion separately. It is intentionally static-only
# so app ad filtering does not add response-body parsing or runtime JS execution.
ADDON = Path("plugins/installed-app-adblock-addon.plugin")
addon_source = ADDON.read_text(encoding="utf-8")
addon_lines = addon_source.splitlines()
addon_sections = {}
for name in ["Rule", "Rewrite", "MITM"]:
    marker = f"[{name}]"
    if addon_lines.count(marker) != 1:
        raise SystemExit(f"FAIL: companion expected exactly one {marker}")
    start = addon_lines.index(marker) + 1
    end = next((i for i in range(start, len(addon_lines)) if addon_lines[i].startswith("[") and addon_lines[i].endswith("]")), len(addon_lines))
    addon_sections[name] = [line for line in addon_lines[start:end] if line.strip() and not line.lstrip().startswith("#")]

if any(line.strip() == "[Script]" for line in addon_lines):
    raise SystemExit("FAIL: companion must not contain a [Script] section")
if any(token in addon_source for token in ["script-path=", "http-response ", "response if ", "script("]):
    raise SystemExit("FAIL: companion must remain free of scripts and response-body parsing")
if len(addon_sections["Rule"]) != 5:
    raise SystemExit(f"FAIL: companion Rule count {len(addon_sections['Rule'])}, expected 5")
if len(addon_sections["Rewrite"]) != 20:
    raise SystemExit(f"FAIL: companion Rewrite count {len(addon_sections['Rewrite'])}, expected 20")
if any(not line.startswith("request if ") or "then reject_dict(200)" not in line for line in addon_sections["Rewrite"]):
    raise SystemExit("FAIL: companion Rewrite entries must be exact request URL rejects")
addon_host_line = next((line for line in addon_sections["MITM"] if line.strip().lower().startswith("hostname") and "=" in line), None)
if not addon_host_line:
    raise SystemExit("FAIL: companion MITM hostname declaration missing")
addon_hosts = [host.strip() for host in addon_host_line.split("=", 1)[1].split(",") if host.strip()]
if len(addon_hosts) != 14 or len(addon_hosts) != len(set(addon_hosts)):
    raise SystemExit(f"FAIL: companion MITM count/uniqueness mismatch: {len(addon_hosts)}")
print("PASS: installed-app companion has 5 domain rules, 20 request-only rewrites, 14 unique MITM hosts, and no scripts.")
