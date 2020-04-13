import json
import os
import requests
import sqlite3

API_KEY = "AIzaSyBrOMEPtu55GW6CTLVA5M6DLcW395dLds0"
pagetoken40 = "CsQCOwEAAHFA40UIEA1IwKmCNva5Xp7s_vMMLLayfHJ-8WeYplOyX6zRM5EjFnMLNblwsI6Vc_Bj8H82oDvR4qntM6K0NVMreJ0eQtzmS4YJoIL1nNr7zITCF-ob0U4KnfAkHWh_a7Trv6K95AKcdL6cDq3Vb2gSNHfH_F2zmJYy_VMYp8BJ66zOKj5YMV4-MxCh2eWE4QIsj-AWK7VxOq5EcBUAhqqRNeW-EZk0ijwyKn3uzeUZqFmD8BqLYU6vj1eLsWjhhMTPRKJgPncRYuVWQAfYnPhe1tnmQatc2eHvyDY1pZOi8ywL55hWKIq8F9Qq6mmK0jQaGaSlJO4jIRpYp2bMC4tRvbYPLQ0knePsSjtUPaLe2i9VvRy9AryXF8rawyX3iffy4QLQNT5k2WjN-tC2D3mFzABobq8IH9mtmUmnOWByEhCV1DggVIwErerOSKFEy-9nGhQ4oT39Bw9CWFmZhdtZpyZgQG6ckQ"
pagetoken60 = "CuQD2wEAACFeBo2-DG9vj7lXNhZIo7t_mCr9gBQsXE9SRbhRdXh1Q02-GuFLFswZDZy413Sr2DXcnQhAtqUQWU5txkzxJl0D6x7RTCd3UPX-jii3dxUaxBc27i4PODxVenlVI00S11CdcKPw_Io4D9MYJ8KKvip4PPW0BOD1baKiXJ90Wkd3iKZP05cH9390Z6j7QsjjBgPflkWR1RTzOOHlkDmTTnsRuEF8r1Q9mwteUbu3N6peA6GoNF2eQ6LtNrtBVlP9VMLNtXkmFBzh5P7NRvjO2dpKcuheSAAYJ-gkAXxA29wkn88Jh4mZqwwVZbo1iw2g5Nn7fOoKtyrYW1sBXXW-aFw4KUlbul4B7fR_Mgj05exwRlKfJn3TIScNmtY_M6QjEeY7mkqmQKIuEBYgQV6N3ZAbMGG54RQTmc-OeBZ8obDo7dkkRsjH56oAtTvSskxnV5SBhn_Xb2jJBIlEzaY3LTf8rfQJTQAwL5H0DR77_Nk9mDcsUchXMraesheVwE6nnRbaotc1VNAb7YIxtYQY0ohXb-pLULEDNE4zfAfvzhe5FILW7Fa14S2VA8PCXW-jkceIUBDRcvh3dst2eYw9pJC5rcF1dKzk5Es0qxEGPa6ZlkGDT_5hHoa6uPOlhhLHRxIQ0i8-DCC1Te4rIk1_ZeCIVxoUjJkW2z9SwDzy2zVB9I8U7jmb-0I"
search = "restaurants+in+Ann+Arbor"
search2 = "restaurants+in+Ypsilanti"
search3 = "restaurants+in+Plymouth"

dir_path = os.path.dirname(os.path.realpath(__file__))
filepath = dir_path + '/' + "google.json"


def write_json(API_KEY, nextpagetoken, search):
    open_file = open(filepath, 'w')
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&location=42.2808,83.7430&type=restaurant&pagetoken={}&key={}".format(search, nextpagetoken, API_KEY)
    

    request = requests.get(base_url)
    response = json.loads(request.text)
    open_file.write(json.dumps(response))
    open_file.close()


#write_json(API_KEY, pagetoken60, search2)

def sort_rest(API_KEY, search):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&location=42.2808,83.7430&type=restaurant&key={}".format(search, API_KEY)
    request = requests.get(base_url)
    response = json.loads(request.text)

    total = []
   # sort_lst = []

    for items in response['results']:
        if items['id'] not in total:
            total.append((items['rating'], items['id'], items['name']))
           # sort_lst.append(float(items['rating']))
    total = sorted(total, key = lambda x: x[0], reverse = True)
   # print(len(total))
   # print(total)
    return total


first20 = sort_rest(API_KEY, search)

def next(API_KEY, nextpagetoken, search):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&location=42.2808,83.7430&type=restaurant&pagetoken={}&key={}".format(search, nextpagetoken, API_KEY)
    request = requests.get(base_url)
    response = json.loads(request.text)

    total = []
   # sort_lst = []

    for items in response['results']:
        if items['id'] not in total:
            total.append((items['rating'], items['id'], items['name']))
           # sort_lst.append(float(items['rating']))
    total = sorted(total, key = lambda x: x[0], reverse = True)
   # print(len(total))
   # print(total)
    return total

upto40 = next(API_KEY, pagetoken40, search)
upto60 = next(API_KEY, pagetoken60, search)
upto80 = sort_rest(API_KEY, search2)
upto100 = sort_rest(API_KEY, search3)

everything = first20 + upto40 + upto60 + upto80 + upto100
everything = sorted(everything, key = lambda x: x[0], reverse = True)

def name(lst):
    names = []
    for items in lst:
        names.append(items[2])
    return names

def rest_id(lst):
    ids = []
    for items in lst:
        ids.append(items[1])
    return ids

def rating(lst):
    rates = []
    for items in lst:
        rates.append(items[0])
    return rates




def start_db():
    conn = sqlite3.connect('/Users/laurenwatsky/Documents/final-project/final-database.db')
    cur = conn.cursor()
       # cur.execute("DROP TABLE IF EXISTS zomato_data")
       # cur.execute("DROP TABLE IF EXISTS zomato")
    cur.execute("DROP TABLE IF EXISTS GoogleData")
    cur.execute("CREATE TABLE IF NOT EXISTS GoogleData (restaurant_name TEXT, restaurant_id INTEGER, restaurant_rating FLOAT)")

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
            cur.execute("INSERT INTO GoogleData (restaurant_name, restaurant_id, restaurant_rating) VALUES (?, ?, ?)", (_rest_name, _rest_id, _rest_rate))
            conn.commit()
        print('successfully added')
        cur.close()
    except:
        print("ERROR")

start_db()
write_db(name(everything)[0:20], rest_id(everything)[0:20], rating(everything)[0:20])
write_db(name(everything)[20:40], rest_id(everything)[20:40], rating(everything)[20:40])
write_db(name(everything)[40:60], rest_id(everything)[40:60], rating(everything)[40:60])
write_db(name(everything)[60:80], rest_id(everything)[60:80], rating(everything)[60:80])
write_db(name(everything)[80:], rest_id(everything)[80:], rating(everything)[80:])






