import random 

def calculate_elo(old_rating, opponent_rating, outcome):
    K = 32  # The constant that determines the impact of the match on the rating
    expected_outcome = 1 / (1 + 10 ** ((opponent_rating - old_rating) / 400))
    return old_rating + K * (outcome - expected_outcome)


def test_calculate_elo():
    old_rating = random.randint(1200,1400)
    opponent_rating = random.randint(1000,3000)
    outcome = random.choice([0,1])
    new_rating = calculate_elo(old_rating, opponent_rating, outcome)
    print("Old Rating:",old_rating)
    print("Opponent Rating:",opponent_rating)
    print("Outcome:",outcome)
    print("New Rating:",new_rating)
test_calculate_elo()

def test_calculate_elo2():
    old_rating = 1210
    opponent_rating = 1200
    outcome = random.choice([0,1])
    new_rating = calculate_elo(old_rating, opponent_rating, outcome)
    print("V2_Old Rating:",old_rating)
    print("V2_Opponent Rating:",opponent_rating)
    print("V2_Outcome:",outcome)
    print("V2_New Rating:",new_rating)
test_calculate_elo2()