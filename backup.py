# 2020 https://github.com/xwillmarktheplace (discord:xwillmarktheplace#4400)
import requests
import json
import datetime as dt
import time

GAMES = ['oot', 'ootextras']
DEBUG = True # print link for every api request

class Endpoint:

    def __init__(self, base_url, base_params=None, max_per_page=200):
        self.page_offset = 0
        self.fetched_all = False
        self.max_per_page = max_per_page
        self.base_url = base_url
        self.base_params = base_params if base_params else {}


    def reset_pagination(self):
        self.page_offset = 0
        self.fetched_all = False

    def fetch_all(self):
        self.reset_pagination()
        result = {'data' : []}

        while(not self.fetched_all):
            src_json = self.fetch_next()
            if 'pagination' not in src_json.keys():
                self.fetched_all = True
                return src_json
            result['data'] += src_json['data']
        return result

    def fetch_next(self):
        if self.fetched_all:
            return print(f'Already downloaded everything for endpoint {self.base_url} with parameters {self.base_params}.')
        src_json = self._get()
        if 'pagination' not in src_json.keys() or src_json['pagination']['size'] < src_json['pagination']['max']:
            self.fetched_all = True
        self.page_offset += self.max_per_page
        return src_json


    def _get(self):
        params = self.base_params.copy()
        params.update({
            'max' : self.max_per_page,
            'offset' : self.page_offset
        })
        return get_request(self.base_url, params)



def get_request(url, params=None, attempts=5):

    params = params if params else {}

    for i in range(attempts):
        response = requests.get(url, params=params)
        if DEBUG:
            print(response.url)
        status = response.status_code

        if status == 200:
            return response.json()
        if status == 404:
            return

        print(f"Error while accessing {url}: status {status}, after {i+1} attempts.")


start_time = time.time()
timestamp = dt.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

for game in GAMES:

    print(f"\nDownloading data for game '{game}'...")
    game_data = get_request(f'https://www.speedrun.com/api/v1/games/{game}')
    if not game_data:
        print(f"Could not find game '{game}', please use the abbreviation that is used on speedrun.com (i.e. sm64 for Super Mario 64)")
        continue
    game_id = game_data['data']['id']



    # all runs of the game (including subcategories, ILs, obsolete, rejected, etc)
    runs_endpoint = Endpoint(f'https://www.speedrun.com/api/v1/runs', {'game' : game_id, 'embed' : 'players', 'orderby' : 'submitted', 'direction' : 'desc'})
    runs_data = runs_endpoint.fetch_all()
    with open(f"{timestamp}_{game}_runs.txt", 'w') as outfile:
        json.dump(runs_data, outfile)
    print(f"Downloaded all {len(runs_data['data'])} runs for '{game}' ({timestamp}_{game}_runs.txt).")


    game_data = {}
    # general game info (moderators, platforms, regions, etc)
    game_endpoint = Endpoint(f"https://www.speedrun.com/api/v1/games/{game_id}", {'embed':'moderators,regions,platforms'})
    game_data['game'] = game_endpoint.fetch_all()

    # category rules/info
    category_endpoint = Endpoint(f'https://www.speedrun.com/api/v1/games/{game_id}/categories', {'embed' : 'variables'})
    game_data['categories'] = category_endpoint.fetch_all()

    # individual level rules/info (if applicable)
    levels_endpoint = Endpoint(f'https://www.speedrun.com/api/v1/games/{game_id}/levels', {'embed' : 'variables'})
    game_data['levels'] = levels_endpoint.fetch_all()

    with open(f"{timestamp}_{game}_game_data.txt", 'w') as outfile:
        json.dump(game_data, outfile)
    print(f"Downloaded game info for '{game}' ({timestamp}_{game}_game_data.txt).")


elapsed_time = time.time() - start_time
print(f"\nFinished in {round(elapsed_time, 1)} seconds.")