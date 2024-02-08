import requests
import json
import webex_chatbot
from os import getenv
from dotenv import load_dotenv
from pathlib import Path

# Load Tokens and Keys from .env file
file_path = Path('~/Documents/GitHub/k12_automation_workshop/python_labs/Lab3/.env')
absolute_file_path = file_path.expanduser().resolve()
load_dotenv(dotenv_path=absolute_file_path)
ROOM_ID = getenv("K12_AUTOMATION_ROOM_ID")
TOKEN = getenv("LUMI_WEBEX_TOKEN")


def get_sup_status():
  url = "https://sandbox-nxos-1.cisco.com:443/ins"

  payload = "\"ins_api\": {\n    \"input\": \"show system redundancy status\",\n    \"version\": \"1.0\",\n    \"type\": \"cli_show\",\n    \"chunk\": \"0\",\n    \"sid\": \"1\",\n    \"output_format\": \"json\"\n}"
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46QWRtaW5fMTIzNCE=',
    'Cookie': 'nxapi_auth=dzqnf:aA3liNn/ROUuJtU9nH/Y8Iqxeec='
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  json_data = response.json()

  this_sup_internal_state = json_data['ins_api']['outputs']['output']['body']['this_sup_internal_state'] 
  other_sup_rdn_state = json_data['ins_api']['outputs']['output']['body']['other_sup_rdn_state'] 

  if (this_sup_internal_state.lower() != "active with ha standby") or (other_sup_rdn_state.lower() != "ha standby"):
      message = f"SupA: {this_sup_internal_state} and SupB: {other_sup_rdn_state}"
      
      webex_chatbot.post_message(TOKEN, ROOM_ID, message)



def main():
    if TOKEN:
        get_sup_status()
    else:
        print(f"No WebEx token found in .env file: TOKEN={TOKEN}")


if __name__ == "__main__":
    main()  

