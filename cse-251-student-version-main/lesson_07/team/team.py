"""
Course: CSE 251 
Lesson: L07 Team
File:   team.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server.

Instructions:

1) Make a copy of your lesson 2 prove assignment. Since you are  working in a team for this
   assignment, you can decide which assignment 2 program that you will use for the team activity.

2) You can continue to use the Request_Thread() class that makes the call to the server.

3) Convert the program to use a process pool that uses apply_async() with callback function(s) to
   retrieve data from the Star Wars website. Each request for data must be a apply_async() call;
   this means 1 url = 1 apply_async call, 94 urls = 94 apply_async calls.
"""


from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_Thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        # threading.Thread.__init__(self)
        super().__init__()
        self.url = url
        self.response = {}
        self.status_code = {}
        self.data = {}

    def run(self):
        self.response = requests.get(self.url)
    
    # Check the status code to see if the request succeeded.
        if self.response.status_code == 200:
            self.data = self.response.json()
            
            

# TODO Add any functions you need here
def find_urls():
    req = Request_Thread(TOP_API_URL)
    req.start()
    req.join()
    
    data = req.data
    #print(data)    
    
    req = Request_Thread(f'{data["films"]}6')
    req.start()
    req.join()
    
    data = req.data
    #print_dict(data)
    def target_part(feild, content):
        print(f"{feild}:")
        print_dict(f"{data[content]}")

    threads = []
    targets = ["title", "episode_id", "opening_crawl", "director", "producer", "release_date", "characters", "planets", "starships", "vehicles", "species", "created", "edited", "url"
        ]
    for x in targets:
        tn = threading.Thread(target=target_part, args=(x, x))
        threads.append(tn)
        tn.start()

    for threads in threads:
        tn.join()

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    find_urls()
    # TODO Retrieve Details on film 6
    
    # TODO Display results

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()