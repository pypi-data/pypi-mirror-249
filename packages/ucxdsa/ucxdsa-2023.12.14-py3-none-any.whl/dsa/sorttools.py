import random

def rand_int_array(n, maxnum):
    ''' return an array of n integers of random numbers from 0 to maxnum '''
    array = [None] * n
    for i in range(n):
        array[i] = random.randint(0, maxnum)
    return array

def filled_array(n):
    ''' return an array of n integers from 0 to n '''
    array = [None] * n
    for i in range(n):
        array[i] = i
    return array    

def shuffle_array(n):
    ''' return a shuffled array of n integers from 0 to n '''
    array = filled_array(n)
    for i in range(n):
        r = random.randint(i, n-1)
        array[i], array[r] = array[r], array[i]
    return array

