#project 2: webscraper using beautiful soup4vand requests

import requests
from bs4 import BeautifulSoup
import pandas 
import argparse
import connect 

parser = argparse.ArgumentParser()
parser.add_argument("--page_num_max", helps="Enter the number of pages to parse", type=int)
parser.add_argument("--dbname", help="Enter the name of db", type=str)
args = parser.parse_args()

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore//?page="
page_num_MAX = 3

for page_num in range(1, page_num_MAX):
    url = oyo_url + str(page_num)
    print("GET request for: " + url )
    req = requests.get(url)
    content = req.content

    soup = BeautifulSoup(content, "html.parser")

    all_hotels = soup.find_all("div", {"class": "hotelCardListing"})
    scraped_info_list = []

    for hotel in all_hotels:
        hotel_dict = {}   
        hotel_dict["name"] = hotel.find("h3", {"class": "listinghoteldescription__hotelName"}).text
        hotel_dict["address"] = hotel.find("span", {"itemprop":  "streetAddress"}).text
        hotel_dict["price"] = hotel.find ("span",{"class": "listingprice_finalprice"}).text
        #try ..... except
        try:
            hotel_dict["rating"] = hotel.find("span", {"class": "hotelrating__ratingsummary"}).text
        except AttributeError:
            hotel_dict["rating"] = None
     
        parent_amenities_element = hotel.find("div", {"class": "amenitywrapper"})
    
        amenities_list = []
    for amenity in parent_amenities_element.find_all("div", {"class": "amenitywrapper_amenity"}):
        amenities_list.append(amenity.find("span", {"class": "d-body-sm"}).text.strip())
    
    hotel_dict["amenities"] = ','.join(amenities_list[:-1])
    
    scraped_info_list.append(hotel_dict)
    connect.insert_into_table(args.dbname, tuple(hotel_dict.values()))
    
    #print(hotel_name, hotel_address, hotel_rating, amenities_list)
          
dataframe = pandas.dataframe(scraped_info_list)
print("creating csv file...")
dataframe.to_csv("oyo.csv")
connect.get_hotel_info(args.dbname)