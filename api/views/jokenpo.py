from flask import session
from flask_restx import Resource


from api.server.instance import server
from api.models import play, delete_play, success, error
from api.views import constants

app, api = server.app, server.api


@api.route('/play')
class PlayJokenpo(Resource):
    @api.expect(play, valitade=True)
    @api.response(200, 'Success', success)
    @api.response(400, 'Validation Error', error,)
    def post(self):
        request = api.payload
        players = []
        entrances = []
        for x in request:
            if x.get('player') in [d['player'] for d in session['plays']]:
                players.append(x.get('player'))
            if x.get('entrance') in [d['entrance'] for d in session['plays']]:
                entrances.append(x.get('entrance'))
        if players:
            return {"error": {"player": f"Jogador {players} já cadastrado"}}, 400
        if entrances:
            return {"error": {"entrance": f"Entradas {entrances} já cadastrada"}},400
        [session['plays'].append(x) for x in request]
        session['plays'] = sorted(session['plays'], key=lambda d: d['entrance'])
        player_winner = get_winner(session['plays'])
        if player_winner.get('winner'):
            return {"winner": f'Jogador - {player_winner.get("player")}'}, 200
        else:
            return {"winner": f'Ninguém ganhou'}, 200

    @api.expect(delete_play)
    def delete(self):
        request = api.payload
        players = []
        entrances = []
        for x in request:
            if x.get('player') in [d['player'] for d in session['plays']]:
                players.append(x.get('player'))
            if x.get('entrance') in [d['entrance'] for d in session['plays']]:
                entrances.append(x.get('entrance'))
        if players:
            session['plays'] = list(filter(lambda i: i['player'] not in players, session['plays']))
            return {"success": f"Jogadores {players} removidos"}
        elif entrances:
            session['plays'] = list(filter(lambda i: i['entrance'] not in entrances, session['plays']))
            return {"success": f"Entradas {entrances} removidos"}
        else:
            return {"error": f"Necessário informar jogador ou entrada"}, 404

@app.before_first_request
def before_request_func():
    session['plays'] = []

def get_winner(plays):
    p = plays.copy()
    count = len(p)
    while count:
        player1 = p[0].get('play')
        player2 = p[1].get('play')

        if count == 2 and player1 == player2:
            return {}

        if player2 in constants.JOKENPO_WIN.get(player1):
            p.pop(1)
            count -= 1
        else:
            p.pop(0)
            count -= 1
    return {"winner": p[0]}
