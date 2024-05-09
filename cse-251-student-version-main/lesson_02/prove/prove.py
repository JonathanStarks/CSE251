"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)

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