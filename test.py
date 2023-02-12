import math
K = 50 / (1 + 0 / 800)
print('k is ',K)

opponent_rating = 1800
old_rating = 1700
expected_outcome = 1 / (1 + 10 ** ((opponent_rating - old_rating) / 400))
print('expected_outcome is ',expected_outcome)

score_difference = 10
def calculate_point_factor(score_difference):
    return 1 + (math.log(score_difference + 1) / math.log(50))

print('calculate_point_factor is ',calculate_point_factor(score_difference))


def calculate_elo(old_rating, opponent_rating, outcome, score_difference, number_of_games):
    K = 50 / (1 + number_of_games / 800)  # The constant that determines the impact of the match on the rating
    expected_outcome = 1 / (1 + 10 ** ((opponent_rating - old_rating) / 400))
    point_factor = calculate_point_factor(score_difference)
    return old_rating + (K) * point_factor * (outcome - expected_outcome)

     # Calculate the new ratings for the player1
    player1_rating_vs_player3 = calculate_elo(player1_rating, player3_rating, player1_outcome, score_difference_player1, number_of_game_player1)
    player1_rating_vs_player4 = calculate_elo(player1_rating, player4_rating, player1_outcome, score_difference_player1, number_of_game_player1)
    player1_new_rating = (player1_rating_vs_player3 + player1_rating_vs_player4) 

    # Calculate the new ratings for the player2
    player2_rating_vs_player3 = calculate_elo(player2_rating, player3_rating, player2_outcome, score_difference_player2, number_of_game_player2)
    player2_rating_vs_player4 = calculate_elo(player2_rating, player4_rating, player2_outcome, score_difference_player2, number_of_game_player2)
    player2_new_rating = (player2_rating_vs_player3 + player2_rating_vs_player4) 

    # Calculate the new ratings for the player3
    player3_rating_vs_player1 = calculate_elo(player3_rating, player1_rating, player3_outcome, score_difference_player3, number_of_game_player3)
    player3_rating_vs_player2 = calculate_elo(player3_rating, player2_rating, player3_outcome, score_difference_player3, number_of_game_player3)
    player3_new_rating = (player3_rating_vs_player1 + player3_rating_vs_player2) 

    # Calculate the new ratings for the player4
    player4_rating_vs_player1 = calculate_elo(player3_rating, player1_rating, player3_outcome, score_difference_player3, number_of_game_player3)
    player4_rating_vs_player2 = calculate_elo(player3_rating, player2_rating, player3_outcome, score_difference_player3, number_of_game_player3)
    player4_new_rating = (player4_rating_vs_player1 + player4_rating_vs_player2) 