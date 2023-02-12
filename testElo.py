import math

# calculate the factor of the differnce of the point 
def calculate_point_factor(score_difference):
    return 1 + (math.log(score_difference + 1) / math.log(50))


def calculate_elo(old_rating, opponent_rating, outcome, score_difference, number_of_games):
    K = 50 / (1 + number_of_games / 800)  # The constant that determines the impact of the match on the rating
    expected_outcome = 1 / (1 + 10 ** ((opponent_rating - old_rating) / 400))
    point_factor = calculate_point_factor(score_difference)
    return old_rating + (K) * point_factor * (outcome - expected_outcome)

def test_calculate_elo():
    # Test 1
    old_rating = 1500
    opponent_rating = 1600
    outcome = 1
    score_difference = 4
    number_of_games = 100
    expected_new_rating = 1542.26
    new_rating = calculate_elo(old_rating, opponent_rating, outcome, score_difference, number_of_games)
    assert abs(new_rating - expected_new_rating) < 0.01, f"Expected {expected_new_rating} but got {new_rating}"

    # Test 2
    old_rating = 1600
    opponent_rating = 1500
    outcome = 0
    score_difference = 4
    number_of_games = 100
    expected_new_rating = 1557.74
    new_rating = calculate_elo(old_rating, opponent_rating, outcome, score_difference, number_of_games)
    assert abs(new_rating - expected_new_rating) < 0.01, f"Expected {expected_new_rating} but got {new_rating}"

    # Test 3
    old_rating = 1500
    opponent_rating = 1600
    outcome = 0.5
    score_difference = 4
    number_of_games = 100
    expected_new_rating = 1525
    new_rating = calculate_elo(old_rating, opponent_rating, outcome, score_difference, number_of_games)
    assert abs(new_rating - expected_new_rating) < 0.01, f"Expected {expected_new_rating} but got {new_rating}"

test_calculate_elo()
