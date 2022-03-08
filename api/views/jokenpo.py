from flask import session
from flask_restx import Resource

import pandas as pd

from api.server.instance import server
from api.models import play, success, error, delete_error, delete_success
from api.views.core import JokenpoResult

app, api = server.app, server.api


@api.route('/play', doc={
    "description": 'Maximum number of objects in the body: 50\n\nAccepted Plays:\n- "pedra"\n- "papel"\n- "tesoura"\n- "lagarto"\n- "spock"'})
class PlayJokenpo(Resource):
    @api.expect(play, valitade=True)
    @api.response(200, 'Success Play', success)
    @api.response(400, 'Validation Error Play', error, )
    def post(self):
        request = api.payload
        df_request = pd.DataFrame(request)
        df_request['play'] = df_request['play'].str.lower()
        filter = df_request.play.str.contains(r'pedra|papel|tesoura|lagarto|spock')

        if not df_request[~filter].empty:
            return {"error": {"play": f"Jogadas: {df_request[~filter]['play'].to_list()} inválidas"}}, 400

        players_duplicated = df_request['player'][df_request.duplicated(['player'], keep='first')]
        if players_duplicated.tolist():
            return {"error": {"player": f"Cada jogador deve ser único."}}, 400

        entrance_duplicated = df_request['entrance'][df_request.duplicated(['entrance'], keep='first')]
        if entrance_duplicated.tolist():
            return {"error": {"entrace": f"Cada entrada deve ser única."}}, 400

        df_session = pd.DataFrame(session['plays'])
        df_session_request = pd.concat([df_request, df_session])

        df_request.sort_values(by=['entrance'], ascending=False).iloc[0].to_dict()

        players = df_session_request['player'][df_session_request.duplicated(['player'], keep='first')].tolist()
        entrances = df_session_request['entrance'][df_session_request.duplicated(['entrance'], keep='first')].tolist()
        if players:
            return {"error": {"player": f"Jogador {list(dict.fromkeys(players))} já cadastrado"}}, 400
        if entrances:
            return {"error": {"entrance": f"Entradas {list(dict.fromkeys(entrances))} já cadastrada"}}, 400

        session['plays'] = sorted(df_session_request.to_dict("records"), key=lambda d: d['entrance'])
        result = JokenpoResult(pd.DataFrame(session['plays']))
        result.get_winner()
        if result.winner.get('player'):
            return {"winner": f'Jogador - {result.winner.get("player")}'}, 200
        else:
            return {"winner": f'Ninguém ganhou'}, 200


@api.route('/player/<int:id>', doc={"description": "This request will delete all objects linked to it. Like an entrance and play."})
class PlayerJokenpo(Resource):
    @api.response(200, 'Success Player', delete_success)
    @api.response(400, 'Error Player', delete_error)
    def delete(self, id):
        df_session = pd.DataFrame(session['plays'])
        try:
            if df_session[df_session['player'] == id].empty:
                return {"error": f"Jogador {id} inválido ou não cadastrado"}, 400
            else:
                df_session = df_session.drop(df_session.index[df_session[df_session['player'] == id].index])
                session['plays'] = sorted(df_session.to_dict("records"), key=lambda d: d['entrance'])
                return {"success": f"Jogador {id} removido"}
        except KeyError:
            return {"error": f"Jogador {id} inválido ou não cadastrado"}, 400


@api.route('/entrance/<int:id>', doc={"description": "This request will delete all objects linked to it. Like a player and play."})
class EntranceJokenpo(Resource):
    @api.response(200, 'Success Player', delete_success)
    @api.response(400, 'Error Player', delete_error)
    def delete(self, id):
        df_session = pd.DataFrame(session['plays'])
        try:
            if df_session[df_session['entrance'] == id].empty:
                return {"error": f"Entrada {id} inválido ou não cadastrado"}, 400
            else:
                df_session = df_session.drop(df_session.index[df_session[df_session['entrance'] == id].index])
                session['plays'] = sorted(df_session.to_dict("records"), key=lambda d: d['entrance'])
                return {"success": f"Entrada {id} removido"}
        except KeyError:
            return {"error": f"Entrada {id} inválido ou não cadastrado"}, 400

@app.before_first_request
def before_request_func():
    session['plays'] = []
