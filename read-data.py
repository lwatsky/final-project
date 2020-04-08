#Final Project
#Lauren Watsky, Katie Wolberg, Jamie Zuckerman

#this file will be used to read the data from the APIs and stores the data in the database

#must limit to 20 items at a time added to the database for the first 100 rows stored

import json
import os
import requests
import sqlite3

API_KEY = "7ebe7ce4e9c950e0c5fbedd33d5379db"

dir_path = os.path.dirname(os.path.realpath(__file__))
CACHE_FNAME = dir_path + '/' + "zomato.json"

def zomato(API_KEY):
    base_url = "https://developers.zomato.com/api/v2.1/search?"
    headers = {'Accept': 'application/json', 'user-key': API_KEY}
    params = {'entity_id': 280, 'entity_type': 'city', 'start': 20, 'count' :20, 'sort': 'rating', 'order' : 'desc'}
    request = requests.get(base_url, headers = headers, params = params)
    response = json.loads(request.text)
    restaurant_lst = []

    for item in response['restaurants']:
        #print((item['restaurant']))
        #print(item['restaurant']['name'])
        if item['restaurant']['name'] not in restaurant_lst:
            restaurant_lst.append(item['restaurant']['name'])
    print(len(restaurant_lst))
    print(restaurant_lst)
           # print(rest)
          # print(rest)
           #for x in rest[2]:
             #  print(x)
               

    #print(response)
    #print(response)
    #for item in response: 
    #    print(item)
    return response

open_file = open(CACHE_FNAME, 'w')
open_file.write(json.dumps(zomato(API_KEY)))
open_file.close()


zomato(API_KEY)




