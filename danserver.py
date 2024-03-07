import numpy as np

from typing import List, Tuple, Optional

from Player import GuanDanAI, Player
from Message import Message, MessageType
from Card import Card, CardDecor, CardComb

class GuanDanServer(object):
    
    def __init__(self):
        self.player_list : List[Player] = list()
        self.player_card : Tuple[List[int], List[int], List[int], List[int]] = None
        
    def add_player(self, player : Player) -> None:
        if len(self.player_list) < 4:
            self.player_list.append(player)
        else:
            raise ValueError("There are already 4 players!")
        
    def start_game(self, time : int = 1) -> None:
        assert time >= 1 and time <= 1e12

if __name__ == "__main__":
    server = GuanDanServer()
    
    # Create Player in order!
    # player1 = GuanDanAI(1)
    
    # Add Player in order!
    # server.add_player(player1)
    
    server.start_game(1)
    