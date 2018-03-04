weights = {
    'Bronze': 1,
    'Silver': 1.25,
    'Gold': 1.5,
    'Diamond': 2,
    'Platinum': 2.5,
    'Master': 3,
    'EliteMaster': 3.5,
    'GrandMaster': 4,
    'Sponsor': 5,
    '@everyone': 0.5
}


def get_vote_weight(role_name: str):
    print(role_name)
    if role_name in weights:
        print('Voted with ' + str(weights[role_name]))
        return weights[role_name]
    return 5
