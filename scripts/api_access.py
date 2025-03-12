import time

import requests
import jsonify
import string
import array
from enum import Enum

# user = 76561199221076311  # me

class Game:
    def __init__(self, appid: int, name: string):
        self.appid = appid
        self.name = name
    def __str__(self):
        return f'name: {self.name}, appid: {self.appid}'
class APIRequestType(Enum):
    def __init__(self, interface, method, method_version):
        self.interface = interface
        self.method = method
        self.method_version = method_version

    WISHLIST_GET_ALL = 'IWishlistService', 'GetWishlist', 'v1'
    GAMES_GET_ALL = 'ISteamApps', 'GetAppList', 'v2'

def request_url(request_type: APIRequestType, params_no_key: dict = None):
    url = 'https://api.steampowered.com/' + request_type.interface + '/' + request_type.method + '/' + request_type.method_version + '/'

    # parameters to be passed with the url
    api_key = 0x5B624547C66523E8850C121185F1E90B  # my key

    request_parameters = {
        'key': api_key
    }

    if (params_no_key != None):
        for param in params_no_key:
            request_parameters[param] = params_no_key[param]

    # http request
    try:
        response = requests.get(url, request_parameters)
        return response
    except:
        print('HTTP Error: ' + response.status_code)
def get_id_list(request_type: APIRequestType, params: dict = None):
    try:
        try:
            response = request_url(request_type, params)
            items = response.json()['response']['items']

            ids = []
        except: print('get_id_list(): Problem with response.')

        try:
            for i in items:
                appid = i['appid']
                ids.append(appid)
            ids.sort()
            return ids
        except:
            print('get_id_list(): Problem with items, most likely none provided.')

    except: print('get_id_list(): Unknown error.')
def resolve_game_ids(id_list: array = []):
    games_raw = []
    if (id_list != []):
        id_list_length = 0

        print('Sorting game list...')
        all_games = request_url(APIRequestType.GAMES_GET_ALL).json()['applist']['apps']

        # sort the list of all the games
        all_games_sorted = sorted(all_games, key=lambda x: x['appid'])
        num_games = 0
        for i in all_games_sorted:
            num_games += 1
        print(str(num_games) + ' games sorted.')

        # verify that it's sorted
        print('Verifying sort...')
        previous_game_id = 0
        for game in all_games_sorted:
            current_game_id = game['appid']
            if (current_game_id < previous_game_id):
                print('List not sorted. Exiting...')
                exit(1)
            else:
                previous_game_id = current_game_id

        print('Sort verified.')

        print('Resolving IDs...')
        try:
            id_list_length = len(id_list)

            # resolve ids
            for index, id in enumerate(id_list):
                for game in all_games_sorted:
                    if (id == game['appid']):
                        games_raw.append(Game(game['appid'], game['name']))
                        continue

            # # remove duplicates (they came with the json) on return
            # games = []
            # [games.append(i) for i in games_raw if i.appid not in games]

            return games_raw


        except:
            print('resolve_game_ids(): Problem resolving IDs.')
            return 0
        print('Problem with ID resolving. Exited early.')

    else: print('No IDs provided.')

# print(get_id_list(APIRequestType.WISHLIST_GET_ALL, {'steamid':76561199221076311}))

game_id_list = get_id_list(APIRequestType.WISHLIST_GET_ALL, {'steamid':76561199221076311})
games = resolve_game_ids(game_id_list)

print(len(games))

for ind, i in enumerate(games):
    print(str(ind+1) + '. ' + str(i.appid) + " " + i.name)