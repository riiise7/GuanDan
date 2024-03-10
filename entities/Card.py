import numpy as np

from math import floor
from enum import IntEnum

from typing import List, Optional, Tuple, Union

'''
Danzero的作者似乎把方块和梅花搞反了，C（Club）应该是梅花，D（Diamond）应该是方块。
具体的需要看内部代码怎么写的，现在还在研究！
'''
class CardDecor(IntEnum):
    #"红桃"
    H = 0
    #黑桃
    S = 1
    #"方块"
    C = 2
    #"梅花"
    D = 3
    #"没有"，仅限大王小王
    N = 4

class Card(object):
    
    def __init__(self, card_atrributes : Tuple[int, CardDecor]):
        assert card_atrributes[0] <= 15 and card_atrributes[0] >= 1
        self.card_number = card_atrributes[0]
        self.card_decor = card_atrributes[1]
    
    @classmethod
    def create_card_attributes_from_value(cls, value : int) -> Tuple[int, CardDecor]:
        card_decor = floor(value / 13)
        if card_decor == 4:
            return (value - 38, CardDecor(4))
        card_number = value % 13 + 1
        return (card_number, CardDecor(card_decor))
        
    
    def __str__(self) -> str:
        if self.card_number >= 14:
            return "SB" if self.card_number == 14 else "HR"
        else:
            answer = ""
            if self.card_decor == CardDecor.H :
                answer += "H"
            elif self.card_decor == CardDecor.S :
                answer += "S"
            elif self.card_decor == CardDecor.C :
                answer += "C"
            elif self.card_decor == CardDecor.D :
                answer += "D"
            else:
                raise ValueError("Unknown Card Decor!")
            
            if self.card_number > 8:
                if self.card_number == 9:
                    answer += "T"
                elif self.card_number == 10:
                    answer += "J"
                elif self.card_number == 11:
                    answer += "Q"
                elif self.card_number == 12:
                    answer += "K"
                else:
                    answer += "A"
            
            return answer
    
    def card_value(self):
        if self.card_number >= 14:
            return 52 if self.card_number == 14 else 53
        return self.card_decor * 13 + self.card_number

class CombType(IntEnum):
    PASS = -1
    Single = 0
    Pair = 1
    Trips = 2
    ThreePair = 3
    ThreeWithTwo = 4
    TwoTrips = 5
    Straight = 6
    StraightFlush = 7
    Bomb = 8
    

class CardComb(object):
    
    def __init__(self, comb_type : CombType, cards : Optional[Union[List[Card], List[Tuple[int, CardDecor]]]]):
        self.comb_type = comb_type
        self.cards : Optional[List[Card]] = None
        if int(comb_type) > -1:
            self.cards = list()
            assert len(cards) > 0
            obj = cards[0]
            if isinstance(obj, Card):
                self.cards = cards
            elif isinstance(obj, Tuple):
                assert len(cards[0]) == 2
                assert isinstance(cards[0][0], int)
                assert isinstance(cards[0][1], CardDecor)
                for attribute in cards:
                    self.cards.append(Card(attribute))
    
    def to_nplist(self) -> np.ndarray:
        pass
    
    def __str__(self) -> str:
        '''
        案例1：
        self.combo_type = CombType.Pair
        self.cards = [Card(10, H), Card(10, D)]
        输出：['Pair','HT','DT']
        案例2：
        self.combo_type = CombType.Single
        self.cards = [Card(14, N)]
        输出：['Single','SB']
        案例3：
        self.combo_type = PASS
        self.cards = None
        输出：['None']
        '''
        str_comb = ''
        if self.combo_type == CombType.Single:
            str_comb = str_comb +  str(CombType.Single) + str(self.cards)
        elif self.combo_type == CombType.Pair:
            str_comb = str_comb +  str(CombType.Pair) + str(self.cards)
        elif self.combo_type == CombType.Trips:
            str_comb = str_comb +  str(CombType.Trips) + str(self.cards)
        elif self.combo_type == CombType.ThreePair:
            str_comb = str_comb +  str(CombType.ThreePair) + str(self.cards)
        elif self.combo_type == CombType.ThreeWithTwo:
            str_comb = str_comb +  str(CombType.ThreeWithTwo) + str(self.cards)
        elif self.combo_type == CombType.TwoTrips:
            str_comb = str_comb +  str(CombType.TwoTrips) + str(self.cards)
        elif self.combo_type == CombType.Straight:
            str_comb = str_comb +  str(CombType.Straight) + str(self.cards)
        elif self.combo_type == CombType.StraightFlush:
            str_comb = str_comb +  str(CombType.StraightFlush) + str(self.cards)
        elif self.combo_type == CombType.Bomb:
            str_comb = str_comb +  str(CombType.Bomb) + str(self.cards)
        return str_comb
        pass