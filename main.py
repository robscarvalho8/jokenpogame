from api.server.instance import server
from api.views.jokenpo import PlayJokenpo, PlayerJokenpo, EntranceJokenpo

server = server.app

if __name__ == '__main__':
    server.run()