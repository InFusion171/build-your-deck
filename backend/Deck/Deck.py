import hashlib

from Card.CardDatabase import CardDatabase


class Deck:
    def __init__(self, card_evos: list, cards: list, tower_troop_id: int, 
                 play_date: str) -> None:
        
        self.play_date = play_date

        self.card_evos = card_evos
        self.card_evos.sort()

        self.cards = cards
        self.cards.sort()

        self.tower_troop_id = tower_troop_id

        self.won_count = 0
        self.lost_count = 0

        self.trophies = -1

    def __str__(self) -> str:
        with CardDatabase() as database:
            return database.get_deck_cards(self.card_evos, self.cards)
    
    def delete_deck_cards_from_cards(self, all_cards: list[dict]) -> None:

        for card in self.card_evos + self.cards:
            for all_card in all_cards:
                if card == all_card.get('id'):
                    all_cards.remove(all_card)
                    break

    def __hash__(self) -> str:
        deck_string = ','.join(map(str, self.card_evos + self.cards + [self.tower_troop_id]))

        hasher = hashlib.shake_256(deck_string.encode())
        
        return hasher.hexdigest(6)
    
    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def get_id(self):
        return self.__hash__()

    def build_deck_for_db(self, column_names: dict) -> dict:   
        if len(self.card_evos + self.cards) != 8:
            print('we need 8 total cards')
            return None

        if self.trophies == -1:
            return None

        base_row = {
                    column_names['deck_id']: self.get_id(),
                    column_names['tower_troop']: self.tower_troop_id,
                    column_names['play_date']: self.play_date,
                    column_names['trophies']: self.trophies,
                    column_names['won_count']: self.won_count,
                    column_names['lost_count']: self.lost_count
                }

        create_db_cards_row = lambda card_offset: {column_names[f'card_{card_number + card_offset}']: self.cards[card_number] 
                                    for card_number in range(len(self.cards))}

        if len(self.card_evos) == 0:
            self.deck_row = base_row | create_db_cards_row(1)

        if len(self.card_evos) == 1:
            self.deck_row = base_row | {column_names['card_1_evo'] : self.card_evos[0]} | create_db_cards_row(2)

        if len(self.card_evos) == 2:
            self.deck_row = base_row | {column_names['card_1_evo']: self.card_evos[0],
                                   column_names['card_2_evo']: self.card_evos[1]} | create_db_cards_row(3)

        return self.deck_row

    