import numpy as np

from enum import IntEnum
from abc import abstractmethod

from Message import Message

class PlayerType(IntEnum):
    RULE_BASE = 0
    GUANDAN_AI = 1
    OTHER = 2

class Player(object):
    
    def __init__(self, player_id : int, player_type : PlayerType):
        self.player_id = player_id
        self.player_type = player_type
        
        self.cards = list()
    
    @abstractmethod
    def receive_message(self, message : Message):
        raise RuntimeError("This is an abstract method!")

class GuanDanAI(Player):
    
    def __init__(self, player_id : int):
        super().__init__(player_id, PlayerType.GUANDAN_AI)
    
    def receive_message(self, message: Message):
        pass