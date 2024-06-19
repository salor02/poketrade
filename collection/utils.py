def get_cards_by_set(cards):
    cards_by_set = {}
    for card in cards:
        if not card.set in cards_by_set:
            cards_by_set[card.set] = []
        cards_by_set[card.set].append(card)
    return cards_by_set