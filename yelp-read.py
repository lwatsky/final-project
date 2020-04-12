import json
import os
import requests
import sqlite3

API_KEY = "gZabPb4Kf3x9h9N4mJNZqg1YnMVx_Idy5ST8BS4BiWHUhH0fD8xWbs1THaY_JIabtN9L5QVTNY_1T4BHAnmquGOi7dNwZgRIe6WY_mpDZtYn3yt-BbNAPQqMKvuMXnYx"

dir_path = os.path.dirname(os.path.realpath(__file__))
filepath = dir_path + '/' + "yelp.json"

def write_json(API_KEY):
    open_file = open(filepath, 'w')

    base_url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization" : "Bearer %s" % API_KEY}
    params = {'term': "restaurants", 'location': 'Detroit', "sort_by": "rating"}
    request = requests.get(base_url, headers = headers, params = params)
    response = json.loads(request.text)

    open_file.write(json.dumps(response))
    open_file.close()


write_json(API_KEY)



def pull_data(API_KEY):
    offset = 0
    rating_lst = []
    rates = []
    while offset < 101:
    
        base_url = "https://api.yelp.com/v3/businesses/search"
        headers = {"Authorization" : "Bearer %s" % API_KEY}
        params = {'term': "restaurants", 'location': 'Detroit', "sort_by": "rating", "limit": 50, "offset": offset}
        request = requests.get(base_url, headers = headers, params = params)
        response = json.loads(request.text)

        for item in response['businesses']:
    
            if item['id'] not in rating_lst:
                rating_lst.append((item['rating'], item['id'], item['name']))
                rates.append(float(item['rating']))
        offset += 51
    rating_lst = sorted(rating_lst, key = lambda x: x[0], reverse = True)
   # print(len(rates))
   # print(rates)
    return rating_lst

def name(pull_data):
    lst = pull_data(API_KEY)
    name = []
    for items in lst:
        name.append(items[2])
   # print(name)
  #  print(len(name))
    return name

name(pull_data)

def rating(pull_data):
    lst = pull_data(API_KEY)
    rates = []
    for items in lst:
        rates.append(items[0])
    #print(rates)
   # print(len(rates))
    return rates

rating(pull_data)

def rest_id(pull_data):
    lst = pull_data(API_KEY)
    id = []
    for items in lst:
        id.append(items[1])
  #  print(id)
   # print(len(id))
    return id

rest_id(pull_data)


write_json(API_KEY)

def start_db():
    conn = sqlite3.connect('/Users/laurenwatsky/Documents/final-project/final-database.db')
    cur = conn.cursor()
       # cur.execute("DROP TABLE IF EXISTS zomato_data")
       # cur.execute("DROP TABLE IF EXISTS zomato")
    cur.execute("DROP TABLE IF EXISTS YelpData")
    cur.execute("CREATE TABLE IF NOT EXISTS YelpData (restaurant_name TEXT, restaurant_id INTEGER, restaurant_rating FLOAT)")

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
            cur.execute("INSERT INTO YelpData (restaurant_name, restaurant_id, restaurant_rating) VALUES (?, ?, ?)", (_rest_name, _rest_id, _rest_rate))
            conn.commit()
        print('successfully added')
        cur.close()
    except:
        print("ERROR")

start_db()
write_db(name(pull_data)[0:20], rest_id(pull_data)[0:20], rating(pull_data)[0:20])
write_db(name(pull_data)[20:40], rest_id(pull_data)[20:40], rating(pull_data)[20:40])
write_db(name(pull_data)[40:60], rest_id(pull_data)[40:60], rating(pull_data)[40:60])
write_db(name(pull_data)[60:80], rest_id(pull_data)[60:80], rating(pull_data)[60:80])
write_db(name(pull_data)[80:], rest_id(pull_data)[80:], rating(pull_data)[80:])

