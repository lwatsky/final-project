import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import os
import numpy as np
import matplotlib.patches as mpatches

googlezomato1 = "GoogleZomato"
yelpgoogle2 = "YelpGoogle"
yelpzomato3 = "YelpZomato"

title1 = "Restaurants on Both Google and Zomato"
title2 = "Restaurants on Both Yelp and Google"
title3 = "Restaurants on Both Yelp and Zomato"

savename1 = "ZGVisualization.png"
savename2 = "YGVisualization.png"
savename3 = "YZVisualization.png"


def visualization1(tablename, title, savename):
    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        cur.execute("SELECT {}.restaurant_name, {}.super_rating, {}.city_id FROM {}".format(tablename, tablename, tablename, tablename))
        names = []
        super_rating = []
        cityids =[]
        data = cur.fetchall()
        for values in data:
            names.append(values[0])
            super_rating.append(values[1])
            cityids.append(values[2])
        colors = []
        for cities in cityids:
            if cities == 1:
                colors.append('red')
            if cities ==2:
                colors.append('orange')
            if cities ==3:
                colors.append('yellow')
            if cities ==4:
                colors.append('green')
            if cities == 5:
                colors.append('blue')
        print(colors)
        
        xvals = names
        yvals = super_rating
        plt.bar(xvals, yvals, align= 'center', color = colors)

        plt.xticks(rotation= 'vertical', fontsize =8)
        plt.ylabel("Super Rating", fontsize = 12)
        plt.ylim(8, 10)
        plt.xlabel("Restaurant Name", fontsize = 12)
        red_patch = mpatches.Patch(color='red', label='Ann Arbor')
        orange = mpatches.Patch(color='orange', label='Gainesville')
        yellow = mpatches.Patch(color='yellow', label='Austin')
        green = mpatches.Patch(color='green', label='Bloomington')
        blue = mpatches.Patch(color='Blue', label='Madison')
        plt.legend(handles=[red_patch, orange, yellow, green, blue])
        plt.title(title, fontsize = 15)
        plt.savefig(savename)
        plt.show()

    except:
        print("NOT WORKING")


googlezomato1 = "GoogleZomato"
yelpgoogle2 = "YelpGoogle"
yelpzomato3 = "YelpZomato"

title1 = "Restaurants on Both Google and Zomato"
title2 = "Restaurants on Both Yelp and Google"
title3 = "Restaurants on Both Yelp and Zomato"

savename1 = "ZGVisualization.png"
savename2 = "YGVisualization.png"
savename3 = "YZVisualization.png"

visualization1(googlezomato1, title1, savename1)
visualization1(yelpgoogle2, title2, savename2)
visualization1(yelpzomato3, title3, savename3)

def visualization2():
    try:
        conn = sqlite3.connect('final-database.db')
        cur = conn.cursor()
        cur.execute("SELECT YelpZomato.restaurant_name, YelpZomato.super_rating, YelpZomato.city_id, GoogleData.restaurant_rating FROM YelpZomato INNER JOIN GoogleData ON YelpZomato.restaurant_name = GoogleData.restaurant_name")
        data = cur.fetchall()
        names = []
        super_ratings = []
        cityids = []
        for row in data:
            names.append(row[0])
            super_ratings.append(row[1]+row[3])
            cityids.append(row[2])
        colors = []
        for cities in cityids:
            if cities == 1:
                colors.append('red')
            if cities ==2:
                colors.append('orange')
            if cities ==3:
                colors.append('yellow')
            if cities ==4:
                colors.append('green')
            if cities == 5:
                colors.append('blue')

        xvals = names
        yvals = super_ratings
        plt.bar(xvals, yvals, align= 'center', color = colors)

        plt.xticks(rotation= 'horizontal', fontsize =8)
        plt.ylabel("Max Rating", fontsize = 12)
        plt.ylim(10, 15)
        plt.xlabel("Restaurant Name", fontsize = 12)
        red_patch = mpatches.Patch(color='red', label='Ann Arbor')
        orange = mpatches.Patch(color='orange', label='Gainesville')
        yellow = mpatches.Patch(color='yellow', label='Austin')
        green = mpatches.Patch(color='green', label='Bloomington')
        blue = mpatches.Patch(color='Blue', label='Madison')
        plt.legend(handles=[red_patch, orange, yellow, green, blue])
        plt.title("Restaurants on All 3 API's", fontsize = 15)
        plt.savefig("All3.png")
        plt.show()

    except:
        print("NOT WORKING")

visualization2()