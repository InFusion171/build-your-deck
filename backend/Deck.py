import hashlib

class Deck:
    def __init__(self, card_evo1: int, card_evo2: int, card3: int, card4: int, 
                 card5: int, card6: int, card7: int, card8: int) -> None:
        
        self.card_evos = [card_evo1, card_evo2]
        self.card_evos.sort()

        self.cards = [card3, card4, card5, card6, card7, card8]
        self.cards.sort()

    def __str__(self) -> str:
        return ','.join(self.card_evos + self.cards)
    
    def __hash__(self) -> str:
        hasher = hashlib.sha1(self.__str__().encode())
        
        # 10 hash digits are enough
        return hasher.hexdigest()[2:12]
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def get_deck(self) -> list[int]:
        return self.card_evos + self.cards

    