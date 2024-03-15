import numpy as np

from typing import List, Tuple, Optional

from entities.Player import GuanDanAI, Player
from entities.Message import Message, MessageType
from entities.Card import Card, CardDecor, CardComb

class GuanDanServer(object):
    
    def __init__(self):
        # 玩家列表，按顺序是[0号，1号，2号，3号]
        # 中途玩家可以退出，换新玩家上场，但必须在本次游戏结束后
        self.player_list : List[Optional[Player]] = [None] * 4
        self.is_playing : bool = False
        
    def add_player(self, player : Player, index : int = -1) -> None:
        assert index < 4 and index >= -1
        if self.is_playing:
            raise ValueError("Current game is in progress!")
        if sum(isinstance(x, Player) for x in self.player_list) < 4:
            if index == -1:
                self.player_list[self.player_list.index(None)] = player
            else:
                self.player_list[index] = player
        else:
            raise ValueError("There are already 4 players!")
        
    def start_game(self, time : int = 1) -> None:
        assert time >= 1 and time <= 1e12
        self.is_playing = True
        
        for _ in range(time):
            # [现在等级，1号队伍等级，2号队伍等级]
            # 1号队伍是0号和2号玩家；2号队伍是1号和3号玩家
            levels = list([1, 1, 1])
            
            print(f"Current level is {Card.card_number_to_level(levels[0])}")
            
            
        
        self.is_playing = False

if __name__ == "__main__":
    server = GuanDanServer()
    
    # Create Player in order!
    # player1 = GuanDanAI(1)
    
    # Add Player in order!
    # server.add_player(player1)
    
    server.start_game(1)
    