"""
Course: CSE 251 
Lesson: L05 Team Activity
File:   team.py
Author: <Add your name here>

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools.
- Follow the graph from the `../canvas/teams.md` instructions.
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it.
"""

import time
import threading
import multiprocessing as mp
import random
from os.path import exists

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# TODO create read_thread function
def reader():
    num_queue = []
    with open("data.txt", "r") as file:
        for line in file:
            words = line.strip().split()
            for word in words:
                num_queue.append(int(word))
                
                return num_queue



# TODO create prime_process function
def primer(num_queue):
    primes = []
    while num_queue:
        num = num_queue.pop(0)
        if is_prime(num):
            primes.append(num)
        
        return primes

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    # Create the data file for this demo if it does not already exist.
    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    num_queue = mp.Queue()
    primes = mp.Queue()

    # TODO create reading thread
    t = threading.Thread(target=reader, args=(num_queue, primer,))

    # TODO create prime processes
    processes = []
    for p in range(PRIME_PROCESS_COUNT):
        p - mp.Process(target=primer, args=(num_queue, primes))
        primes.append(p)

    # TODO Start them all
    for threads in 

    # TODO wait for them to complete

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()
