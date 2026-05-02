import requests
import json

api_key = "VOTRE_CLE_API_OPENAQ"  # ⚠️ Insérez ici votre vraie clé
url = "https://api.openaq.org/v3/countries/CM?limit=1"

headers = {"X-API-Key": api_key}
r = requests.get(url, headers=headers)

if r.status_code == 200:
    print("🔑 Authentification réussie !")
    data = r.json()
    # Avec cette URL, pas de clé 'results', le résultat est direct
    print(data)
else:
    print(f"Erreur HTTP {r.status_code}: {r.text}")