"""
From the_odds_api.py
"""

#Complete Finish the arbitage function
# # def arbitage_bets(games, verbose):
# """
# :argument games -> of Game() objects to check and see if there are any suitable arbitage oppertunities
# :return   checked_games -> list of Game() objects which where given as the argument but have been updated with
#           odds and where appropriate arbitage options
# """
# checked_games,left_outcomes, right_outcomes = [],[],[]
# all_outcomes, game_odds = [], {}
# for game in games:
#     for bookmaker in game.available_bookmakers:
#         team_a_name  = bookmaker['markets'][0]['outcomes'][0]['name']
#         team_a_price = bookmaker['markets'][0]['outcomes'][0]['price']
#         team_b_name  = bookmaker['markets'][0]['outcomes'][1]['name']
#         team_b_price = bookmaker['markets'][0]['outcomes'][1]['price']
#         if team_a_price >= config['Betting']['MIN_PRICE']:
#             left_outcomes.append((team_a_name,team_a_price, bookmaker['key']))
#         if team_b_price >= config['Betting']['MIN_PRICE']:
#             right_outcomes.append((team_b_name, team_b_price, bookmaker['key']))
#         res = {
#             'bookmaker_key': bookmaker['key'],
#             'outcomes': {
#                             'team_a_name':  bookmaker['markets'][0]['outcomes'][0]['name'],
#                             'team_a_price': bookmaker['markets'][0]['outcomes'][0]['price'],
#                             'team_b_name':  bookmaker['markets'][0]['outcomes'][1]['name'],
#                             'team_b_price': bookmaker['markets'][0]['outcomes'][1]['price']
#                         }}
#         all_outcomes.append(res)
#         if res:
#             if verbose:
#                 print(f'\t > {res["outcomes"]["team_a_name"]} : {str(res["outcomes"]["team_a_price"]).ljust(4,"0")} | {res["outcomes"]["team_b_name"]} : {str(res["outcomes"]["team_b_price"]).ljust(4,"0")} : {bookmaker["title"]} ')
#         game_odds[game.id] = all_outcomes


# i = 0
# all_matches = []
# all_match_ids = []
# all_fail_ids = []
# all_fails = []
#
# while i < count:
#     pass
#     # for game in ok:
#     #     if not game.id in all_match_ids:
#     #         all_match_ids.append(game.id)
#     #         all_matches.append(game)
#     # for gg in fails:
#     #     if not gg.id in all_fail_ids:
#     #         all_fail_ids.append(gg.id)
#     #         all_fails.append(gg)
#     # i += 1
#     # print(f'Checking Count: {count}')
#     # if len(ok):
#     #     print(ok)
#     #     return all_matches, all_fails
# # return all_matches, all_fails
