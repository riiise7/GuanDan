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