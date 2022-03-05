
import json

def get_keys(path):
    with open(path) as f:
        return json.load(f)

keys = get_keys("../../.secret/twitter_api_key.json")
API_Key = keys['API Key']

