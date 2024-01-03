import requests

def get_achievements(token):
    url = 'http://game-store.7m.pl/api.php?action=get_achievements&token=' + token
    response = requests.get(url)
    return response.json()

def unlock_achievement(token, game_id, achievement_name):
    url = f'http://game-store.7m.pl/api.php?action=unlock_achievement&token={token}&game_id={game_id}&achievement_name={achievement_name}'
    response = requests.get(url)
    return response.json()
