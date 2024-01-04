import requests

def pasetebin_apiKey(api_key):
    global api_keyint
    api_keyint = api_key

def get_paste_content_withApiKey(api_key1, paste_id1):
    api_url = f'https://pastebin.com/raw/{paste_id1}'
    params = {
        'api_dev_key': api_key1,
    }

    response = requests.get(api_url, params=params)
    
    if response.text.startswith('Bad API request'):
        print(f"Error: {response.text}")
        return None
    else:
        return response.text

def get_paste_content(paste_id2):
    return(get_paste_content_withApiKey(api_keyint,paste_id2))

class bintet():
    def t1(t):
        print(t)
