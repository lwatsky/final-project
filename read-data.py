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

#def zomato(API_KEY):
  #  start = 0
  #  restaurant_lst = []
  #  while start < 100:
    
   #     base_url = "https://developers.zomato.com/api/v2.1/search?"
   #     headers = {'Accept': 'application/json', 'user-key': API_KEY}
   #     params = {'entity_id': 280, 'entity_type': 'city', 'start': start, 'count' :20, 'sort': 'rating', 'order' : 'desc'}
    #    request = requests.get(base_url, headers = headers, params = params)
     #   response = json.loads(request.text)

     #   for item in response['restaurants']:
    
      #      if item['restaurant']['id'] not in restaurant_lst:
       #         restaurant_lst.append((item['restaurant']['name'], item['restaurant']['id']))
    #    start += 20

   # return restaurant_lst


def restaurant_name(API_KEY):
    start = 0
    rest_name = []
    names = []
    while start < 100:
    
        base_url = "https://developers.zomato.com/api/v2.1/search?"
        headers = {'Accept': 'application/json', 'user-key': API_KEY}
        params = {'entity_id': 280, 'entity_type': 'city', 'start': start, 'count' :20, 'sort': 'rating', 'order' : 'desc'}
        request = requests.get(base_url, headers = headers, params = params)
        response = json.loads(request.text)

        for item in response['restaurants']:
    
            if item['restaurant']['id'] not in rest_name:
                rest_name.append((item['restaurant']['name'], item['restaurant']['id']))
                names.append(item['restaurant']['name'])
        start += 20

    return names

def restaurant_id(API_KEY):
    start = 0
    rest_id = []
    while start < 100:
    
        base_url = "https://developers.zomato.com/api/v2.1/search?"
        headers = {'Accept': 'application/json', 'user-key': API_KEY}
        params = {'entity_id': 280, 'entity_type': 'city', 'start': start, 'count' :20, 'sort': 'rating', 'order' : 'desc'}
        request = requests.get(base_url, headers = headers, params = params)
        response = json.loads(request.text)

        for item in response['restaurants']:
    
            if item['restaurant']['id'] not in rest_id:
                rest_id.append(item['restaurant']['id'])
        start += 20

    return rest_id

def write_json(API_KEY):
    open_file = open(CACHE_FNAME, 'w')

    base_url = "https://developers.zomato.com/api/v2.1/search?"
    headers = {'Accept': 'application/json', 'user-key': API_KEY}
    params = {'entity_id': 280, 'entity_type': 'city'}
    request = requests.get(base_url, headers = headers, params = params)
    response = json.loads(request.text)

    open_file.write(json.dumps(response))
    open_file.close()


#print(zomato(API_KEY))
write_json(API_KEY)

def write_db(API_KEY):
    conn = sqlite3.connect('final-database.db')
    cur = conn.cursor()
    count = 0

    cur.execute("CREATE TABLE IF NOT EXISTS zomato-data (restaurant_name TEXT, restaurant_id INTEGER)")
    cur.execute("INSERT INTO zomato-data (restaurant_name, restaurant_id) VALUES (?, ?)", restaurant_name(API_KEY), restaurant_id(API_KEY))







