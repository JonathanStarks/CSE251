"""
Course: CSE 251 
Lesson: L06 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe
- Note, while getting your program to work, you can create a smaller text file instead of
  the ones given.  For example, create a text file with one line of text and get it to work
  with your program, then add another line of text and so on.
- After you can copy a text file word by word exactly, change the program (any way you want) to be
  faster (still using the processes).
"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(conn, filename): # Parent
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(filename, "rb") as file:
        done = False
        while not done:
            block = f

def receiver(conn, filename): # Child
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(filename, "rb") as done_file:
        while True:
            block = conn.recv()
            if block == EDN_MESSAGE:
                break
            sent_things


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    sender, receiver = mp.Pipe()
    # TODO create variable to count items sent over the pipe
    sent_things = 0

    # TODO create processes 
    pip1 = mp.Process(target=sender, args=(log,))
    pip2 = mp.Process(target=receiver, args=(log,))
    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    pip1.start()
    pip2.start()
    
    # TODO wait for processes to finish
    pip1.join()
    pip2.join()
    stop_time = log.get_time()

    log.stop_timer(f"Total time to transfer content = {stop_time - start_time}: ")
    #log.write(f'items / second = {PUT YOUR VARIABLE HERE / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')