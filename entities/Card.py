import numpy as np

from math import floor
from enum import IntEnum

from typing import List, Optional, Tuple

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
    
    def __init__(self, card_atrributes : Tuple[int, CardDecor], level_card : bool = False):
        assert card_atrributes[0] <= 15 and card_atrributes[0] >= 1
        # 卡数是从1到15。
        # 1对应的是2，2对应的是3，直到13对应的是A，14和15分别对应小王和大王
        self.card_number = card_atrributes[0]
        
        # 卡的花色，小王和大王没有花色
        self.card_decor = card_atrributes[1]
        
        self.level_card : bool = level_card
    
    @classmethod
    def create_card_attributes_from_value(cls, value : int) -> Tuple[int, CardDecor]:
        card_decor = floor(value / 13)
        if card_decor == 4:
            return (value - 38, CardDecor(4))
        card_number = value % 13 + 1
        return (card_number, CardDecor(card_decor))
    
    @classmethod
    def card_number_to_level(cls, value : int) -> str:
        assert value <= 13 and value >= 1
        if value < 9:
            return str(value + 1)
        if value == 9:
            return "T"
        if value == 10:
            return "J"
        if value == 11:
            return "Q"
        if value == 12:
            return "K"
        return "A"

    def __lt__(self, other : object) -> bool:
        if self.card_number < other.card_number:
            return True
        if self.card_number == other.card_number:
            return self.card_decor < other.card_decor
        return False

    def __eq__(self, other: object) -> bool:
        return self.card_number == other.card_number and self.card_decor == other.card_decor
    
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
            else:
                answer += str(self.card_number)
            
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
    
    def __str__(self) -> str:
        if self.value == -1:
            return "Pass"
        if self.value == 0:
            return "Single"
        if self.value == 1:
            return "Pair"
        if self.value == 2:
            return "Trips"
        if self.value == 3:
            return "ThreePair"
        if self.value == 4:
            return "ThreeWithTwo"
        if self.value == 5:
            return "TwoTrips"
        if self.value == 6:
            return "Straight"
        if self.value == 7:
            return "StraightFlush"
        if self.value == 8:
            return "Bomb"
        raise ValueError("Invalid self.value!!!")     

class CardComb(object):
    
    def __init__(self, comb_type : CombType, cards : Optional[List[Card]], feature : Optional[Tuple[int, int]], decor : Optional[CardDecor]):
        '''
        @param feature:
        # 如果是Pass,Single,Pair或者Triple,则为None.
        # 如果是ThreePair,就是(最小卡值,最大卡值);例如["H5", "H5", "S6", "S6", "C7", "D7"]的feature是(4,6).
        # 如果是TwoTrips,就是(最小卡值,最大卡值);例如["H5", "H5", "S5", "S6", "C6", "D6"]的feature是(4,5).
        # 如果是ThreeWIthTwo,就是(Trips值,Pair值);例如["HT", "HT", "DT", "SA", "CA"]的feature是(9,13).
        # 如果是Straight,就是(最小卡值,最大卡值);例如["HA", "D2", "S3", "S4", "C5"]的feature是(13,4).
        # 如果是StraightFlush,就是(最小卡值,最大卡值);例如["D2", "D3", "D4", "D5", "D6"]的feature是(1,5).
        # 如果是Bomb,就是(卡牌数,卡值);例如["HT", "HT", "ST", "CT", "DT", "DT"]的feature是(6,9).
        # 如果是王炸,固定为(100,100).
        '''
        self.comb_type = comb_type
        self.cards : Optional[List[Card]] = None
        self.level_red_heart = list([-1, -1])
        self.feature = feature
        self.decor = decor
        if int(comb_type) > -1:
            assert len(cards) > 0
            self.cards = [None] * len(cards)
            
            if feature is not None:
                pass

    def self_sorting(self) -> None:
        if self.level_red_heart.count(-1) == 2:
            if self.comb_type == -1 or self.comb_type == 0:
                return
            elif self.comb_type.value != 4:
                list.sort(self.cards)
                return
        elif self.level_red_heart.count(-1) == 1:
            pass
    
    def to_ndarray(self) -> np.ndarray:
        if self.cards == None:
            return np.array([-1])
        shape = (len(self.cards),)
        array_comb = np.empty(shape, dtype=Card)
        for i in range(shape[0]):
            array_comb[i] = self.cards[i]
        return array_comb

    
    def __str__(self) -> str:
        '''
        案例1：
        self.combo_type = CombType.Pair
        self.cards = [Card(10, H), Card(10, D)]
        输出：[Pair,HT,DT]
        案例2：
        self.combo_type = CombType.Single
        self.cards = [Card(14, N)]
        输出：[Single,SB]
        案例3：
        self.combo_type = PASS
        self.cards = None
        输出：[None]
        '''
        if self.comb_type == CombType.PASS:
            return "[None]"
        
        str_comb = "["
        str_comb += str(self.comb_type)
        str_comb += ","
        
        for card in self.cards:
            str_comb += str(card)
            str_comb += ","
        str_comb = str_comb.rstrip(str_comb[-1])
        str_comb += "]"
        
        return str_comb

    @classmethod
    def check_combo_type(cls, combo_type: CombType, cards : Optional[List[Card]], feature : Optional[Tuple[int, int]], decor : Optional[CardDecor] = None) -> bool:
        if combo_type == CombType.PASS:
            return cards == None and feature == None
        if combo_type == CombType.Single:
            return len(cards) == 1 and feature == None
        if combo_type == CombType.Pair:
            if feature != None:
                return False
            # Todo
        if combo_type == CombType.Trips:
            if feature != None:
                return False
            # Todo
        if combo_type == CombType.ThreePair:
            if not isinstance(feature, tuple):
                return False
            # Todo
        if combo_type == CombType.ThreeWithTwo:
            if not isinstance(feature, tuple):
                return False
            # Todo
        if combo_type == CombType.TwoTrips:
            if not isinstance(feature, tuple):
                return False
            # Todo
        if combo_type == CombType.Straight:
            if not isinstance(feature, tuple):
                return False
            # Todo
        if combo_type == CombType.StraightFlush:
            if not isinstance(feature, tuple):
                return False
            if decor == None or decor == CardDecor.N:
                return False
            
            expected_card_decor = [decor] * 5
            for card in cards:
                if (card.level_card and card.card_decor == CardDecor.H) or card.card_decor == decor:
                    expected_card_decor.remove(decor)
                else:
                    return False
            
            if len(expected_card_decor) > 0:
                return False
            
            min_val, max_val = feature[0], feature[1]
            expected_card_values = list([min_val, max_val - 3, max_val - 2, max_val - 1, max_val])
            level_red_heart_count = 0
            for card in cards:
                if card.level_card and card.card_decor == CardDecor.H:
                    level_red_heart_count += 1
                elif card.card_number in expected_card_values:
                    expected_card_values.remove(card.card_number)
                else:
                    return False
            
            if len(expected_card_values) > level_red_heart_count:
                return False
            return True
        if combo_type == CombType.Bomb:
            if not isinstance(feature, tuple):
                return False
            if feature[0] == 100 and feature[1] == 100:
                expected_card_values = list([52, 52, 53, 53])
                for card in cards:
                    if card.card_value() in expected_card_values:
                        expected_card_values.remove(card.card_value())
                    else:
                        return False
                return len(expected_card_values) == 0
            else:
                if len(cards) != feature[0]:
                    return False
                expected_card_values = [feature[1]] * feature[0]
                for card in cards:
                    if card.card_number in expected_card_values or (card.level_card and card.card_decor == CardDecor.H):
                        expected_card_values.remove(feature[1])
                    else:
                        return False
                return len(expected_card_values) == 0
        raise ValueError("Invalid CombType!s")