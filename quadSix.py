from random import randint
from datetime import datetime
'''
    This script will emulate 4 di rolls to see how many rolls it takes to hit 4 sixes.
    It takes the average of multiple test and spits it out at end along with min and max roll count
    change the amount of test by adjusting the 'MAX_ROLL_COUNT' variable (currently 100000 test are ran)
'''
def runTest():
    quad_six_found = False
    roll_attempts = 0
    while quad_six_found != True :
        roll_attempts += 1
        di1 = randint(1,6)
        di2 = randint(1,6)
        di3 = randint(1,6)
        di4 = randint(1,6)
        #print("di_1: " + str(di1) + " di_2: " + str(di2) + " di_3: " + str(di3) + " di_4: " + str(di4) )
        if di1 == 6 and di2 == 6 and di3 == 6 and di4 == 6 :
            print("Quad 6 found after " + str(roll_attempts) + " attempted rolls!!!!")
            quad_six_found = True
        else:
            quad_six_found = False
    return roll_attempts
    
'''
        MAIN
'''
tstart = datetime.now()
MAX_ROLL_COUNT = 100000
roll_attempts_count = []
test_count = 0
while test_count < MAX_ROLL_COUNT :
    test_count += 1
    print("test # " + str(test_count) + " is starting")
    attempts = runTest()
    roll_attempts_count.append( attempts )
#print(str(roll_attempts_count))
avg = reduce(lambda x, y: x + y, roll_attempts_count) / len(roll_attempts_count)
print("******************************************************************************")
print("Average attempts made :: " + str(avg))
print("Minimum roll attempts :: " + str(min(roll_attempts_count)))
print("Maximum roll attempts :: " + str(max(roll_attempts_count)))
print("******************************************************************************")
tend = datetime.now()
print("time diff " + str(tend-tstart))