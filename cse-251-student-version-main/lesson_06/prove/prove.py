"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: <Add name here>

Purpose: Processing Plant

Instructions:

- Implement the necessary classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME   = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'

class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = (
        'Gold',
        'Orange Peel',
        'Purple Plum',
        'Blue',
        'Neon Silver', 
        'Tuscan Brown', 
        'La Salle Green', 
        'Spanish Orange', 
        'Pale Goldenrod', 
        'Orange Soda', 
        'Maximum Purple', 
        'Neon Pink', 
        'Light Orchid', 
        'Russian Violet', 
        'Sheen Green', 
        'Isabelline', 
        'Ruby', 
        'Emerald', 
        'Middle Red Purple', 
        'Royal Orange', 
        'Dark Fuchsia', 
        'Slate Blue', 
        'Neon Dark Green', 
        'Sage', 
        'Pale Taupe', 
        'Silver Pink', 
        'Stop Red', 
        'Eerie Black', 
        'Indigo', 
        'Ivory', 
        'Granny Smith Apple', 
        'Maximum Blue', 
        'Pale Cerulean', 
        'Vegas Gold', 
        'Mulberry', 
        'Mango Tango', 
        'Fiery Rose', 
        'Mode Beige', 
        'Platinum', 
        'Lilac Luster', 
        'Duke Blue', 
        'Candy Pink', 
        'Maximum Violet', 
        'Spanish Carmine', 
        'Antique Brass', 
        'Pale Plum', 
        'Dark Moss Green', 
        'Mint Cream', 
        'Shandy', 
        'Cotton Candy', 
        'Beaver', 
        'Rose Quartz', 
        'Purple', 
        'Almond', 
        'Zomp', 
        'Middle Green Yellow', 
        'Auburn', 
        'Chinese Red', 
        'Cobalt Blue', 
        'Lumber', 
        'Honeydew', 
        'Icterine', 
        'Golden Yellow', 
        'Silver Chalice', 
        'Lavender Blue', 
        'Outrageous Orange', 
        'Spanish Pink', 
        'Liver Chestnut', 
        'Mimi Pink', 
        'Royal Red', 
        'Arylide Yellow', 
        'Rose Dust', 
        'Terra Cotta', 
        'Lemon Lime', 
        'Bistre Brown', 
        'Venetian Red', 
        'Brink Pink', 
        'Russian Green', 
        'Blue Bell', 
        'Green', 
        'Black Coral', 
        'Thulian Pink', 
        'Safety Yellow', 
        'White Smoke', 
        'Pastel Gray', 
        'Orange Soda', 
        'Lavender Purple',
        'Brown', 
        'Gold', 
        'Blue-Green', 
        'Antique Bronze', 
        'Mint Green', 
        'Royal Blue', 
        'Light Orange', 
        'Pastel Blue', 
        'Middle Green')

    def __init__(self, creator):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.creator = creator

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        # print("Made it to the run of the creator")
        for i in range(1000): #MARBLE_COUNT
            data = Marble_Creator.colors[random.randint(0, len(Marble_Creator.colors) - 1)]
            self.creator.send(data)
            time.sleep(0.01) #CREATOR_DELAY
        self.creator.send(None)


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, bagger_r, bagger_s):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.bagger_r = bagger_r
        self.bagger_s = bagger_s

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        # print("Made it to the run of the bagger")
        marble_bag = []
        while True:
            time.sleep(0.01) #BAGGER_DELAY
            data = self.bagger_r.recv()
            marble_bag.append(data)
            if len(marble_bag) == 7:
                self.bagger_s.send(marble_bag)
                # print(marble_bag)
                marble_bag = []
            if data is None:
                self.bagger_s.send(None)
                return
        # while len(marble_bag) < 7: #NUMBER_OF_MARBLES_IN_A_BAG
        #     data = self.bagger_r.recv()
        #     marble_bag.append(data)
            
        #
        #
        #print(f"sent marble bag")
        #


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, assembler_r, assembler_s):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.assembler_r = assembler_r
        self.assembler_s = assembler_s

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        # print("Made it to the run of the assembler")
        full_marble_bag = []
        while True:
            marble_bag = self.assembler_r.recv()
            if marble_bag is None:
                self.assembler_s.send(None)
                return
            for marble in marble_bag:
                full_marble_bag.append(marble)
            full_marble_bag.append(", Big Marble: " + Assembler.marble_names[random.randint(0, len(Assembler.marble_names) - 1)])
            self.assembler_s.send(full_marble_bag)
            time.sleep(0.05) #ASSEMBLER_DELAY
        # while len(full_marble_bag) < 8:
        #     
        #     print(f"marble_bag got {marble_bag}")
        #     
        #         
        #     
        #     print(full_marble_bag)
        #     
        # 
        # print(full_marble_bag)


class Wrapper(mp.Process):
    """ Takes created gifts and "wraps" them by placing them in the boxes file. """
    def __init__(self, wrapper):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.wrapper = wrapper

        

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(BOXES_FILENAME, "a") as file:
            while True:
                bag_to_box = self.wrapper.recv()
                # print(bag_to_box)
                if bag_to_box is None:
                    return
                file.write(f"Created:{datetime.now()} {bag_to_box}\n")
                time.sleep(0.05) #WRAPPER_DELAY

                    
            
            



def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator, bagger_r = mp.Pipe()
    bagger_s, assembler_r = mp.Pipe()
    assembler_s, wrapper = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    
    
    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')
    # TODO Create the processes (ie., classes above)
    mrbl_crtr = Marble_Creator(creator)
    mrbl_bggr = Bagger(bagger_r, bagger_s)
    gift_assmblr = Assembler(assembler_r, assembler_s)
    gift_wrpr = Wrapper(wrapper)


    log.write('Starting the processes')
    # TODO add code here
    mrbl_crtr.start()
    mrbl_bggr.start()
    gift_assmblr.start()
    gift_wrpr.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    mrbl_crtr.join()
    mrbl_bggr.join()
    gift_assmblr.join()
    gift_wrpr.join()
    print("All done")

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.

    log.stop_timer(f'Total time')




if __name__ == '__main__':
    main()
