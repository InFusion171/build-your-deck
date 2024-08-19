import hashlib

class Deck:
    def __init__(self, card_evo1: int, card_evo2: int, card3: int, card4: int, 
                 card5: int, card6: int, card7: int, card8: int, tower_troop_id: int, 
                 play_date: str) -> None:
        
        self.play_date = play_date

        self.card_evos = [card_evo1, card_evo2]
        self.card_evos.sort()

        self.cards = [card3, card4, card5, card6, card7, card8]
        self.cards.sort()

        self.tower_troop_id = tower_troop_id

        self.won_count = 0
        self.lost_count = 0

    def __str__(self) -> str:
        return ','.join(map(str, self.card_evos + self.cards + [self.tower_troop_id]))
    
    def __hash__(self) -> str:
        hasher = hashlib.shake_256(self.__str__().encode())
        
        return hasher.hexdigest(6)
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def get_id(self):
        return self.__hash__()

    def build_deck_for_db(self, database) -> dict:
        deck_row = {
                    database.column_names['deck_id']: self.get_id(),
                    database.column_names['card_1_evo']: self.card_evos[0],
                    database.column_names['card_2_evo']: self.card_evos[1],

                    # +3 because we want to start at 3
                    **{database.column_names[f'card_{card_number + 3}']: self.cards[card_number] 
                       for card_number in range(len(self.cards))},

                    database.column_names['tower_troop']: self.tower_troop_id,
                    database.column_names['play_date']: self.play_date,
                    database.column_names['won_count']: self.won_count,
                    database.column_names['lost_count']: self.lost_count
                }

        return deck_row

    