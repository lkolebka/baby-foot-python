import math
a = 1500 
b = 1600

teamAB = a + b
print('teamAB =', teamAB)

newrating = 1 + (a - teamAB)/1000
print('newrating =', newrating)

score_difference = abs(1-11)
print('score_difference =', score_difference)


calculate_point_factor =  1 + (math.log(score_difference + 1) / math.log((3)))
print("calculate_point_factor = ", calculate_point_factor)