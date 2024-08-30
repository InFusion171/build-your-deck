from Database import Database
from Deck.Deck import Deck

import sqlalchemy as sql
from sqlalchemy import func, desc, select

class DeckDatabase(Database):
    database_path = ''
    table_name = ''

    @classmethod
    def setup_database_connection(cls, database_path: str, table_name: str):
        cls.database_path = database_path
        cls.table_name = table_name

    def __init__(self):
        super().__init__(self.database_path, self.table_name)

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
            'trophies': 'TROPHIES',
            'won_count': 'WON_COUNT',
            'lost_count': 'LOST_COUNT'
        }

        self.create_table()

        
    def create_table(self):
        self.metadata = sql.MetaData()

        self.decks_table = sql.Table(self.table_name, self.metadata,
                                    sql.Column(self.column_names['deck_id'], sql.String(), primary_key=True),
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
                                    sql.Column(self.column_names['trophies'], sql.INTEGER(), nullable=False),
                                    sql.Column(self.column_names['won_count'], sql.INTEGER(), nullable=False),
                                    sql.Column(self.column_names['lost_count'], sql.INTEGER(), nullable=False),
                                    )
        
        self.metadata.create_all(self.engine)
        
    def add_decks(self, database: Database, decks: list[Deck]):
        if not decks:
            return

        new_decks: list[dict] = []
        existing_decks: list[dict] = []

        existing_deck_ids = self.get_existing_deck_ids(database, set([deck.get_id() for deck in decks]))

        for deck in decks:
            build_db_deck = deck.build_deck_for_db(self.column_names)

            if build_db_deck is None:
                continue

            if build_db_deck[self.column_names['deck_id']] in existing_deck_ids:
                existing_decks.append(build_db_deck)
            else:
                new_decks.append(build_db_deck)

    
        if new_decks:
            self.insert(database, Deck.compress(new_decks, self.column_names))

        if existing_decks:
            self.update_values(database, existing_decks)





    def get_play_date(self, database: Database, deck_id: str) -> str:
        result = database.exec_query(
            select(self.decks_table.c[self.column_names['play_date']]).
            where(self.decks_table.c[self.column_names['deck_id']] == deck_id)
        )

        return result[0]._asdict()[self.column_names['play_date']]

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

    def get_existing_deck_ids(self, database: Database, deck_ids: set) -> set[str]:
        existing_deck_ids_result = database.exec_query(
            select(self.decks_table.c[self.column_names['deck_id']])
            .where(self.decks_table.c[self.column_names['deck_id']].in_(deck_ids))
        )

        return set(row[0] for row in existing_deck_ids_result)


    def update_values(self, database: Database, decks_to_update: list[dict]):
        deck_id_col = self.column_names['deck_id']
        play_date_col = self.column_names['play_date']
        
        for deck in decks_to_update:
            deck_id = deck[self.column_names['deck_id']]
            won_count_col = self.column_names['won_count']
            lost_count_col = self.column_names['lost_count']
            trophies_col = self.column_names['trophies']

            update_stmt = (
                self.decks_table.update()
                .where(
                    (self.decks_table.c[deck_id_col] == deck_id) &
                    (self.decks_table.c[play_date_col] < deck[play_date_col])
                )
                .values({
                    won_count_col: self.decks_table.c[won_count_col] + deck[won_count_col],
                    lost_count_col: self.decks_table.c[lost_count_col] + deck[lost_count_col],
                    trophies_col: func.max(self.decks_table.c[trophies_col], deck[trophies_col]),
                    play_date_col: deck[play_date_col]
                })
            )

            try:
                database.connection.execute(update_stmt)
                database.connection.commit()
            except Exception as e:
                database.connection.rollback()
                print('couldnt update values')




    def find_highest_level_war_decks(self, database: Database, cards: list[dict]):
        decks = []

        card_copy = cards.copy()

        for _ in range(0,4):
            deck_list = self.find_highest_level_deck(database, card_copy)
            
            if len(deck_list) == 0:
                continue

            deck = deck_list[0]

            deck.delete_deck_cards_from_cards(card_copy)

            decks.append(deck)



    def find_highest_level_deck(self, database: Database, card_levels: list[dict], deck_return_count: int = 1) -> list[Deck]:
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
            #.filter(
             #   (subquery.c[self.column_names['won_count']] + subquery.c[self.column_names['lost_count']] > 30)
            #)
            .order_by(
                desc(subquery.c['total_level']), 
                desc(self.column_names['trophies']), 
                desc(win_probability_expr)        
            )
            .limit(deck_return_count)  
        )

        result = database.connection.execute(query)

        deck_rows = [row._asdict() for row in result.fetchall()]

        decks = []

        for deck in deck_rows:
            evo_cards = []
            cards = []

            for colmn_name, card_id in deck.items():
                if colmn_name == self.column_names['card_1_evo']:
                    evo_cards.append(card_id)

                elif colmn_name == self.column_names['card_2_evo']:
                    evo_cards.append(card_id)

                elif 'CARD_' in colmn_name and card_id != None:
                    cards.append(card_id)

            decks.append(Deck(evo_cards, cards, deck[self.column_names['tower_troop']], deck[self.column_names['play_date']]))

        return decks
 

    def insert(self, database: Database, deck_rows: list[dict]):
        try:
            database.connection.execute(self.decks_table.insert(), deck_rows)
            database.connection.commit()
        except Exception as e:
            database.connection.rollback()
            print('couldnt insert values')