from typing import Any, Dict, Literal
from Database import Database
from Deck import Deck

import sqlalchemy as sql
from sqlalchemy import func, desc, select

class DeckDatabase(Database):
    def __init__(self, database_path: str, table_name: str):
        super().__init__(database_path, table_name)

        self.column_names = {
            'deck_id': 'DECK_ID',
            'card_1_evo': 'CARD_1_EVO',
            'card_2_evo': 'CARD_2_EVO',
            'card_1': 'CARD_1',
            'card_2': 'CARD_2',
            'card_3': 'CARD_3',
            'card_4': 'CARD_4',
            'card_5': 'CARD_5',
            'card_6': 'CARD_6',
            'card_7': 'CARD_7',
            'card_8': 'CARD_8',
            'tower_troop': 'TOWER_TROOP',
            'play_date': 'PLAY_DATE',
            'won_count': 'WON_COUNT',
            'lost_count': 'LOST_COUNT'
        }

        self.create_table()

        
    def create_table(self):
        self.metadata = sql.MetaData()

        self.decks_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column(self.column_names['deck_id'], sql.CHAR(12), primary_key=True),
                                    sql.Column(self.column_names['card_1_evo'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_2_evo'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_1'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_2'], sql.Integer(), nullable=True),
                                    sql.Column(self.column_names['card_3'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_4'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_5'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_6'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_7'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['card_8'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['tower_troop'], sql.Integer(), nullable=False),
                                    sql.Column(self.column_names['play_date'], sql.String(), nullable=False),
                                    sql.Column(self.column_names['won_count'], sql.INTEGER(), nullable=False),
                                    sql.Column(self.column_names['lost_count'], sql.INTEGER(), nullable=False),
                                    )
        
        self.metadata.create_all(self.engine)
        
    def add_decks(self, database: Database, decks: dict[int, Deck]):
        if decks is None:
            return

        transaction = database.connection.begin()

        for id, deck in decks.items():
            build_db_deck = deck.build_deck_for_db(self.column_names)

            if build_db_deck is None:
                continue

            if self.deck_id_exists(database, id):
                self.update_play_date(database, id, build_db_deck)
                self.update_won_lost_match_counter(database, id, build_db_deck)
            else:
                self.insert(database, build_db_deck)
        
        transaction.commit()

    def update_won_lost_match_counter(self, database: Database, deck_id: str, updated_deck_row: dict):
        column_won_count = self.column_names['won_count']
        column_lost_count = self.column_names['lost_count']

        database.connection.execute(
            self.decks_table.update().
            where(self.decks_table.c[self.column_names['deck_id']] == deck_id).
            values({
                column_won_count: self.decks_table.c[column_won_count] + 
                    updated_deck_row[column_won_count],

                column_lost_count: self.decks_table.c[column_lost_count] + 
                    updated_deck_row[column_lost_count]
            })
        )

    def deck_id_exists(self, database: Database, deck_id):
        exists = database.connection.execute(
            sql.select(self.decks_table.c[self.column_names['deck_id']]).
                where(self.decks_table.c[self.column_names['deck_id']] == deck_id)
        ).fetchone() 

        return exists != None

    def update_play_date(self, database: Database, deck_id: str, updated_deck_row: dict):
        database.connection.execute(
            self.decks_table.update().
            where(self.decks_table.c[self.column_names['deck_id']] == deck_id).
            values({
                self.column_names['play_date']: updated_deck_row[self.column_names['play_date']]
                })
        )
    
    def find_highest_level_war_decks(self, database: Database, card_levels: list[dict]):
        decks = []

        def find_card(id: int):
            for card in card_levels:
                if card['id'] == id:
                    return card
            
            return None

        card_copy = card_levels.copy()

        for _ in range(0,4):
            deck = self.find_highest_level_deck(database, card_copy)

            decks.append(deck)

            print(deck)

            card_copy.remove(find_card(deck[0]['CARD_1_EVO']))
            card_copy.remove(find_card(deck[0]['CARD_2_EVO']))
            card_copy.remove(find_card(deck[0]['CARD_3']))
            card_copy.remove(find_card(deck[0]['CARD_4']))
            card_copy.remove(find_card(deck[0]['CARD_5']))
            card_copy.remove(find_card(deck[0]['CARD_6']))
            card_copy.remove(find_card(deck[0]['CARD_7']))
            card_copy.remove(find_card(deck[0]['CARD_8']))

        def get_card_name(id: int):
            for card in card_levels:
                if card['id'] == id:
                    return card['name']

        for deck in decks:
            print(f'''
                {get_card_name(deck['CARD_1_EVO'])}, 
                {get_card_name(deck['CARD_2_EVO'])}, 
                {get_card_name(deck['CARD_3'])}, 
                {get_card_name(deck['CARD_4'])}, 
                {get_card_name(deck['CARD_5'])}, 
                {get_card_name(deck['CARD_6'])}, 
                {get_card_name(deck['CARD_7'])},
                {get_card_name(deck['CARD_8'])}'''.replace('\n', ''))


    def find_highest_level_deck(self, database: Database, card_levels: list[dict], deck_return_count: int = 1):
        evo_cards = [evo for evo in card_levels if 'evolutionLevel' in evo]
        evo_cards_id = [card['id'] for card in evo_cards]
        evo_cards_level_dict = {card['id']: card['level'] for card in evo_cards}

        cards_id = [card['id'] for card in card_levels]
        cards_level_dict = {card['id']: card['level'] for card in card_levels}

        def get_card_name(card_pos: int):
            if len(evo_cards_level_dict) == 0:
                return f'card_{card_pos}'
            
            if len(evo_cards_level_dict) == 1:
                if card_pos == 1:
                    return f'card_{card_pos}_evo'
                
                return f'card_{card_pos}'
                
            if card_pos <= 2:
                return f'card_{card_pos}_evo'
            
            return f'card_{card_pos}'

        # junk code but i don't know a better solution :(
        def get_level_dict(card_pos) -> dict:
            if len(evo_cards_level_dict) == 0:
                return cards_level_dict
            
            if len(evo_cards_level_dict) == 1:
                if card_pos == 1:
                    return evo_cards_level_dict
                
                return cards_level_dict
                
            if card_pos <= 2:
                return evo_cards_level_dict
            
            return cards_level_dict
       
        level_sum_expression = sum(
            sql.case(
                *[(self.decks_table.c[self.column_names[get_card_name(i)]] == card_id, level) 
                for card_id, level in get_level_dict(i).items()],
                else_=0
            ) for i in range(1, 9)
        )
        

        subquery = (
            sql.select(
                self.decks_table,
                level_sum_expression.label('total_level'),
            )
            .filter(
                sql.and_(
                    self.decks_table.c[self.column_names['card_1_evo']].in_(evo_cards_id),
                    self.decks_table.c[self.column_names['card_2_evo']].in_(evo_cards_id),
                    *[self.decks_table.c[self.column_names[f'card_{x}']].in_(cards_id) for x in range(3, 9)]
                )
            )
            .order_by(desc(level_sum_expression))  
            .subquery()
        )


        win_probability_expr = func.coalesce(
            subquery.c[self.column_names['won_count']] / 
            (subquery.c[self.column_names['won_count']] + subquery.c[self.column_names['lost_count']]), 
            0
        )

        query = (
            sql.select(
                *[subquery.c[col] for col in subquery.c.keys() if col != 'total_level']  
            )
            .filter(
                (subquery.c[self.column_names['won_count']] + subquery.c[self.column_names['lost_count']] > 10)
            )
            .order_by(
                desc(subquery.c['total_level']),  
                desc(win_probability_expr)        
            )
            .limit(deck_return_count)  
        )

        result = database.connection.execute(query)

        return [row._asdict() for row in result.fetchall()]
 
        
    # unused
    def delete_deck_id_duplicate(self, database: Database, deck_id):
        database.connection.execute(
            self.decks_table.delete().where(self.decks_table.c[self.column_names['deck_id']] == deck_id)
        )

    def insert(self, database: Database, deck_row: dict):
        database.connection.execute(
            self.decks_table.insert().values(deck_row)
        )