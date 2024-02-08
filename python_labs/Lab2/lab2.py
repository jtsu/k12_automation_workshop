import requests


url = "https://sandbox-nxos-1.cisco.com:443/ins"

payload = "\"ins_api\": {\n    \"input\": \"show system redundancy status\",\n    \"version\": \"1.0\",\n    \"type\": \"cli_show\",\n    \"chunk\": \"0\",\n    \"sid\": \"1\",\n    \"output_format\": \"json\"\n}"
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Authorization': 'Basic YWRtaW46QWRtaW5fMTIzNCE=',
  'Cookie': 'nxapi_auth=dzqnf:aA3liNn/ROUuJtU9nH/Y8Iqxeec='
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

# print(response.text)


json_data = response.json()

this_sup_internal_state = json_data['ins_api']['outputs']['output']['body']['this_sup_internal_state'] 
other_sup_rdn_state = json_data['ins_api']['outputs']['output']['body']['other_sup_rdn_state'] 

if ("standby" not in this_sup_internal_state.lower()) or ("standby" not in other_sup_rdn_state.lower()):
    message = f"SupA: {this_sup_internal_state} \nSupB: {other_sup_rdn_state}"

    print(message)


