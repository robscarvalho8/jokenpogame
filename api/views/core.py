from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
import pandas as pd

class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # stone.set_next(paper).set_next(scissors)
        return handler

    @abstractmethod
    def handle(self, request: Any, df: pd.DataFrame):
        if self._next_handler:
            return self._next_handler.handle(request, df)

        return None


class StoneHandler(AbstractHandler):
    def handle(self, request: Any, df: pd.DataFrame):
        if request.lower() == "pedra":
            try:
                play2 = df.sort_values(by=['entrance'], ascending=True).iloc[1].to_dict().get('play')
            except IndexError:
                next_play = ''
                return df, next_play

            if play2 in ['tesoura', 'lagarto', 'pedra']:
                df = df.drop(df.index[1])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            else:
                df = df.drop(df.index[0])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            return df, next_play
        else:
            return super().handle(request, df)


class PaperHandler(AbstractHandler):
    def handle(self, request: Any, df: pd.DataFrame):
        if request.lower() == "papel":
            try:
                play2 = df.sort_values(by=['entrance'], ascending=True).iloc[1].to_dict().get('play')
            except IndexError:
                next_play = ''
                return df, next_play

            if play2 in ['spock', 'pedra', 'papel']:
                df = df.drop(df.index[1])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            else:
                df = df.drop(df.index[0])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            return df, next_play
        else:
            return super().handle(request, df)


class ScissorHandler(AbstractHandler):
    def handle(self, request: Any, df: pd.DataFrame):
        if request.lower() == "tesoura":
            try:
                play2 = df.sort_values(by=['entrance'], ascending=True).iloc[1].to_dict().get('play')
            except IndexError:
                next_play = ''
                return df, next_play

            if play2 in ['lagarto', 'papel', 'tesoura']:
                df = df.drop(df.index[1])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            else:
                df = df.drop(df.index[0])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            return df, next_play
        else:
            return super().handle(request, df)


class LizardHandler(AbstractHandler):
    def handle(self, request: Any, df: pd.DataFrame):
        if request.lower() == "lagarto":
            try:
                play2 = df.sort_values(by=['entrance'], ascending=True).iloc[1].to_dict().get('play')
            except IndexError:
                next_play = ''
                return df, next_play

            if play2 in ['papel', 'spock', 'lagarto']:
                df = df.drop(df.index[1])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            else:
                df = df.drop(df.index[0])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            return df, next_play
        else:
            return super().handle(request, df)


class SpockHandler(AbstractHandler):
    def handle(self, request: Any, df: pd.DataFrame):
        if request.lower() == "spock":
            try:
                play2 = df.sort_values(by=['entrance'], ascending=True).iloc[1].to_dict().get('play')
            except IndexError:
                next_play = ''
                return df, next_play

            if play2 in ['pedra', 'tesoura', 'spock']:
                df = df.drop(df.index[1])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            else:
                df = df.drop(df.index[0])
                next_play = df.sort_values(by=['entrance'], ascending=True).iloc[0].to_dict().get('play')
            return df, next_play
        else:
            return super().handle(request, df)


class JokenpoResult():
    def __init__(self, df:pd.DataFrame):
        stone = StoneHandler()
        paper = PaperHandler()
        scissor = ScissorHandler()
        lizard = LizardHandler()
        spock = SpockHandler()
        stone.set_next(paper).set_next(scissor).set_next(lizard).set_next(spock)
        self.df = df
        self.jokenpo = stone
        self.winner = {}

    def get_winner(self):
        self.df['play'] = self.df['play'].str.lower()
        self.df = self.df.sort_values(by=['entrance'], ascending=True)
        next_play = self.df.iloc[0].to_dict().get('play')
        while next_play:
            self.df, next_play = self.jokenpo.handle(next_play, self.df)
        self.winner = self.df.to_dict('records')[0]
