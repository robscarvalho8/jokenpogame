from flask_restx import fields

from api.server.instance import server

play = server.api.model('Play',{
    'player': fields.Integer(required=True, description='Número do jogador.'),
    'entrance': fields.Integer(required=True, description='Número da Entrada.'),
    'play': fields.String(required=True, min_length=1, max_length=200, description='Jogada'),
})

delete_play = server.api.model('Delete Play', {
    'player': fields.Integer(description='Número do jogador.'),
    'entrance': fields.Integer(description='Número da Entrada.'),
})

success = server.api.model('Success',{
    'winner': fields.String(min_length=1, max_length=200, description='Descritivo da vitória ou da derrota'),
})

player_number = server.api.model('Player Error', {
    'entrance': fields.String(description='Números das entradas já cadastrados'),
    'player': fields.String(description='Números dos jogadores já cadastrados'),
})

error = server.api.model('Error',{
    "error": fields.Nested(player_number)
})