
import requests

api_key = 0x5B624547C66523E8850C121185F1E90B
user = 76561199221076311  # me
game = 1454400

interface = 'ISteamUser'
method = 'CheckAppOwnership'
method_version = 'v4'

# request format https://api.steampowered.com/<interface>/<method>/<method_version>/
url = 'https://api.steampowered.com/' + interface + '/' + method + '/' + method_version + '/'

headers = {
    'Host': 'silverabyss6808.com'
}

request_parameters = {
    'key': api_key,
    'steamid': user,
    'appid': game
}

response = requests.get(url, request_parameters)
print(response.text)
