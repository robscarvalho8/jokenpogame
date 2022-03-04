from flask import Flask
from flask_restx import Api

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'mysecret1'
        self.api = Api(self.app,
                       version='1.0',
                       title="Jokenpô API",
                       description="A simple jokenpo API",
                       doc="/docs",
                       )
    def run(self):
        self.app.run(
            debug=True
        )

server = Server()