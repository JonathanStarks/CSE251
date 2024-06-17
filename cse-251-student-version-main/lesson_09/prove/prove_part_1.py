"""
Course: CSE 251 
Lesson: L09 Prove Part 1
File:   prove_part_1.py
Author: <Add name here>

Purpose: Part 1 of prove 9, finding the path to the end of a maze using recursion.

Instructions:

- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Complete any TODO comments.
"""

from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 files
from cse251 import *
import random

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
SLOW_SPEED = 100
FAST_SPEED = 1
speed = SLOW_SPEED

# TODO: Add any functions needed here.

def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
    path = []

    def solve(x, y): #returns true if at the end else flase and keeps going
        if maze.at_end(x, y):
            return True
        
        movement = maze.get_possible_moves(x, y)
        
        for move in movement:
            new_x, new_y = move
            if (maze.can_move_here(new_x, new_y)): #movement[len(movement) - 1][0], movement[len(movement) - 1][1])#)):
                # path.append(maze.get_possible_moves(movement[len(movement) - 1][0], movement[len(movement) - 1][1])[random.randint(0, len(movement))])
                maze.move(new_x, new_y, COLOR)#x, y, COLOR)
                # print(path)
                path.append((new_x, new_y))
                #movement[len(movement) - 1][0], movement[len(movement) - 1][1])
                
                if solve(new_x, new_y):
                    return True
            
                # print("got here")
                path.pop()
                maze.restore(x, y)
                # solve(movement[len(movement) - 1][0], movement[len(movement) - 1][1])
        return False

    start_pos = maze.get_start_pos()
    # print(start_pos)
    path.append(start_pos)
    solve(start_pos[0], start_pos[1])
    return path
    
    ''' above is the code that I tried to get to work over the course of 8 hours, and below is the code that chat gpt said would work. '''


    # def solve(x, y):
    #     if maze.at_end(x, y):  # Check if current position is the end
    #         return True

    #     movement = maze.get_possible_moves(x, y)  # Get possible moves from current position

    #     for move in movement:
    #         new_x, new_y = move
    #         if maze.can_move_here(new_x, new_y):  # Check if we can move to the new position
    #             maze.move(new_x, new_y, COLOR)  # Move to the new position
    #             path.append((new_x, new_y))  # Add the new position to the path

    #             if solve(new_x, new_y):  # Recursively solve from the new position
    #                 return True

    #             # Backtrack
    #             path.pop()  # Remove the new position from the path
    #             maze.restore(x, y)  # Restore the move

    #     return False

    # start_pos = maze.get_start_pos()  # Get starting position
    # path.append(start_pos)  # Initialize path with the starting position

    # if solve(start_pos[0], start_pos[1]):  # Start solving the maze from the starting position
    #     print("Path to the end found:", path)
    # else:
    #     print("No path to the end exists.")

    # return path

    


def get_path(log, filename):
    """ Do not change this function """
    # 'Maze: Press "q" to quit, "1" slow drawing, "2" faster drawing, "p" to play again'
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Drawing commands to solve = {screen.get_command_count()}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True

    return path


def find_paths(log):
    """ Do not change this function """

    files = (
        'very-small.bmp',
        'very-small-loops.bmp',
        'small.bmp',
        'small-loops.bmp',
        'small-odd.bmp',
        'small-open.bmp',
        'large.bmp',
        'large-loops.bmp',
        # 'large-squares.bmp',
        # 'large-open.bmp'
    )

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        filename = f'./mazes/{filename}'
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length     = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()