from flask_restx import fields

from api.server.instance import server

play = server.api.model('Play', {
    'player': fields.Integer(required=True, description='Player Number'),
    'entrance': fields.Integer(required=True, description='Entrance Number'),
    'play': fields.String(required=True, min_length=1, max_length=200, description='Play'),
})

success = server.api.model('Success', {
    'winner': fields.String(min_length=1, max_length=200, description='Return message with winning player.'),
})

player_number = server.api.model('Player Error', {
    'entrance': fields.String(description='Return message with numbers of entries already registered.'),
    'player': fields.String(description='Return message with numbers of players already registered.'),
    'play': fields.String(description='Return message with invalid play.'),
})

error = server.api.model('Error', {
    "error": fields.Nested(player_number)
})

delete_success = server.api.model('Delete Play Success', {
    'success': fields.String(description='Return a success message.'),
})

delete_error = server.api.model('Delete Play Error', {
    'error': fields.String(description='Return an error message.'),
})
