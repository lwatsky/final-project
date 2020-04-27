import json
import os
import requests
import sqlite3

API_KEY = "AIzaSyBrOMEPtu55GW6CTLVA5M6DLcW395dLds0"

city = input("Please enter the city you would like to add data for: ")
city = str(city)
search = "" 
if city == "Ann Arbor":
    search = "restaurants+in+Ann+Arbor"
if city == "Gainesville":
    search = "restaurants+in+Gainesville"
if city == "Austin":
    search = "restaurants+in+Austin"
if city == "Bloomington":
    search = "restaurants+in+Bloomington"
if city == "Madison":
    search = "restaurants+in+Madison"

dir_path = os.path.dirname(os.path.realpath(__file__))
filepath = dir_path + '/' + "google.json"





def pull_data(API_KEY, search):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&location=42.2808,83.7430&type=restaurant&key={}".format(search, API_KEY)
    request = requests.get(base_url)
    response = json.loads(request.text)
   
    total = []

    for items in response['results']:
        if items['id'] not in total:
            total.append((items['rating'], items['id'], items['name']))
    total = sorted(total, key = lambda x: x[0], reverse = True)

    return total


def name(city):
    lst = pull_data(API_KEY, search)
    name = []
    for items in lst:
        name.append(items[2])
    print(name)
    return name

def rest_id(city):
    lst = pull_data(API_KEY, search)
    ids = []
    for items in lst:
        ids.append(items[1])
    return ids

def rating(city):
    lst = pull_data(API_KEY, search)
    rates = []
    for items in lst:
        rates.append(items[0])
    return rates

def convert(city):
    namelst = name(city)
    int_lst = []
    for city1 in range(len(namelst)):
        if city == "Ann Arbor":
            int_lst.append(1)
        if city == "Gainesville":
            int_lst.append(2)
        if city == "Austin":
            int_lst.append(3)
        if city == "Bloomington":
            int_lst.append(4)
        if city == "Madison":
            int_lst.append(5)
        
    return int_lst



def start_db():
    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS GoogleData (restaurant_name TEXT, restaurant_id INTEGER, restaurant_rating FLOAT, city_id INTEGER)")
        print("table created")
    except:
        print("table not create")

def write_db(rest_data, rest_id, rest_rate, city_id):

    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        
        for i in range(20):
            _rest_name = rest_data[i]
            _rest_id = rest_id[i]
            _rest_rate = rest_rate[i]
            _city_id = city_id[i]
            cur.execute("INSERT INTO GoogleData (restaurant_name, restaurant_id, restaurant_rating, city_id) VALUES (?, ?, ?, ?)", (_rest_name, _rest_id, _rest_rate, _city_id))
            conn.commit()
        print('successfully added')
        cur.close()
    except:
        print("ERROR")


if city == "Ann Arbor":
    start_db()
write_db(name(city), rest_id(city), rating(city), convert(city))






