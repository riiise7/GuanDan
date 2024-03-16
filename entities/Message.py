import json

from typing import Tuple
from abc import abstractmethod

from entities.Card import Card, CardComb

class Message(object):
    
    def __init__(self, src_player_id : int, dsct_player_id : int):
        self.src_player_id = src_player_id
        self.dsct_player_id = dsct_player_id

    @abstractmethod
    def to_json_str(self) -> str:
        raise RuntimeError("This is an abstract method!")

class NotifyMessage(Message):

    # 只有发牌员会发送NotifyMessage给其他玩家，因此src_player_id一定是-1
    def __init__(self, dsct_player_id : int, message : Message):
        super().__init__(-1, dsct_player_id)
        self.message : Message = message

    def to_json_str(self) -> str:
        json_dict = {
            'src_id': -1,
            'dsct_id': self.dsct_player_id,
        }
        return json.dumps(json_dict)

class PlayCardMessage(Message):

    # 玩家只会向发牌员发送PlayCardMessage，因此dsct_player_id一定是-1
    def __init__(self, src_player_id, cardcomb : CardComb):
        super().__init__(src_player_id, -1)
        self.cardcomb : CardComb = cardcomb

    def to_json_str(self) -> str:

        pass

class TributeMessage(Message):

    # 玩家进贡还贡时向对方发送TributeMessage，玩家不会向发牌员发送此类消息
    def __init__(self, src_player_id: int, dsct_player_id: int, card : Card):
        super().__init__(src_player_id, dsct_player_id)
        self.card : Card = card

    def to_json_str(self) -> str:
        pass

class AntiTributeMessage(Message):

    # 两个玩家（两个玩家可以是同一个玩家）抗贡，src_player_id和dsct_player_id分别记录两个抗贡玩家的id
    def __init__(self, src_player_ids : Tuple[int, int]):
        super().__init__(src_player_ids[0], src_player_ids[1])

    def to_json_str(self) -> str:
        pass