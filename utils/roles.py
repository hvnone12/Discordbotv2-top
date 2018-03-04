def get_role(number: int):
    invites_keys = roles.keys()
    invites_keys = sorted(invites_keys, reverse=True)
    for invites_needed in invites_keys:
        if number >= invites_needed:
            return roles[invites_needed]
    return None


def get_next_role(number: int):
    invites_keys = roles.keys()
    invites_keys = sorted(invites_keys)
    for invites_needed in invites_keys:
        if number < invites_needed:
            return roles[invites_needed], invites_needed
    return 'Rank 1', 100


def get_previous_role(number: int):
    invites_keys = roles.keys()
    invites_keys = sorted(invites_keys)
    previous = 0
    for invites_needed in invites_keys:
        if number < invites_needed:
            return roles[previous], previous
        previous = invites_needed


roles = {
    1: 'Rank 10',
    3: 'Rank 9',
    8: 'Rank 8',
    15: 'Rank 7',
    30: 'Rank 6',
    50: 'Rank 5',
    75: 'Rank 4',
    100: 'Rank 3',
    150: 'Rank 2',
    200: 'Rank 1',
}
