import numpy as np

from enum import IntEnum
from abc import abstractmethod
from typing import Optional, List

from entities.Message import Message, NotifyMessage
from entities.Card import Card

class PlayerType(IntEnum):
    DEALER = -1
    RULE_BASE = 0
    GUANDAN_AI = 1
    OTHER = 2

class Player(object):
    
    def __init__(self, player_id : int, player_type : PlayerType):
        self.player_id = player_id
        self.player_type = player_type
        
        self.cards : Optional[List[Card]] = None
    
    @abstractmethod
    def receive_message(self, message : Message) -> None:
        raise RuntimeError("This is an abstract method!")

class GuanDanAI(Player):
    
    def __init__(self, player_id : int):
        super().__init__(player_id, PlayerType.GUANDAN_AI)
        self.cards = list()
    
    def receive_message(self, message: Message) -> None:
        if isinstance(message, NotifyMessage):
            pass
            
    
    def add_cards(self, cards : List[Card]):
        for card in cards:
            self.cards.append(Card([card.card_number, card.card_decor]))

class Dealer(Player):
    
    def __init__(self):
        super().__init__(-1, player_type=PlayerType.DEALER)
        
    def receive_messae(self, message : Message) -> None:
        pass