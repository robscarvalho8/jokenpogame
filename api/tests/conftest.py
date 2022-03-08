import pytest
from api.views.jokenpo import app

@pytest.fixture
def client():
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    with app.test_client() as client:
        return client

@pytest.fixture
def patterns_plays():
    patterns_plays = [
        {
            "player": 1,
            "play": "pedra",
            "entrance": 1,
        },
        {
            "player": 2,
            "play": "papel",
            "entrance": 2,
        },
        {
            "player": 3,
            "play": "tesoura",
            "entrance": 3,
        },
        {
            "player": 4,
            "play": "lagarto",
            "entrance": 4,
        },
        {
            "player": 5,
            "play": "spock",
            "entrance": 5,
        },
    ]

    return patterns_plays

@pytest.fixture
def player_duplicated():
    player_duplicated =[
            {
                "player": 1,
                "play": "tesoura",
                "entrance": 1
            },
            {
                "player": 1,
                "play": "papel",
                "entrance": 2
            },
        ]
    return player_duplicated

@pytest.fixture
def entrance_duplicated():
    entrance_duplicated =[
            {
                "player": 1,
                "play": "tesoura",
                "entrance": 1
            },
            {
                "player": 2,
                "play": "papel",
                "entrance": 1
            },
        ]
    return entrance_duplicated

@pytest.fixture
def invalid_play():
    invalid_play = [
        {
            "player": 1,
            "play": "CANIVETE",
            "entrance": 1,
        }
    ]

    return invalid_play