##################### HEAD #######################

import requests
from selenium import webdriver
from lxml import html

import pprint
import sys
import csv

#################### CONFIG ######################

debug = True
print_headers = False
path_to_chromedriver = "/Users/Admin/Desktop/chromedriver"

################### FUNCTIONS ####################


# This function prompts the keyord and returns it with chosen character as encoding
def encode(character, query = None):

    if not query:
        query = raw_input("[Info] Enter search query >>> ")

    query = query.strip().replace(" ", character) 

    return query


# This function fetches the website and returns an html object
def load(url, client = None, headers = {}):

    if not headers: 
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    if not client:
        client = requests.Session()    

    try:
        response = client.get(url, headers = headers)

        if debug:
            file = open("url.html", 'w')
            file.write(response.content)
        if print_headers:
            print response.status_code # Response Code  
            print response.headers # Response Headers

    except:
        print "[ERROR] Connection error."  
              
        if debug:
            file = open("url.html", 'w')
            file.write(response.content)
        if print_headers:
            print response.status_code # Response Code  
            print response.headers # Response Headers
        quit()

    try:
        response = response.content.replace('<!--', '').replace('-->', '')
        response = html.fromstring(response)
    except:
        print "[ERROR] Parsing error."
        quit()

    return response, client


def browse(url, client = None, headers = {}):

    if not headers: 
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}

    #if not client:
    #    client = requests.Session()    

    try:
        browser = webdriver.Chrome(executable_path = path_to_chromedriver)
        response = browser.get(url)

    except:
        print "[ERROR] Connection error."
        quit()

    #try:
    #    response = response.content.replace('<!--', '').replace('-->', '')
    #    response = html.fromstring(response)
    #except:
    #    print "[ERROR] Parsing error."
    #    quit()

    return response, client


def pretty_print(objects, fields):

    print "-" * 80

    for j in fields:
        for i, obj in enumerate(objects):
            i += 1
            print "[{:2}]".format(i), getattr(obj, j)
        print "-" * 80 


# This function prints listings to console
def output_console(objects, fields):

    row_headers = [field.capitalize() for field in fields]

    print u"-" * 160

    print u"[##]  ",
    for i, column in enumerate(row_headers):  
        print u"{:32}    ".format(column[:32]), 
    print ""

    for i, obj in enumerate(objects):
        row = [getattr(obj, field) for field in fields]

        print u"[{:2}]  ".format(i+1),
        for column in row:
            print u"{:32}    ".format(column[:32]), 
        print "" 

    print "-" * 160


# This function exports listings as csv file
def output_csv(filename, objects, fields):

    if ".csv" not in filename: filename = filename + ".csv"

    row_headers = [field.capitalize() for field in fields]

    try :
        file = open(filename, "a")
        writer = csv.writer(file)
    except :
        file = open(filename, "w")
        write = csv.writer(file)
        writer.writerow(row_headers)

    for obj in objects:
        row = [getattr(obj, field) for field in fields]
        row = [column.encode('utf-8') for column in row]
        writer.writerow(row)

    print "[Info] Wrote to {}".format(filename)
