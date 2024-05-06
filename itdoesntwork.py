import requests
import json

# Const Values
TOP_API_URL = r'http://127.0.0.1:8790'

if __name__ == '__main__':

    response = requests.get(TOP_API_URL)
    
    # Check the status code to see if the request succeeded.
    if response.status_code == 200:
        data = response.json()
        print(data)

		# Example to get person 1 url
        print('\nHere is the URL for person id = 1:', f'{data["people"]}1')
    else:
        print('Error in requesting ID')