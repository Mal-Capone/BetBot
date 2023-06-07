# the-odds-api.com
# -----------IMPORTS----------#
import os
import requests
import configparser

from statistics import mean
from betbot.utils import Printer as pr
from betbot.bookmakers import load_data

config = configparser.ConfigParser()
config.read('config.ini')

"""
~~~~~~~API COSTS~~~~~~~~
Remember the-odds-api caps the amount of requests depending on level of paid for API keys so cost_per_request is important
the API cost is based on how many markets and how many sports are included within the parameters for example...

markets * regions = cost_per_request

1 market, 1 region | Cost: 1
3 markets, 1 region | Cost: 3
1 market, 3 regions | Cost: 3
3 markets, 3 regions | Cost: 9

"""

class Game:
    def __init__(self, game):
        if game:
            self.game = game
            self.id = self.game['id']
            self.sport = self.game['sport_key'].split("_")[0]
            self.league = self.game['sport_title']
            self.start_date = self.game['commence_time'].split('T')[0]
            self.start_time = self.game['commence_time'].split('T')[1].replace('Z','')
            self.team_a = self.game['bookmakers'][0]['markets'][0]['outcomes'][0]['name']
            self.team_a_average_price = 0
            self.team_b = self.game['bookmakers'][0]['markets'][0]['outcomes'][1]['name']
            self.team_b_average_price = 0
            self.potential_outcomes = len(self.game['bookmakers'][0]['markets'][0]['outcomes'])
            self.available_bookmakers = self.game['bookmakers']
            self.arbitage_available = False
            self.arbitage_bookeeper_left = None
            self.arbitage_bookeeper_right = None
    def find_arbitrage(self):
        h2h_1   = None
        h2h_2   = None
        h2h_lay = None
        o = {}
        """
        outcomes = {games : [
                        { game1_id : 00001,
                          team_1 : mal
                          team_2 : toby },
                        { game_id : 00002,
                          team_1 : cuffy,
                          team_2 : shiv } 
                            ]
                        }
        """

        if self.potential_outcomes == 2:
            out = self.available_bookmakers[0]['markets'][0]['outcomes']
            self.team_a = out[0]['Name']
            self.team_b = out[1]['Name']
            for bookmaker in self.available_bookmakers:
                markets = bookmaker['markets'][0]
                o['game'] = self.id
class Bookmaker:
    def __init__(self, key):
        self.key     = key if key else None
        self.name    = None
        self.website = None
        self.region  = None
    def lookup_bookmaker(self, key):
        data = load_data()
        self.name = data[key]['name']
        self.region= data[key]['region']
        self.website = data[key]['website']
def get_response(regions=None,quota=False):
    try:
        API_KEY     = os.environ.get('THE_ODDS_API_KEY')
        API_KEY     = '1bbd198f53c2a0b715e02113ae6c18ad' if not API_KEY else API_KEY
        REGIONS     = config['OddsApi']['REGIONS'] if not regions else regions
        MARKETS     = config['OddsApi']['MARKETS']
        ODDS_FORMAT = config['OddsApi']['ODDS_FORMAT']
        DATE_FORMAT = config['OddsApi']['DATE_FORMAT']
        SPORT       = config['OddsApi']['SPORT']
        params = {
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT}
        if quota:
            response = requests.get(f'https://api.the-odds-api.com/v4/sports',params)
            remaining = response.headers['X-Requests-Remaining']
            used = response.headers['X-Requests-Used']
            this_cost = len(REGIONS.split(",") * len(MARKETS.split(",")))
            return remaining, used, this_cost
        else:
            response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params).json()
        return response
    except Exception as ex:
        print(f'[!] Exception: {ex}')
        return None
def findMatches(regions, outcomes, verbose=False):
    i = 0
    game_odds  = {}
    odds_response = get_response(regions=regions)
    all_games = [Game(game) for game in odds_response if len(game['bookmakers'][0]['markets'][0]['outcomes']) <= outcomes]
    all_games_refined = []
    for game in all_games:
        i += 1
        lst_a, lst_b = [], []
        outcomes = []
        pr.ok(f'[{str(i).ljust(2,"0")}]  {str(game.sport).title()}: ({game.team_a}) vs ({game.team_b}) | Start Time: {game.start_date} {str(game.start_time).strip("Z")} | Checking {len(game.available_bookmakers)} bookmakers')
        for bookmaker in game.available_bookmakers:
            team_a_name  = bookmaker['markets'][0]['outcomes'][0]['name']
            team_b_name  = bookmaker['markets'][0]['outcomes'][1]['name']
            team_a_price = bookmaker['markets'][0]['outcomes'][0]['price']
            team_b_price = bookmaker['markets'][0]['outcomes'][1]['price']

            if team_a_price >= 2.0:
                lst_a.append((team_a_name,team_a_price, bookmaker['key']))

            if team_b_price >= 2.0:
                lst_b.append((team_b_name, team_b_price, bookmaker['key']))

            result = {
                'bookmaker_key': bookmaker['key'],
                'outcomes': {
                                'team_a_name':  bookmaker['markets'][0]['outcomes'][0]['name'],
                                'team_a_price': bookmaker['markets'][0]['outcomes'][0]['price'],
                                'team_b_name':  bookmaker['markets'][0]['outcomes'][1]['name'],
                                'team_b_price': bookmaker['markets'][0]['outcomes'][1]['price']
                            }}
            outcomes.append(result)

            if result:
                if verbose:
                    print(f'\t > {result["outcomes"]["team_a_name"]} : {str(result["outcomes"]["team_a_price"]).ljust(4,"0")} | {result["outcomes"]["team_b_name"]} : {str(result["outcomes"]["team_b_price"]).ljust(4,"0")} : {bookmaker["title"]} ')
            game_odds[game.id] = outcomes

        if len(lst_b) and len(lst_a):
            maxlst_a = max(lst_a)
            maxlst_b = max(lst_b)
            game.arbitage_available = True
            game.arbitage_left_bookeeper = maxlst_a[2]
            game.arbitage_left_price = maxlst_a[1]
            game.arbitage_right_bookeeper = maxlst_b[2]
            game.arbitage_right_price = maxlst_b[1]
            game.team_a_average_price = maxlst_a[1]
            game.team_b_average_price = maxlst_b[1]
            print(f"> {pr.sep()}{pr.info('Arbitage bet found!')}")
            print(f"> {str(game.sport).title()} {game.league} - {game.start_time} {game.start_date}")
            print(f"> {game.team_a} ({game.arbitage_left_bookeeper}:{game.arbitage_left_price}) vs {game.team_b} ({game.arbitage_right_bookeeper}:{game.arbitage_right_price}){pr.sep()})")

        all_games_refined.append(game)

    return game_odds, all_games_refined
def get_results(regions='all', outcomes=2):
    """
        Finds all the current available bets which match the criteria for a surebet
        :max_tries: user input field, maximum number of api calls warranted, if set to 0 then will loop infinite, default is 10
        :interval - time between API calls
    """
    verbose = config['System']['VERBOSE']
    left_bets, right_bets = [], []
    rgames = []
    game_odds, all_games = findMatches(regions, outcomes, verbose)
    for game_id, all_game_odds in game_odds.items():
        game = [x for x in all_games if x.id == game_id][0]
        for odds in all_game_odds:
            bookmaker_key = odds['bookmaker_key']
            outcomes      = odds['outcomes']
            team_a_price  = outcomes['team_a_price']
            team_b_price  = outcomes['team_b_price']
            if team_a_price >= 2:
                left_bets.append([team_a_price, outcomes['team_a_name'], bookmaker_key])
            if team_b_price >= 2:
                right_bets.append([team_b_price, outcomes['team_b_name'], bookmaker_key])
        if not game.arbitage_available:
            game.team_a_average_price = round(mean([p['outcomes']['team_a_price'] for p in all_game_odds]), 2)
            game.team_b_average_price = round(mean([p['outcomes']['team_b_price'] for p in all_game_odds]), 2)
        left_bets = []
        right_bets = []
    print(rgames) if len(rgames) else None
    response = {
        'game_odds' : game_odds,
        'all_games' : all_games,
        # 'rgames'    : rgames,
        'quota'     : get_response(regions=regions,quota=True)
    }
    return response

if __name__ == '__main__':
    pass
