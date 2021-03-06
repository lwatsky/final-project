import json
import os
import requests
import sqlite3

API_KEY = "gZabPb4Kf3x9h9N4mJNZqg1YnMVx_Idy5ST8BS4BiWHUhH0fD8xWbs1THaY_JIabtN9L5QVTNY_1T4BHAnmquGOi7dNwZgRIe6WY_mpDZtYn3yt-BbNAPQqMKvuMXnYx"

dir_path = os.path.dirname(os.path.realpath(__file__))
filepath = dir_path + '/' + "yelp.json"

city = input("Please enter the city you would like to add data for: ")
city = str(city)



def pull_data(API_KEY, city):
    rating_lst = []
    rates = []
    
    base_url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization" : "Bearer %s" % API_KEY}
    params = {'term': "restaurants", 'location': city, "sort_by": "rating", "limit": 50}
    request = requests.get(base_url, headers = headers, params = params)
    response = json.loads(request.text)

    for item in response['businesses']:
    
        if item['id'] not in rating_lst:

            rating_lst.append((item['rating'], item['id'], item['name'], item["location"]['city']))
            rates.append(float(item['rating']))

    rating_lst = sorted(rating_lst, key = lambda x: x[0], reverse = True)[0:20]

    return rating_lst

def name():
    lst = pull_data(API_KEY, city)
    name = []
    for items in lst:
        name.append(items[2])

    return name


def rating():
    lst = pull_data(API_KEY, city)
    rates = []
    for items in lst:
        rates.append(items[0])

    return rates


def rest_id():
    lst = pull_data(API_KEY, city)
    id = []
    for items in lst:
        id.append(items[1])

    return id

def add_city():
    lst = pull_data(API_KEY, city)
    cities = []
    for items in lst:
        cities.append(items[3])
    return cities

def convert():
    city_lst = add_city()
    int_lst = []
    for city1 in city_lst:
        if city1 == "Ann Arbor":
            int_lst.append(1)
        if city1 == "Ypsilanti":
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
    conn = sqlite3.connect('final-database.db')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS YelpData")
    cur.execute("DROP TABLE IF EXISTS CityIdConversion")
    cur.execute("CREATE TABLE IF NOT EXISTS CityIdConversion (city_id INTEGER PRIMARY KEY, city_name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS YelpData (restaurant_name TEXT PRIMARY KEY, restaurant_id INTEGER, restaurant_rating FLOAT, city_id INTEGER, FOREIGN KEY(city_id) REFERENCES CityIdConversion(city_id))")

def write_db(rest_data, rest_id, rest_rate, city_id):

    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        
        for i in range(20):
            _rest_name = rest_data[i]
            _rest_id = rest_id[i]
            _rest_rate = rest_rate[i]
            _city_id = city_id[i]
            cur.execute("INSERT INTO YelpData (restaurant_name, restaurant_id, restaurant_rating, city_id) VALUES (?, ?, ?, ?)", (_rest_name, _rest_id, _rest_rate, _city_id))
            conn.commit()
        print('successfully added')
        cur.close()
    except:
        print("ERROR")

def new_table(city_id, city):
    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
    
        cur.execute("INSERT INTO CityIdConversion (city_id, city_name) VALUES (?, ?)", (city_id, city))
        conn.commit()
        print("new table successfully added")
        cur.close()
    except:
        print(city_id)
        print(city)
        print("ERROR")


if city == "Ann Arbor":
    start_db()
write_db(name(), rest_id(), rating(), convert())
new_table(convert()[0], city)


