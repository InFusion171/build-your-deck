
class Card:
    @staticmethod
    def normalize_card_level(card_rarity: str, card_level: int) -> int:
        match card_rarity:
            case 'common':
                return card_level
            case 'rare':
                return card_level + 2
            case 'epic':
                return card_level + 5
            case 'legendary':
                return card_level + 8
            case 'champion':
                return card_level + 10