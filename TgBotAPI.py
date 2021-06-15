import requests
import re



def sendMessage(chat_id, text, bot_secret):
    # print(text)
    data = {'text': f"{text}", 'chat_id': f"{chat_id}"}
    requests.post(
        f"https://api.telegram.org/bot{bot_secret}/sendMessage", data=data)


def getMessage(chat_id, bot_secret):
    url = f"https://api.telegram.org/bot{bot_secret}/getUpdates"
    response = requests.get(url)
    json = response.json()
    # print(json)
    if json['ok'] == False:
        print("Error in getMessage ", json['description'])
        return
    text = "No Messages"
    for i in json['result']:
        if "message" in i.keys():
            idx = "message"
        else:
            continue
        if i[idx]['chat']['id'] == chat_id:
            text = i[idx]['text']
            url = f"https://api.telegram.org/bot{bot_secret}/getUpdates?offset={int(i['update_id'])+1}"
            response = requests.get(url)
            print(text)
            break

    return text
