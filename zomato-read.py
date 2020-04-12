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

def rating(API_KEY):
    start = 0
    rating_lst = []
    rates = []
    while start < 100:
    
        base_url = "https://developers.zomato.com/api/v2.1/search?"
        headers = {'Accept': 'application/json', 'user-key': API_KEY}
        params = {'entity_id': 280, 'entity_type': 'city', 'start': start, 'count' :20, 'sort': 'rating', 'order' : 'desc'}
        request = requests.get(base_url, headers = headers, params = params)
        response = json.loads(request.text)

        for item in response['restaurants']:
    
            if item['restaurant']['id'] not in rating_lst:
                rating_lst.append((item['restaurant']['user_rating']['aggregate_rating'], item['restaurant']['id']))
                rates.append(float(item['restaurant']['user_rating']['aggregate_rating']))
        start += 20
    #print(len(rates))
    #print(rates)
    return rates

rating(API_KEY)


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

def start_db():
    conn = sqlite3.connect('/Users/laurenwatsky/Documents/final-project/final-database.db')
    cur = conn.cursor()
       # cur.execute("DROP TABLE IF EXISTS zomato_data")
       # cur.execute("DROP TABLE IF EXISTS zomato")
    cur.execute("DROP TABLE IF EXISTS ZomatoData")
    cur.execute("CREATE TABLE IF NOT EXISTS ZomatoData (restaurant_name TEXT, restaurant_id INTEGER, restaurant_rating FLOAT)")

def write_db(rest_data, rest_id, rest_rate):

    try:
        conn = sqlite3.connect('/Users/laurenwatsky/Documents/final-project/final-database.db')
        cur = conn.cursor()
       # cur.execute("DROP TABLE IF EXISTS zomato_data")
       # cur.execute("DROP TABLE IF EXISTS zomato")
       # cur.execute("DROP TABLE IF EXISTS ZomatoData")
       # cur.execute("CREATE TABLE IF NOT EXISTS ZomatoData1 (restaurant_name TEXT, restaurant_id INTEGER)")
        
        for i in range(20):
            _rest_name = rest_data[i]
            _rest_id = rest_id[i]
            _rest_rate = rest_rate[i]
            cur.execute("INSERT INTO ZomatoData (restaurant_name, restaurant_id, restaurant_rating) VALUES (?, ?, ?)", (_rest_name, _rest_id, _rest_rate))
            conn.commit()
        print('successfully added')
        cur.close()
    except:
        print("ERROR")

start_db()
write_db(restaurant_name(API_KEY)[0:20], restaurant_id(API_KEY)[0:20], rating(API_KEY)[0:20])
write_db(restaurant_name(API_KEY)[20:40], restaurant_id(API_KEY)[20:40], rating(API_KEY)[20:40])
write_db(restaurant_name(API_KEY)[40:60], restaurant_id(API_KEY)[40:60], rating(API_KEY)[40:60])
write_db(restaurant_name(API_KEY)[60:80], restaurant_id(API_KEY)[60:80], rating(API_KEY)[60:80])
write_db(restaurant_name(API_KEY)[80:100], restaurant_id(API_KEY)[80:100], rating(API_KEY)[80:100])









