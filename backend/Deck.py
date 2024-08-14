
from numpy import sort


class Deck:
    def __init__(self, card_evo1: str, card_evo2: str, card3: str, card4: str, 
                 card5: str, card6: str, card7: str, card8: str) -> None:
        
        self.card_evos = [card_evo1, card_evo2]
        self.card_evos.sort()

        self.cards = [card3, card4, card5, card6, card7, card8]
        self.cards.sort()

    def __str__(self) -> str:
        return ','.join(self.card_evos + self.cards)
    
    def __hash__(self) -> int:
        return hash(self.__str__())

    