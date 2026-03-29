import requests
import json

# Tranzaksiyaları gətirən API ünvanı
url = "http://web0x06.hbtn/api/customer/transactions"

# Sənin sessiya cookie-n
cookies = {
    "session": "vw5CZ4aypAxDEmWUSq7mZ2XOYWfUaSVvcCaOQlRhrdo.5eImUtd-10eJCycNoR4zyDVtIOQ"
}

print("Tranzaksiyalar yoxlanılır və 'HolbertonSchool' dataları axtarılır...\n")

try:
    # Bütün tranzaksiyaları çəkirik
    response = requests.get(url, cookies=cookies)
    
    if response.status_code == 200:
        data = response.json().get("message", [])
        
        # İçində "Holberton" sözü keçən bütün qeydləri tapırıq
        holberton_data = [
            t for t in data 
            if t.get("merchant_name") and "Holberton" in t.get("merchant_name", "")
        ]
        
        if holberton_data:
            print(f"HolbertonSchool üçün {len(holberton_data)} qeyd tapıldı. Bütün detallar:\n")
            print("-" * 60)
            # Datanı səliqəli JSON formatında ekrana çıxarırıq
            print(json.dumps(holberton_data, indent=4, ensure_ascii=False))
            print("-" * 60 + "\n")
        else:
            print("HolbertonSchool adına aid heç bir data tapılmadı.")
            
    else:
        print(f"Xəta: API-yə qoşulmaq olmadı. Status Code: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"Bağlantı xətası baş verdi: {e}")
