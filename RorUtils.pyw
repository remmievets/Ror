import random

def Roll1d6():
###########################################################################
# @brief Roll 1 six sided dice
#
# @return die 1 result
###########################################################################
    return random.randint(1,6)
        
def Roll2d6():
###########################################################################
# @brief Roll 2 six sided dice
#
# @return total, die 1 result, die 2 result
###########################################################################
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    total = die1 + die2
    return total, die1, die2

def Roll3d6():
###########################################################################
# @brief Roll 3 six sided dice
#
# @return total, die 1 result, die 2 result, die 3 result
###########################################################################
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    die3 = random.randint(1,6)
    total = die1 + die2 + die3
    return total, die1, die2, die3
