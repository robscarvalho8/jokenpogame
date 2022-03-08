import json

def test_play_post_success(client, patterns_plays):
    with client.session_transaction() as session:
        session['plays'] = []
    response = client.post("/play", json=patterns_plays)
    assert 200 == response.status_code
    assert "Jogador - 5" == json.loads(response.data).get('winner')

def test_play_invalid(client, invalid_play):
    response = client.post("/play", json=invalid_play)
    assert 400 == response.status_code
    assert {"play": f"Jogadas: ['canivete'] inválidas"} == json.loads(response.data).get('error')

def test_play_player_duplicated_error(client, player_duplicated):
    response = client.post("/play", json=player_duplicated)
    assert 400 == response.status_code
    assert {'player': 'Cada jogador deve ser único.'} == json.loads(response.data).get('error')


def test_play_entrance_duplicated_error(client, entrance_duplicated):
    response = client.post("/play", json=entrance_duplicated)
    assert 400 == response.status_code
    assert {'entrace': 'Cada entrada deve ser única.'} == json.loads(response.data).get('error')

def test_play_player_registered_error(client, patterns_plays):
    with client.session_transaction() as session:
       session['plays'] = patterns_plays

    body = [
        {
            "player": 1,
            "play": "pedra",
            "entrance": 12,
        },
    ]
    response = client.post("/play", json=body)
    assert 400 == response.status_code
    assert {'player': 'Jogador [1] já cadastrado'} == json.loads(response.data).get('error')

def test_play_entrance_registered_error(client, patterns_plays):
    with client.session_transaction() as session:
        session['plays'] = patterns_plays
    body = [
        {
            "player": 8,
            "play": "pedra",
            "entrance": 1,
        },
    ]
    response = client.post("/play", json=body)
    assert 400 == response.status_code
    assert {'entrance': 'Entradas [1] já cadastrada'} == json.loads(response.data).get('error')

