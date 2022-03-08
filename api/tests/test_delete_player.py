import json

def test_delete_player_success(client, patterns_plays):
    with client.session_transaction() as session:
        session['plays'] = patterns_plays
    response = client.delete("/player/1")
    assert 200 == response.status_code
    assert "Jogador 1 removido" in json.loads(response.data).get('success')

def test_delete_player_error_without_session_plays(client):
    with client.session_transaction() as session:
        session['plays'] = []
    response = client.delete("/player/8")
    assert 400 == response.status_code
    assert "Jogador 8 inválido ou não cadastrado" in json.loads(response.data).get('error')

def test_delete_player_error_with_session_plays(client, patterns_plays):
    with client.session_transaction() as session:
        session['plays'] = patterns_plays
    response = client.delete("/player/8")
    assert 400 == response.status_code
    assert "Jogador 8 inválido ou não cadastrado" in json.loads(response.data).get('error')