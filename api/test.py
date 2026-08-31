import requests
import json

headers = {
    "Accept": "application/json",
    "X-API-Key":"tpb_live.DjpROXA2.dTimdaxAuBaCGsvEQ8ESA_QUTGMCRfev"
}

url = "https://servix.cc/api/v1/assets/GOLD_18_RLS"

response  = requests.get(
    url=url,
    headers = headers
)
data = response.json()
# with open("response.json",'w') as fp:
#     json.dump(response,fp, indent=4)

with open("gold.json", "w") as file:
    json.dump(data, file, indent=4)