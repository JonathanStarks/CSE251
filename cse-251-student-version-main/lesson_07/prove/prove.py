"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: <Add name here>

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

Note: each of the 5 task functions need to return a string.  They should not print anything.

TODO:
If I understand the purpose of the pool size it is to determine how many threads there can be for a pool, I found that around six 
for each pool was a good amount, any more than that and the saved time is negligable. I determined this by using brute force.

Add your comments here on the pool sizes that you used for your assignment and why they were the best choices.
"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from multiprocessing import Pool
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment

PRIME_POOL_SIZE = 6
WORD_POOL_SIZE  = 6
UPPER_POOL_SIZE = 6
SUM_POOL_SIZE   = 6
NAME_POOL_SIZE  = 6

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    # if value % 2 != 0 or value == 2:
    #     # print(value)
    #     return(f"{value} is prime")
    # else:
    #     return(f"{value} is not prime")
    if is_prime(value):
        return(f"{value} is prime")
    return(f"{value} is not prime")
    

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt", "r") as f:
        word = f.read()
    for lines in word:
        if word == lines:
            # print(word)
            return(f"{lines} found")
        else:
            return (f"{lines} not found")


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """

    # print(new_text)
    return (f"{text.upper()} ==> uppercase version of {text}")


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of all numbers between start_value and end_value
        answer = {start_value:,} to {end_value:,} = {total:,}
    """

    # i = 0
    # while (start_value + i) != end_value:
    #     total = start_value + (start_value + i)
    #     i += 1
    
    # result_sums.append(f"{start_value:,} to {end_value:,} = {total:,}")
    # print(total_msg)
    total = sum(range(start_value, end_value + 1))
    return (f"{start_value:,} to {end_value:,} = {total:,}")
        


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        name = response.json().get("name", "unknown")
    # if response.status_code == 200:
    
        return(f"{url} has name{response.json()['name']}.")
    # else:
    except Exception as e:
        return(f"{url} had an error.")


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool_prime = mp.Pool(PRIME_POOL_SIZE)
    pool_word = mp.Pool(WORD_POOL_SIZE)
    pool_upper = mp.Pool(UPPER_POOL_SIZE)
    pool_sum = mp.Pool(SUM_POOL_SIZE)
    pool_name = mp.Pool(NAME_POOL_SIZE)

    # TODO change the following if statements to start the pools
    def callback_prime(result):
        result_primes.append(result)
        
    def callback_word(result):
        result_words.append(result)

    def callback_upper(result):
        result_upper.append(result)

    def callback_sum(result):
        result_sums.append(result)

    def callback_name(result):
        result_names.append(result)
    
    count = 0
    task_files = glob.glob("tasks/*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        # print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            # task_prime(task['value'])
            pool_prime.apply_async(task_prime, args=(task['value'],), callback= callback_prime)
            # print(count)
        
        elif task_type == TYPE_WORD:
            # task_word(task['word'])
            pool_word.apply_async(task_word, args=(task['word'],), callback= callback_word)
            # print(count)
        elif task_type == TYPE_UPPER:
            # task_upper(task['text'])
            pool_upper.apply_async(task_upper, args=(task['text'],), callback= callback_upper)
            # print(count)
        elif task_type == TYPE_SUM:
            # task_sum(task['start'], task['end'])
            pool_sum.apply_async(task_sum, args=(task['start'], task['end'],), callback= callback_sum)            
            # print(count)
        elif task_type == TYPE_NAME:
            # task_name(task['url'])
            pool_name.apply_async(task_name, args=(task['url'],), callback=callback_name)
            # print(count)
        else:
            log.write(f'Error: unknown task type {task_type}')
            # print(count)

    # TODO wait on the pools
    pool_prime.close()
    pool_word.close()
    pool_upper.close()
    pool_sum.close()
    pool_name.close()
    
    pool_prime.join()
    pool_word.join()
    pool_upper.join()
    pool_sum.join()
    pool_name.join()
    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')


if __name__ == '__main__':
    main()