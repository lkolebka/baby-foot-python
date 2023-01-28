import random 

def calculate_elo(old_rating, opponent_rating, outcome):
    K = 32  # The constant that determines the impact of the match on the rating
    expected_outcome = 1 / (1 + 10 ** ((opponent_rating - old_rating) / 400))
    return old_rating + K * (outcome - expected_outcome)


def test_calculate_elo():
    old_rating = random.randint(1000,3000)
    opponent_rating = random.randint(1000,3000)
    outcome = random.choice([0,0.5,1])
    new_rating = calculate_elo(old_rating, opponent_rating, outcome)
    print("Old Rating:",old_rating)
    print("Opponent Rating:",opponent_rating)
    print("Outcome:",outcome)
    print("New Rating:",new_rating)
test_calculate_elo()
