player1_rating = 1000
player2_rating = 1200
player3_rating = 1500
player4_rating = 1300   


player1_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player1_rating) / 500))
player1_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player1_rating) / 500))
player1_expected_score = (player1_expected_score_against_player3 + player1_expected_score_against_player4) / 2
   
player2_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player2_rating) / 500))
player2_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player2_rating) / 500))
player2_expected_score = (player2_expected_score_against_player3 + player2_expected_score_against_player4) / 2
   

player3_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player3_rating) / 500))
player3_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player3_rating) / 500))
player3_expected_score = (player3_expected_score_against_player1 + player3_expected_score_against_player2) / 2
   

player4_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player4_rating) / 500))
player4_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player4_rating) / 500))
player4_expected_score = (player4_expected_score_against_player1 + player4_expected_score_against_player2) / 2     

print(f"Player 1 (John) expected score: {player1_expected_score:.6f}")
print(f"Player 2 (Jane) expected score: {player2_expected_score:.6f}")
print(f"Player 3 (Steve) expected score: {player3_expected_score:.6f}")
print(f"Player 4 (Sara) expected score: {player4_expected_score:.6f}")


team1_expected_score = (player1_expected_score + player2_expected_score) / 2
team2_expected_score = (player3_expected_score + player4_expected_score) / 2


print(f"Team  1 expected score: {team1_expected_score:.6f}")
print(f"Team 2 expected score: {team2_expected_score:.6f}")
