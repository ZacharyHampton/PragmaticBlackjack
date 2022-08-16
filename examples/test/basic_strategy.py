def basic_strategy(player_val, dealer_val, soft):
    if soft:
        if player_val == 9:
            return 'stand'
        if player_val == 8:
            if dealer_val == 6:
                return 'double'
            return 'stand'
        if player_val == 7:
            if dealer_val in [3, 4, 5, 6]:
                return 'double'
            if dealer_val in [9, 10]:
                return 'hit'
            return 'stand'
        if player_val == 6:
            if dealer_val in [1, 7, 8, 9, 10]:
                return 'hit'
            return 'double'
        if player_val in [2, 3, 4, 5]:
            if dealer_val in [4, 5, 6]:
                return 'double'
            return 'hit'

        if player_val == 12:
            if dealer_val not in [4, 5, 6]:
                return 'stand'
            return 'hit'
        if player_val in [13, 14, 15, 16]:
            if dealer_val in [2, 3, 4, 5, 6]:
                return 'stand'
            return 'hit'
        if player_val >= 17:
            return 'stand'

    if 4 <= player_val <= 7:
        return 'hit'
    if player_val == 8:
        if dealer_val not in [5, 6]:
            return 'double'
        return 'hit'
    if player_val == 9:
        if dealer_val not in [1, 2, 7, 8, 9, 10]:
            return 'double'
        return 'hit'
    if player_val == 10:
        if dealer_val not in [1, 10]:
            return 'double'
        return 'hit'
    if player_val == 11:
        if dealer_val in [1, 10]:
            return 'hit'
        return 'double'

    else:
        if player_val == 12:
            if dealer_val not in [1, 2, 3, 7, 8, 9, 10]:
                return 'stand'
            return 'hit'
        if 13 <= player_val <= 16:
            if dealer_val in [2, 3, 4, 5, 6]:
                return 'stand'
            return 'hit'
        if player_val >= 17:
            return 'stand'


print(basic_strategy(13, 7, False))
