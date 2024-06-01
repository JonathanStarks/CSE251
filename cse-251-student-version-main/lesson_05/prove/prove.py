"""
Course: CSE 251 
Lesson: L05 Prove
File:   prove.py
Author: <Add name here>

Purpose: Assignment 05 - Factories and Dealers
// I could create a car and then see if theres room in the queue, or I could... the thought was never finished.

questions: 
1) How do I signal the dealerships? What does that mean?
2) How do I send a car to the dealership?
3) How do I make a barrier? What does a barrier do?
4) What info am I supposed to put into Factory_Stats
5) How do I tell the program that there are cars created?
6) How do I tell the program that there are cars sold?

Things I feel are helpful:
1) To create a process do this -> c = Car(arguments)
   then do c.start() and then c.join()
2) Run takes no arguments
3) Don't call Run() directly
4) 

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier!
- Do not use try...except statements.
- You are not allowed to use the normal Python Queue object. You must use Queue251.
- The shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE.
"""

from datetime import datetime, timedelta
import time
import threading
import random
# import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Global Constants.
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

# The Car class is the same, I don't need to do anything there.
class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'

# I am not supposed to change anything with the Queue251 class, but I'm not sure how I'm supposed to use it
class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.__items = []
        self.__max_size = 0

    def get_max_size(self):
        return self.__max_size

    def put(self, item):
        self.__items.append(item)
        if len(self.__items) > self.__max_size:
            self.__max_size = len(self.__items)

    def get(self):
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, empty_spots, filled_spots, barrierf):
        self.cars_to_produce = random.randint(200, 300) # DO NOT change
        # Below are the things that I changed in this method
        threading.Thread.__init__(self)
        self.car_queue = car_queue 
        self.empty_spots = empty_spots
        self.filled_spots = filled_spots
        self.barrierf = barrierf


    def run(self):
        for i in range(self.cars_to_produce):
            # TODO produce the cars, the send them to the dealerships
            data = Car()
            self.empty_spots.acquire()
            self.car_queue.put(data)
            self.filled_spots.release()

            # TODO wait until all of the factories are finished producing cars
        
        self.empty_spots.acquire()
        self.car_queue.put("Stop")
        self.filled_spots.release()
        self.barrierf.wait()
        # return car_count
            # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, dealer_stats, car_queue, empty_spots, filled_spots, barrierd):
        threading.Thread.__init__(self)
        self.dealer_stats = dealer_stats
        self.car_queue = car_queue
        self.empty_spots = empty_spots
        self.filled_spots = filled_spots
        self.barrierd = barrierd

    def run(self):
        while True:
            # TODO handle a car
            self.empty_spots.release()
            self.filled_spots.acquire()
            
            value = self.car_queue.get()
            if value == "Stop":
                self.barrierd.wait()
                break
            
            
            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))
            



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # TODO Create semaphore(s) if needed
    # TODO Create queue
    # TODO Create lock(s) if needed
    # TODO Create barrier
    empty_spots = threading.Semaphore(MAX_QUEUE_SIZE)
    filled_spots = threading.Semaphore(0)
    car_queue = Queue251()
    barrierf = threading.Barrier(factory_count)
    barrierd = threading.Barrier(dealer_count)
    # This is used to track the number of cars received by each dealer
    dealer_stats = list([0] * dealer_count)

    # TODO create your factories, each factory will create a random amount of cars; your code must account for this.
    
    # NOTE: You have no control over how many cars a factory will create in this assignment.

    # TODO create your dealerships
    factories = [Factory(car_queue, empty_spots, filled_spots, barrierf) for i in range(factory_count)]
    dealers = [Dealer(dealer_stats, car_queue, empty_spots, filled_spots, barrierd) for i in range(dealer_count)]

    log.start_timer()

    for dealer in dealers:
        dealer.start()

    for factory in factories:
        factory.start()

    for factory in factories:
        factory.join()

    for dealer in dealers:
        dealer.join()

    run_time = log.stop_timer(f'{len(dealer_stats)} cars have been created.')

    factory_stats = [factory.cars_to_produce for factory in factories]

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : Made = {sum(dealer_stats)} @ {factory_stats}')
        log.write(f'Dealer Stats   : Sold = {sum(factory_stats)} @ {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':
    log = Log(show_terminal=True)
    main(log)

