"""GET endpoints for blaseball /database/ path.

Based off spec: https://github.com/Society-for-Internet-Blaseball-Research/blaseball-api-spec
"""
import requests


BASE_URL = 'https://www.blaseball.com/database'


def get_global_events():
    res = requests.get(f'{BASE_URL}/globalEvents')
    return res.json()


def get_all_teams():
    """
    Returns dictionary keyed by team ID
    """
    res = requests.get(f'{BASE_URL}/allTeams')
    return {t['id']: t for t in res.json()}


def get_all_divisions():
    """
    Returns dictionary keyed by division ID
    """
    res = requests.get(f'{BASE_URL}/allDivisions')
    return {d['id']: d for d in res.json()}


def get_league(id_='d8545021-e9fc-48a3-af74-48685950a183'):
    res = requests.get(f'{BASE_URL}/league?id={id_}')
    return res.json()


def get_subleague(id_):
    res = requests.get(f'{BASE_URL}/subleague?id={id_}')
    return res.json()


def get_division(id_):
    res = requests.get(f'{BASE_URL}/division?id={id_}')
    return res.json()


def get_team(id_):
    res = requests.get(f'{BASE_URL}/team?id={id_}')
    return res.json()


def get_player(id_):
    """
    Accepts single string id_, comma separated string, or list.
    Returns a dictionary with ID as key
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    res = requests.get(f'{BASE_URL}/players?ids={id_}')
    return {p['id']: p for p in res.json()}


def get_games(season, day):
    """
    Season and day will be 1 indexed.
    Returns as dictionary with game ID as key.
    """
    res = requests.get(f'{BASE_URL}/games?season={season - 1}&day={day - 1}')
    return {g['id']: g for g in res.json()}


def get_game_by_id(id_):
    res = requests.get(f'{BASE_URL}/gameById/{id_}')
    return res.json()


def get_offseason_election_details(self):
    res = requests.get(f'{BASE_URL}/offseasonSetup')
    return res.json()


def get_offseason_recap(season):
    """
    Season will be 1 indexed.
    """
    res = requests.get(f'{BASE_URL}/offseasonRecap?season={season - 1}')
    return res.json()


def get_offseason_bonus_results(id_):
    """
    id_ can be a single string ID, comma separated string, or list.
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    res = requests.get(f'{BASE_URL}/bonusResults?ids={id_}')
    return res.json()


def get_offseason_decree_results(id_):
    """
    id_ can be a single string ID, comma separated string, or list.
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    res = requests.get(f'{BASE_URL}/decreeResults?ids={id_}')
    return res


def get_playoff_details(season):
    """
    Season will be 1 indexed.
    """
    res = requests.get(f'{BASE_URL}/playoffs?number={season - 1}')
    return res.json()


def get_playoff_round(id_):
    res = requests.get(f'{BASE_URL}/playoffRound?id={id_}')
    return res.json()