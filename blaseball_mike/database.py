"""
Wrappers for the Official Blaseball API

https://docs.sibr.dev/docs/apis/reference/Blaseball-API.v1.yaml
"""
from blaseball_mike.session import session, check_network_response, TIMESTAMP_FORMAT
from datetime import datetime

BASE_URL = 'https://api.blaseball.com'
BASE_GITHUB = 'https://raw.githubusercontent.com/xSke/blaseball-site-files/main/data'
CONFIG_S3_URL = 'https://blaseball-configs.s3.us-west-2.amazonaws.com'


def get_global_events(*, cache_time=5):
    """
    Get Current Global Events (Ticker Text).

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/globalEvents')
    return check_network_response(res)


def get_all_teams(*, cache_time=5):
    """
    Get All Teams, including Tournament teams and Hall Stars. Returns dictionary keyed by team ID.

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/allTeams')
    return {t['id']: t for t in check_network_response(res)}


def get_all_divisions(*, cache_time=5):
    """
    Get list of all divisions, including removed divisions. Returns dictionary keyed by division ID.

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/allDivisions')
    return {d['id']: d for d in check_network_response(res)}


def get_league(id_='d8545021-e9fc-48a3-af74-48685950a183', cache_time=5):
    """
    Get league by ID.

    Args:
        id_: league ID, defaults to current league (Internet League Blaseball)
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/league?id={id_}')
    return check_network_response(res)


def get_subleague(id_, cache_time=5):
    """
    Get subleague by ID (eg: Mild, Evil, etc).

    Args:
        id_: subleague ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/subleague?id={id_}')
    return check_network_response(res)


def get_division(id_, cache_time=5):
    """
    Get division by ID.

    Args:
        id_: division ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/division?id={id_}')
    return check_network_response(res)


def get_team(id_, cache_time=5):
    """
    Get team by ID.

    Args:
        id_: team ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/team?id={id_}')
    return check_network_response(res)


def get_player(id_, cache_time=5):
    """
    Get players by ID. Returns a dictionary with player ID as key

    Args:
        id_: player ID(s). Can be single string id_, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if len(id_) == 0:
        return {}
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/players?ids={id_}')
    return {p['id']: p for p in check_network_response(res)}


def get_games(season, day, cache_time=5):
    """
    Get games by season and day. Returns as dictionary with game ID as key.

    Args:
        season: Season, 1 indexed
        day: Day, 1 indexed
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/games?season={season - 1}&day={day - 1}')
    return {g['id']: g for g in check_network_response(res)}


def get_tournament(tournament, day, cache_time=5):
    """
    Get games by tournament and day. Returns as dictionary with game ID as key.

    Args:
        tournament: Tournament ID
        day: Day, 1 indexed
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/games?tournament={tournament}&day={day - 1}')
    return {g['id']: g for g in check_network_response(res)}


def get_game_by_id(id_, cache_time=5):
    """
    Get game by ID.

    Args:
        id_: game ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/gameById/{id_}')
    return check_network_response(res)


def get_offseason_election_details(*, cache_time=5):
    """
    Get current Election ballot.

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/offseasonSetup')
    return check_network_response(res)


def get_offseason_recap(season, cache_time=5):
    """
    Get Election results by season.

    Args:
        season: Season, 1 indexed
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/offseasonRecap?season={season - 1}')
    return check_network_response(res)


def get_offseason_bonus_results(id_, cache_time=5):
    """
    Get blessing results by ID.

    Args:
        id: blessing ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/bonusResults?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_offseason_decree_results(id_, cache_time=5):
    """
    Get decree results by ID.

    Args:
        id: blessing ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/decreeResults?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_offseason_event_results(id_, cache_time=5):
    """
    Get tiding results by ID.

    Args:
        id: blessing ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/eventResults?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_playoff_details(season, cache_time=5):
    """
    Get playoff information by season.

    Args:
        season: season, 1 indexed.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/playoffs?number={season - 1}')
    return check_network_response(res)


def get_playoff_round(id_, cache_time=5):
    """
    Get playoff round by ID

    Args:
        id_: playoff round ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/playoffRound?id={id_}')
    return check_network_response(res)


def get_playoff_matchups(id_, cache_time=5):
    """
    Get playoff matchups (one team vs one team) by ID

    Args:
        id: playoff matchup ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(id_, list):
        id_ = ','.join(id_)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/playoffMatchups?ids={id_}')
    return {g['id']: g for g in check_network_response(res)}


def get_standings(id_, cache_time=5):
    """
    Get league standings by ID

    Args:
        id_: standings ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/standings?id={id_}')
    return check_network_response(res)


def get_season(season_number, cache_time=5):
    """
    Get season info by season number

    Args:
        season_number: season, 1 indexed
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/season?number={season_number - 1}')
    return check_network_response(res)


def get_tiebreakers(id, cache_time=5):
    """
    Get tiebreakers (Divine Favor) by ID

    Args:
        id_: tiebreaker ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/tiebreakers?id={id}')
    return {g['id']: g for g in check_network_response(res)}


def get_game_statsheets(ids, cache_time=5):
    """
    Get statsheets for a game by statsheet ID

    Args:
        id: game statsheet ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/gameStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_player_statsheets(ids, cache_time=5):
    """
    Get statsheets for a player by statsheet ID

    Args:
        id: player statsheet ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/playerStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_season_statsheets(ids, cache_time=5):
    """
    Get statsheets for a season by statsheet ID

    Args:
        id: season statsheet ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/seasonStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_team_statsheets(ids, cache_time=5):
    """
    Get statsheets for a team by statsheet ID

    Args:
        id: team statsheet ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/teamStatsheets?ids={ids}')
    return {s['id']: s for s in check_network_response(res)}


def get_tributes(*, cache_time=5):
    """
    Get current Hall of Flame

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/api/getTribute')
    return check_network_response(res)


def get_simulation_data(*, cache_time=5):
    """
    Get current simulation state

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/simulationData')
    return check_network_response(res)


def get_attributes(ids, cache_time=5):
    """
    Get modification by ID

    Args:
        ids: modification ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/mods?ids={ids}')
    return check_network_response(res)


def get_items(ids, cache_time=5):
    """
    Get item by ID

    Args:
        ids: item ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/items?ids={ids}')
    return check_network_response(res)


def get_weather(*, cache_time=5):
    """
    Get weather by ID

    Args:
        ids: weather ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_GITHUB}/weather.json')
    return check_network_response(res)


def get_blood(ids, cache_time=5):
    """
    Get blood type by ID

    Args:
        ids: blood ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/blood?ids={ids}')
    return check_network_response(res)


def get_coffee(ids, cache_time=5):
    """
    Get coffee preference by ID

    Args:
        ids: coffee ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/coffee?ids={ids}')
    return check_network_response(res)


def get_feed_global(limit=50, sort=None, category=None, start=None, type_=None, season=None, sim=None, season_start=None, season_end=None, cache_time=5):
    """
    Get Global Feed

    Args:
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
        type_: event type ID
        season: season, 1-indexed
        sim: sim ID
        season_start: return items after this season (inclusive)
        season_end: return items before this season (inclusive)
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start
    if type_ is not None:
        params["type"] = type_
    if season is not None:
        params["season"] = season - 1
    if sim is not None:
        params["sim"] = sim
    if season_start is not None:
        params["seasonStart"] = season_start - 1
    if season_end is not None:
        params["seasonEnd"] = season_end - 1

    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/feed/global', params=params)
    return check_network_response(res)


def get_feed_game(id_, limit=50, sort=None, category=None, start=None, type_=None, sim=None, season_start=None, season_end=None, cache_time=5):
    """
    Get Game Feed

    Args:
        id_: Game ID
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
        type_: event type ID
        sim: sim ID
        season_start: return items after this season (inclusive)
        season_end: return items before this season (inclusive)
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"id": id_, "limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start
    if type_ is not None:
        params["type"] = type_
    if sim is not None:
        params["sim"] = sim
    if season_start is not None:
        params["seasonStart"] = season_start - 1
    if season_end is not None:
        params["seasonEnd"] = season_end - 1

    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/feed/game', params=params)
    return check_network_response(res)


def get_feed_team(id_, limit=50, sort=None, category=None, start=None, type_=None, season=None, sim=None, season_start=None, season_end=None, cache_time=5):
    """
    Get Team Feed

    Args:
        id_: Team ID
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
        type_: event type ID
        season: 1-indexed
        sim: sim ID
        season_start: return items after this season (inclusive)
        season_end: return items before this season (inclusive)
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"id": id_, "limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start
    if type_ is not None:
        params["type"] = type_
    if season is not None:
        params["season"] = season - 1
    if sim is not None:
        params["sim"] = sim
    if season_start is not None:
        params["seasonStart"] = season_start - 1
    if season_end is not None:
        params["seasonEnd"] = season_end - 1

    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/feed/team', params=params)
    return check_network_response(res)


def get_feed_player(id_, limit=50, sort=None, category=None, start=None, type_=None, season=None, sim=None, season_start=None, season_end=None,  cache_time=5):
    """
    Get Player Feed

    Args:
        id_: Player ID
        limit: Number of entries to return
        sort: 0 - Newest to Oldest, 1 - Oldest to Newest
        category: 0 - Game, 1 - Changes, 2 - Abilities, 3 - Outcomes, 4 - Narrative
        start: timestamp
        type_: event type ID
        season: season, 1-indexed
        sim: sim ID
        season_start: return items after this season (inclusive)
        season_end: return items before this season (inclusive)
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(start, datetime):
        start = start.strftime(TIMESTAMP_FORMAT)

    params = {"id": id_, "limit": limit}
    if sort is not None:
        params["sort"] = sort
    if category is not None:
        params["category"] = category
    if start is not None:
        params["start"] = start
    if type_ is not None:
        params["type"] = type_
    if season is not None:
        params["season"] = season - 1
    if sim is not None:
        params["sim"] = sim
    if season_start is not None:
        params["seasonStart"] = season_start - 1
    if season_end is not None:
        params["seasonEnd"] = season_end - 1

    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/feed/player', params=params)
    return check_network_response(res)


def get_feed_phase(season, phase, cache_time=5):
    """
    Get Feed by Phase

    Args:
        season: season, 1 indexed
        phase: sim phase number
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/feedbyphase?season={season-1}&phase={phase}')
    return check_network_response(res)


def get_feed_story(id_, cache_time=5):
    """
    Get Feed story item by ID

    Args:
        id_: Event ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/feed/story?id={id_}')
    return check_network_response(res)


def get_renovations(ids, cache_time=5):
    """
    Get stadium renovation by ID

    Args:
        ids: renovation ID(s). Can be a single string ID, comma separated string, or list.
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    if isinstance(ids, list):
        ids = ','.join(ids)
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/renovations?ids={ids}')
    return check_network_response(res)


def get_renovation_progress(id_, cache_time=5):
    """
    Get stadium renovation progress by stadium ID

    Args:
        id_: stadium ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/renovationProgress?id={id_}')
    return check_network_response(res)


def get_season_day_count(season, cache_time=5):
    """
    Get number of days in a season, by season

    Args:
        season: season, 1 indexed
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/seasondaycount?season={season - 1}')
    return check_network_response(res)


def get_team_election_stats(team_id, cache_time=5):
    """
    Get will contribution percentage by team ID

    Args:
        team_id: team ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/teamElectionStats?id={team_id}')
    return check_network_response(res)


def get_players_by_item(item, cache_time=5):
    """
    Get player holding an item

    Args:
        item: item ID
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/playersByItemId?id={item}')
    return check_network_response(res)


def get_gift_progress(*, cache_time=5):
    """
    Get league-wide gift shop progress

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/giftProgress')
    return check_network_response(res)


def get_all_players(*, cache_time=5):
    """
    Get list of player names and IDs

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/database/playerNamesIds')
    return check_network_response(res)


def get_days_since_incineration(*, cache_time=5):
    """
    Get the timestamp of the most recent incineration

    Args:
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    s = session(cache_time)
    res = s.get(f'{BASE_URL}/api/daysSinceLastIncineration')
    return check_network_response(res)


def get_schedule(season=None, sim=None, day=None, start_day=None, end_day=None, cache_time=5):
    """
    Get the list of list of games for a particular season/sim
    By default will return the full schedule for the current season/sim

    Args:
        season: filter by season number, if omitted defaults to current season
        sim: filter by sim ID, if omitted defaults to current sim
        day: filter by single day. If set, returns a list of games rather than a list of lists
        start_day: return schedule after this day (inclusive)
        end_day: return schedule before this day (inclusive)
        cache_time: response cache lifetime in seconds, or `None` for infinite cache
    """
    params = {}
    if start_day is not None and end_day is None:
        raise ValueError("Must set both start_day and end_day")

    if season is not None:
        params["season"] = season - 1
    if sim is not None:
        params["sim"] = sim
    if day is not None:
        params["day"] = day - 1
    if start_day is not None:
        params["startDay"] = start_day - 1
    if end_day is not None:
        params["endDay"] = end_day - 1

    s = session(cache_time)
    res = s.get(f'{BASE_URL}/api/games/schedule', params=params)
    return check_network_response(res)


def get_season_sim_map(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/feed_season_list.json')
    return check_network_response(res)


def get_glossary(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/glossary_words.json')
    return check_network_response(res)


def get_book(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/the_book.json')
    return check_network_response(res)


def get_library(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/library.json')
    return check_network_response(res)


def get_sponsor(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/sponsor_data.json')
    return check_network_response(res)


def get_all_attributes(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/attributes.json')
    return check_network_response(res)


def get_stadium_prefabs(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/stadium_prefabs.json')
    return check_network_response(res)


def get_blaseball_beat(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/the_beat.json')
    return check_network_response(res)


def get_fanart(cache_time=5):
    s = session(cache_time)
    res = s.get(f'{CONFIG_S3_URL}/fanart.json')
    return check_network_response(res)
