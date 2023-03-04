import math
a = 1500 
b = 1600

teamAB = a + b
print('teamAB =', teamAB)

newrating = 1 + (a - teamAB)/1000
print('newrating =', newrating)

score_difference = abs(9-11)
print('score_difference =', score_difference)


calculate_point_factor =  1 + (math.log(score_difference + 1) / math.log((10)))
print("calculate_point_factor = ", calculate_point_factor)

calculate_point_factor2 = (score_difference + 15) ** 2 / 225
print("calculate_point_factor2 = ", calculate_point_factor2)
 

a = 1200 + 49.93757802746567 * 1.7153382790366967 * (0.8461538461538461 - 0.5)
print(a)

player3_rating = 1952
player1_rating = 2100
player1_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player1_rating) / 500))

print(player1_expected_score_against_player3)