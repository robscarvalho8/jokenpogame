import json

def test_delete_entrance_success(client, patterns_plays):
    with client.session_transaction() as session:
        session['plays'] = patterns_plays
    response = client.delete("/entrance/1")
    assert 200 == response.status_code
    assert "Entrada 1 removido" in json.loads(response.data).get('success')

def test_delete_entrance_error_without_session_plays(client):
    with client.session_transaction() as session:
        session['plays'] = []
    response = client.delete("/entrance/8")
    assert 400 == response.status_code
    assert "Entrada 8 inválido ou não cadastrado" in json.loads(response.data).get('error')

def test_delete_entrance_error_with_session_plays(client, patterns_plays):
    with client.session_transaction() as session:
        session['plays'] = patterns_plays
    response = client.delete("/entrance/8")
    assert 400 == response.status_code
    assert "Entrada 8 inválido ou não cadastrado" in json.loads(response.data).get('error')
