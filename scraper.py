import re
import requests
import time
import base64
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urlparse, urlunparse

# ========== CONFIGURATION ==========
TEHRAN_TZ = ZoneInfo("Asia/Tehran")

# کانال‌های تلگرامی (بدون @)
CHANNELS = [
    "Configir98",
    "napsternetv",
    "ProxyHub98",
    "ghalagyann",
    "icv2ray",
    "WedBaZvpn",
    "anty_filter",
    "VPNBaz",
    # می‌توانی بعداً اضافه کنی
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Regex های مختلف
URI_REGEX = re.compile(
    r'(?:vmess|vless|trojan|ss|tuic|hysteria2|hysteria|socks)://[^\s\'"<>\[\]{}|\\^`]+',
    re.IGNORECASE
)
JSON_CUSTOM_REGEX = re.compile(
    r'\{[^{}]*"remarks"\s*:\s*"[^"]*"[^{}]*"outbounds"\s*:\s*\[.*?\]\s*[^{}]*\}',
    re.DOTALL
)
IP_PORT_REGEX = re.compile(
    r'(?:host|server|ip|address)?\s*[:=]?\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*[\s,;|]+\s*(?:port|:)?\s*(\d{1,5})',
    re.IGNORECASE
)

REMARK = "☬SHΞN™"
OUTPUT_FILE = "☬SHΞN™.txt"

# ========== FUNCTIONS ==========
def fetch_channel_page(username: str) -> str:
    url = f"https://t.me/s/{username}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[!] Error fetching {username}: {e}")
        return ""

def change_remark(config: str) -> str:
    """تغییر remark به REMARK برای انواع مختلف کانفیگ"""

    # 1) JSON custom
    if config.strip().startswith("{"):
        try:
            obj = json.loads(config)
            if "remarks" in obj:
                obj["remarks"] = REMARK
            return json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
        except Exception:
            pass

    # 2) IP:Port خام – بدون تغییر
    if re.fullmatch(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', config.strip()):
        return config

    # 3) URI based
    if "://" in config:
        try:
            parsed = urlparse(config)
            scheme = parsed.scheme

            # --- vmess جداگانه (base64 json) ---
            if scheme == "vmess":
                try:
                    b64_str = parsed.netloc + (parsed.path if parsed.path else "")
                    padding = 4 - len(b64_str) % 4
                    if padding != 4:
                        b64_str += "=" * padding
                    decoded = base64.b64decode(b64_str).decode("utf-8")
                    obj = json.loads(decoded)
                    obj["ps"] = REMARK
                    new_json = json.dumps(obj, separators=(',', ':'), ensure_ascii=False)
                    new_b64 = base64.b64encode(new_json.encode("utf-8")).decode("utf-8")
                    return f"vmess://{new_b64}"
                except Exception:
                    pass

            # --- بقیه scheme ها (vless, trojan, ss, socks, tuic, ...) ---
            if scheme in ("vless", "trojan", "ss", "socks", "tuic", "hysteria2", "hysteria"):
                new_parsed = parsed._replace(fragment=REMARK)
                return urlunparse(new_parsed)

            # scheme های ناشناخته – fragment
            if parsed.fragment:
                new_parsed = parsed._replace(fragment=REMARK)
                return urlunparse(new_parsed)
            else:
                return config

        except Exception:
            pass

    return config

def generate_output(socks_links, v2ray_links, custom_links, ipport_links) -> str:
    now_tehran = datetime.now(TEHRAN_TZ)
    now_str = now_tehran.strftime("%Y-%m-%d %H:%M:%S")
    total = len(socks_links) + len(v2ray_links) + len(custom_links) + len(ipport_links)
    next_refresh = (now_tehran + timedelta(minutes=10)).strftime("%I:%M %p").lstrip("0")

    lines = []
    lines.append("☬Exclusive SHΞN™ made")
    lines.append("Live Config Collector")
    lines.append(f"Last update: {now_str}      Total configs: {total}   Next refresh: {next_refresh}")
    lines.append("")

    # بخش SOCKS
    if socks_links:
        lines.append("========== SOCKS ==========")
        for link in socks_links:
            lines.append(link)
        lines.append("")

    # بخش V2RAY NORMAL
    if v2ray_links:
        lines.append("========== V2RAY NORMAL (vless, vmess, ss, trojan) ==========")
        for link in v2ray_links:
            lines.append(link)
        lines.append("")

    # بخش CUSTOM
    if custom_links:
        lines.append("========== CUSTOM CONFIGS ==========")
        for link in custom_links:
            lines.append(link)
        lines.append("")

    # بخش IP:PORT
    if ipport_links:
        lines.append("========== IP:PORT PAIRS ==========")
        for link in ipport_links:
            lines.append(link)
        lines.append("")

    # فوتر
    lines.append("Overhauld ☬ SHΞЯVIN™")
    lines.append("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠉⠉⠉⠉⠉⠉⠉⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⢀⣤⣾⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠉⠀⠀⠚⠛⠛⠛⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣀⣀⣀⣀⣀⣀⣀⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠀⠉⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⠤⠀⠉⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠉⠉⢀⣀⣤⣶⣾⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠒⠛⠛⠛⠛⠛⠛⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠀⣶⣶⠀⢰⣶⣶⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⡀⠙⠋⢀⡀⠈⠛⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠿⣶⡶⠿⣿⣿⠶⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠀⣿⡇⠀⣿⣿⠀⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠀⣿⣇⣀⣿⣿⠀⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣶⣶⣶⠀⣶⣶⣶⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠿⠿⠿⠀⠿⠿⠿⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣤⣤⣤⣤⣤⣤⣤⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⠋⢀⣿⠋⢀⡀⠙⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣇⠀⢿⡏⢀⣾⡿⠀⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣤⣀⣀⣼⣇⣀⣰⣿⣿⣿⣿⣿")
    lines.append("⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
    lines.append("☬Exclusive SHΞN™ made")
    lines.append("More !? T.me/Shervini")

    return "\n".join(lines)

def main():
    print(f"[{datetime.now(TEHRAN_TZ).isoformat()}] Starting collector...")

    socks_set = set()
    v2ray_set = set()
    custom_set = set()
    ipport_set = set()

    socks_list = []
    v2ray_list = []
    custom_list = []
    ipport_list = []

    for ch in CHANNELS:
        print(f"  -> Fetching {ch}")
        html = fetch_channel_page(ch)
        if not html:
            continue

        # 1) URI-based
        raw_uris = URI_REGEX.findall(html)
        for raw in raw_uris:
            cfg = change_remark(raw)
            try:
                scheme = urlparse(cfg).scheme
            except Exception:
                scheme = ""
            if scheme == "socks":
                if cfg not in socks_set:
                    socks_set.add(cfg)
                    socks_list.append(cfg)
            elif scheme in ("vmess", "vless", "trojan", "ss", "tuic", "hysteria2", "hysteria"):
                if cfg not in v2ray_set:
                    v2ray_set.add(cfg)
                    v2ray_list.append(cfg)
            else:
                if cfg not in v2ray_set:
                    v2ray_set.add(cfg)
                    v2ray_list.append(cfg)

        # 2) JSON custom
        raw_jsons = JSON_CUSTOM_REGEX.findall(html)
        for raw in raw_jsons:
            cfg = change_remark(raw)
            if cfg not in custom_set:
                custom_set.add(cfg)
                custom_list.append(cfg)

        # 3) IP:Port pairs
        for match in IP_PORT_REGEX.finditer(html):
            ip = match.group(1)
            port = match.group(2)
            pair = f"{ip}:{port}"
            if pair not in ipport_set:
                ipport_set.add(pair)
                ipport_list.append(pair)

        time.sleep(1)

    output_content = generate_output(socks_list, v2ray_list, custom_list, ipport_list)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output_content)

    total = len(socks_list) + len(v2ray_list) + len(custom_list) + len(ipport_list)
    print(f"✅ Total configs: {total} (SOCKS:{len(socks_list)} V2Ray:{len(v2ray_list)} Custom:{len(custom_list)} IP:Port:{len(ipport_list)})")
    print(f"✅ Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
