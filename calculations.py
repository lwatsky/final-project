#Final Project
#Lauren Watsky, Katie Wolberg, Jamie Zuckerman

#this file will select data from the database and calculate values from it
#it will output the calculated data to a file
#can store the calculated data in the database
#wrote out the visualizations in another python file

import json
import os
import requests
import sqlite3

def join_yelpgoogle():
    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        cur.execute("SELECT YelpData.restaurant_name, YelpData.restaurant_rating, GoogleData.restaurant_rating, GoogleData.city_id FROM YelpData INNER JOIN GoogleData ON YelpData.restaurant_name = GoogleData.restaurant_name")
        data = cur.fetchall()
        cur.execute("DROP TABLE IF EXISTS YelpGoogle")
        cur.execute("CREATE TABLE IF NOT EXISTS YelpGoogle (restaurant_name TEXT, yelp_rating FLOAT, google_rating FLOAT, super_rating FLOAT, city_id INTEGER)")
        for row in data:
            restname = row[0]
            yelprate = row[1]
            googlerate = row[2]
            superrate = yelprate + googlerate
            cityid = row[3]
            cur.execute("INSERT INTO YelpGoogle (restaurant_name, yelp_rating, google_rating, super_rating, city_id) VALUES (?, ?, ?, ?, ?)", (restname, yelprate, googlerate, superrate, cityid))
        conn.commit()
        print("YAY")
        cur.close()
    except:
        print("NOT WORKING")

join_yelpgoogle()

def join_yelpzomato():
    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        cur.execute("SELECT YelpData.restaurant_name, YelpData.restaurant_rating, ZomatoData.restaurant_rating, ZomatoData.city_id FROM YelpData INNER JOIN ZomatoData ON YelpData.restaurant_name = ZomatoData.restaurant_name")
        data = cur.fetchall()
        cur.execute("DROP TABLE IF EXISTS YelpZomato")
        cur.execute("CREATE TABLE IF NOT EXISTS YelpZomato (restaurant_name TEXT, yelp_rating FLOAT, zomato_rating FLOAT, super_rating FLOAT, city_id INTEGER)")
        for row in data:
            restname = row[0]
            yelprate = row[1]
            zomatorate = row[2]
            superrate = yelprate + zomatorate
            cityid = row[3]
            cur.execute("INSERT INTO YelpZomato (restaurant_name, yelp_rating, zomato_rating, super_rating, city_id) VALUES (?, ?, ?, ?, ?)", (restname, yelprate, zomatorate, superrate, cityid))
        conn.commit()
        print("YAY")
        cur.close()
    except:
        print("NOT WORKING")

join_yelpzomato()

def join_googlezomato():
    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        cur.execute("SELECT GoogleData.restaurant_name, GoogleData.restaurant_rating, ZomatoData.restaurant_rating, ZomatoData.city_id FROM GoogleData INNER JOIN ZomatoData ON GoogleData.restaurant_name = ZomatoData.restaurant_name")
        data = cur.fetchall()
        cur.execute("DROP TABLE IF EXISTS GoogleZomato")
        cur.execute("CREATE TABLE IF NOT EXISTS GoogleZomato (restaurant_name TEXT, google_rating FLOAT, zomato_rating FLOAT, super_rating FLOAT, city_id INTEGER)")
        for row in data:
            restname = row[0]
            googlerate = row[1]
            zomatorate = row[2]
            superrate = googlerate + zomatorate
            cityid = row[3]
            cur.execute("INSERT INTO GoogleZomato (restaurant_name, google_rating, zomato_rating, super_rating, city_id) VALUES (?, ?, ?, ?, ?)", (restname, googlerate, zomatorate, superrate, cityid))
        
        conn.commit()
        print("YAY")
        cur.close()
    except:
        print("NOT WORKING")
    

join_googlezomato()



def write_txt(filename):
    fileobject = open(filename, 'w')
    conn = sqlite3.connect('final-database.db')
    cur = conn.cursor()
    fileobject.write("The calculated data from the Google+Zomato Superrating\n")
    cur.execute('SELECT GoogleZomato.restaurant_name, GoogleZomato.super_rating FROM GoogleZomato')
    data = cur.fetchall()
    restname = ''
    for item in data:
        restname = item[0]
        item = item[1]
        fileobject.write(restname+': '+(str(item)[:3])+'\n')
    
    fileobject.write("\nThe calculated data from the Yelp+Zomato Superrating\n")
    cur.execute('SELECT YelpZomato.restaurant_name, YelpZomato.super_rating FROM YelpZomato')
    data2 = cur.fetchall()
    restname2 = ''
    for item in data2:
        restname2 = item[0]
        item = item[1]
        fileobject.write(restname2+': '+(str(item)[:3])+'\n')

    fileobject.write("\nThe calculated data from the Google+Yelp Superrating\n")
    cur.execute('SELECT YelpGoogle.restaurant_name, YelpGoogle.super_rating FROM YelpGoogle')
    data3 = cur.fetchall()
    restname3 = ''
    for item in data3:
        restname3 = item[0]
        item = item[1]
        fileobject.write(restname3+': '+(str(item)[:3])+'\n')
            



write_txt('finalcalculations.txt')
