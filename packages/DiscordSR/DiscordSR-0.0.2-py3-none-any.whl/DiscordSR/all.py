import requests
from datetime import datetime, timezone

def guild_mynick(token: str, server_id: int, nick: str, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/guilds/{server_id}/members/@me"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    json = {
        "nick": nick
    }
    r = requests.patch(url, headers=header, json=json)
    try:
        return r.json()
    except:
        return r.status_code

def guild_IDnick(token: str, server_id: int, user_id: int, nick: str, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/guilds/{server_id}/members/{user_id}"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    json = {
        "nick": nick
    }
    r = requests.patch(url, headers=header, json=json)
    try:
        return r.json()
    except:
        return r.status_code

def status( token: str, msg: str, **kwargs) -> dict:
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    text = msg
    jsonData = {
        "status": "online",
        "custom_status": {
            "text": text

        }
    }
    r = requests.patch(f"https://discord.com/api/v8/users/@me/settings", headers = header, json=jsonData)
    try:
        return r.json()
    except:
        return r.status_code

def timeout(token: str, server_id: int, user_id: int, mode: int, **kwargs) -> dict:
    utc_now = datetime.now(timezone.utc)
    utc_now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    if mode <= 0 or mode >= 7:
        raise ValueError
    if mode == 1: #switch文？なにそれおいしいの？（ あ　ほ　く　さ
        disabledate = f"{utc_now.strftime('%Y-%m-%dT%H:')}{utc_now.minute+1}{utc_now.strftime(':%S.%fZ')}"
    elif mode == 2:
        disabledate = f"{utc_now.strftime('%Y-%m-%dT%H:')}{utc_now.minute+5}{utc_now.strftime(':%S.%fZ')}"
    elif mode == 3:
        disabledate = f"{utc_now.strftime('%Y-%m-%dT%H:')}{utc_now.minute+10}{utc_now.strftime(':%S.%fZ')}"
    elif mode == 4:
        disabledate = f"{utc_now.strftime('%Y-%m-%dT')}{utc_now.hour+1}{utc_now.strftime(':%M:%S.%fZ')}"
    elif mode == 5:
        disabledate = f"{utc_now.strftime('%Y-%m-')}{utc_now.day+1}{utc_now.strftime('T%H:%M:%S.%fZ')}"
    elif mode == 6:
        disabledate = f"{utc_now.strftime('%Y-%m-')}{utc_now.day+7}{utc_now.strftime('T%H:%M:%S.%fZ')}"
        
    url = f"https://discord.com/api/v9/guilds/{server_id}/members/{user_id}"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    jsonData = {
        "communication_disabled_until": disabledate
        #"communication_disabled_until":"2024-01-13T19:12:55.595Z"
    }
    r = requests.patch(url, headers = header, json=jsonData)
    try:
        return r.json()
    except:
        return r.status_code

def untimeout(token: str, server_id: int, user_id: int, **kwargs) -> dict:
    utc_now = datetime.now(timezone.utc)
    now = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    url = f"https://discord.com/api/v9/guilds/{server_id}/members/{user_id}"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    jsonData = {
        "communication_disabled_until": now
    }
    r = requests.patch(url, headers = header, json=jsonData)
    try:
        return r.json()
    except:
        return r.status_code

def kick(token: str, server_id: int, user_id: int, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/guilds/{server_id}/members/{user_id}"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    r = requests.delete(url, headers = header)
    try:
        return r.json()
    except:
        return r.status_code

def ban(token: str, server_id: int, user_id: int, deletemsg_time: int, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/guilds/{server_id}/bans/{user_id}"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    jsonData= {
        "delete_message_seconds": deletemsg_time
    }
    r = requests.put(url, headers = header, json=jsonData)
    try:
        return r.json()
    except:
        return r.status_code

def report(token: str, server_id: int, user_id: int, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/reporting/user"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    jsonData= {
        "version":"1.0",
        "variant":"1",
        "language":"en",
        "breadcrumbs":[16,9,7,14],
        "elements":{
            "user_profile_select":[
                "photos","descriptors","name"
            ]
        },
        "guild_id":server_id,
        "user_id":user_id,
        "name":"user"
    }
    r = requests.post(url, headers = header, json=jsonData)
    try:
        return r.json()
    except:
        return r.status_code

def token_check(token: str, **kwargs) -> dict:
    headers = {"Authorization": token}
    r = requests.get("https://discordapp.com/api/v9/users/@me/library", headers=headers)
    if r.status_code == 200:
        return "vaild"
    else:
        return "invaild"

def nitro_check(code: str, **kwargs) -> dict:
    r = requests.get("https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true")
    if r.status_code == 200:
        return "vaild"
    else:
        return "invaild"

def send(token: str, channel_id: int, msg: str, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    jsonData= {
        "content": msg
    }
    r = requests.post(url, headers = header, json=jsonData)
    try:
        return r.json()
    except:
        return r.status_code

def bump(token: str, server_id: int, channel_id: int, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/interactions"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    jsonData= {
        "type":2,
        "application_id":"302050872383242240",
        "guild_id":server_id,
        "channel_id":channel_id,
        "session_id":"2be1fde9927afc846dc7a671abfe294a",
        "data":{
            "version":"1051151064008769576",
            "id":"947088344167366698",
            "name":"bump",
            "type":1,
            "options":[],
            "application_command":{
                "id":"947088344167366698",
                "type":1,
                "application_id":"302050872383242240",
                "version":"1051151064008769576",
                "name":"bump",
                "description":"Pushes your server to the top of all your server's tags and the front page",
                "description_default":"Pushes your server to the top of all your server's tags and the front page",
                "integration_types":[0],
                "options":[],
                "description_localized":"このサーバーの表示順をアップするよ",
                "name_localized":"bump"
            },
            "attachments":[]
        },
        "nonce":"1193586197746679808",
        "analytics_location":"slash_ui"
    }
    r = requests.post(url, headers = header, json=jsonData)
    try:
        return r.json()
    except:
        return r.status_code

def normal_reaction(token: str, channel_id: int, msg_id: str, emoji, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg_id}/reactions/{emoji}/%40me?location=Message&type=0"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    r = requests.put(url, headers = header)
    try:
        return r.json()
    except:
        return r.status_code

def custom_reaction(token: str, channel_id: int, msg_id: str, emoji_name: str , emoji_id: str, **kwargs) -> dict:
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{msg_id}/reactions/{emoji_name}:{emoji_id}/%40me?location=Message&type=0"
    header = {
        "authorization": token,
        'user-agent': "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8"
    }
    r = requests.put(url, headers = header)
    try:
        return r.json()
    except:
        return r.status_code