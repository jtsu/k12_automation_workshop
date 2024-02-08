import json
import requests
import jinja2 

# Simple Bot Function for passing messages to a room
def post_message(token, room_id, message):
    header = {"Authorization": "Bearer %s" % token,
                "Content-Type": "application/json"}

    templateLoader = jinja2.FileSystemLoader(searchpath='./templates/')
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "input-card.j2"
    template = templateEnv.get_template(TEMPLATE_FILE)
    rendered_template = template.render(message=f'\"{message}\"')

    json_data = json.loads(rendered_template)

    card_payload = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": json_data,
    }

    data = {"roomId": room_id,
            "text": message,
            "attachments": card_payload}



    response = requests.post("https://webexapis.com/v1/messages/", headers=header, json=data, verify=True)

    if response.status_code == 200:
        print(f"Message was successfully posted to your Webex Room")

    else:
        print("failed with statusCode: %d" % response.status_code)
        print("Check response codes at the following url:")
        print("https://developer.webex.com/docs/api/v1/user-call-settings/read-call-recording-settings-for-a-personAs")



