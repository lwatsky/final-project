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

city = input("Please enter the city you would like to add data for: ")
city = str(city)
entity_id = 0
entity_type = ""
if city == "Ann Arbor":
    entity_id = 118000
    entity_type = "subzone"
if city == "Gainesville":
    entity_id = 592
    entity_type = "city"
if city == "Austin":
    entity_id = 278
    entity_type = "city"
if city == "Bloomington":
    entity_id = 721
    entity_type = "city"
if city == "Madison":
    entity_id = 1264
    entity_type = "city"


def pull_data(API_KEY, entity_id, entity_type):
    total = []
    
    base_url = "https://developers.zomato.com/api/v2.1/search?"
    headers = {'Accept': 'application/json', 'user-key': API_KEY}
    params = {'entity_id': entity_id, 'entity_type': entity_type, 'start': 0, 'count' :20, 'sort': 'rating', 'order' : 'desc'}
    request = requests.get(base_url, headers = headers, params = params)
    response = json.loads(request.text)

    for item in response['restaurants']:
    
        if item['restaurant']['id'] not in total:
            total.append((item['restaurant']['name'], item['restaurant']['id'], float(item['restaurant']['user_rating']['aggregate_rating']), item['restaurant']["location"]['city']))
    total = sorted(total, key = lambda x: x[2], reverse = True)

    return total

def name(city):
    lst = pull_data(API_KEY, entity_id, entity_type)
    name = []
    for items in lst:
        name.append(items[0])
    return name


def rest_id(city):
    lst = pull_data(API_KEY, entity_id, entity_type)
    ids = []
    for items in lst:
        ids.append(items[1])
    return ids

def rating(city):
    lst = pull_data(API_KEY, entity_id, entity_type)
    rates = []
    for items in lst:
        rates.append(items[2])
    return rates


def add_city(city):
    lst = pull_data(API_KEY, entity_id, entity_type)
    cities = []
    for items in lst:
        cities.append(items[-1])

    return cities


def convert(city):
    city_lst = add_city(city)
    int_lst = []
    for city1 in city_lst:
        if city1 == "Ann Arbor":
            int_lst.append(1)
        if city1 == "Ypsilanti":
            int_lst.append(1)
        if city1 == "Detroit":
            int_lst.append(1)
        if city1 == "Gainesville":
            int_lst.append(2)
        if city1 == "Gainsville": #the city is spelled wrong when we pull the data from the API so we had to account for that
            int_lst.append(2)
        if city1 == "Austin":
            int_lst.append(3)
        if city1 == "Lakeway":
            int_lst.append(3)
        if city1 == "Pflugerville":
            int_lst.append(3)
        if city1 == "Bloomington":
            int_lst.append(4)
        if city1 == "Madison":
            int_lst.append(5)
        if city1 == "Sun Prairie":
            int_lst.append(5)
    return int_lst



def start_db():
    try:
        conn = sqlite3.connect('/Users/laurenwatsky/Documents/final-project/final-database.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ZomatoData (restaurant_name TEXT, restaurant_id INTEGER, restaurant_rating FLOAT, city_id INTEGER)")
        print("table created")
    except:
        print("table not created")

def write_db(rest_data, rest_id, rest_rate, city_id):

    try:
        conn = sqlite3.connect('/Users/laurenwatsky/Documents/final-project/final-database.db')
        cur = conn.cursor()
        
        for i in range(20):
            _rest_name = rest_data[i]
            _rest_id = rest_id[i]
            _rest_rate = rest_rate[i]
            _city_id = city_id[i]
            cur.execute("INSERT INTO ZomatoData (restaurant_name, restaurant_id, restaurant_rating, city_id) VALUES (?, ?, ?, ?)", (_rest_name, _rest_id, _rest_rate, _city_id))
            conn.commit()
        print('successfully added')
        cur.close()
    except:
        print("ERROR")

if city == "Ann Arbor":
    start_db()
write_db(name(city), rest_id(city), rating(city), convert(city))









