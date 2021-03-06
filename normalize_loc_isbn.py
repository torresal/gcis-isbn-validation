import requests
from isbnlib import EAN13, clean, canonical
import os
import json
#import logging

#log = 

error_log = open("book_error_log", "w")
problem_json = []
config = open("isbn.conf", "r")

if not os.path.isdir("isbn13_book/"):
    os.makedirs("isbn13_book/")
if not os.path.isdir("problem_book/"):
    os.makedirs("problem_book/")
if not os.path.isdir("non13_book"):
    os.makedirs("non13_book")

def get_book_dir():
    for line in config:
        if line.startswith("book_json_loc"):
            temp = line.split(":")[1].rstrip("\n")
            temp = temp.replace(" ", "")
            return temp

book_dir = get_book_dir()
#print book_dir

directory = "gcis-isbn-validation/%s"%book_dir


for (root, dirs, files) in os.walk(book_dir):
    for f in files:
        with open(book_dir+f) as item:
        #print "hi"
            json_item = json.load(item)
            book_isbn = json_item['isbn']
            if book_isbn is not None:
                if book_isbn == "None": 
                    with open("problem_book/"+str(f),'w') as jsonFile:
                        jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',',': ')))
                else:
                    book_isbn = clean(book_isbn)
                #book_isbn = book_isbn.replace("-", "")
                    #book_isbn = EAN13(book_isbn)            
                    if EAN13(book_isbn) != None:
                        book_isbn = EAN13(book_isbn)
                    
                        json_item['isbn'] = book_isbn
                        print json_item['isbn']
                        with open("isbn13_book/"+str(f), 'w') as jsonFile:
                            jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',', ': ')))
                    else:
                        with open("non13_book/"+str(f), 'w') as jsonFile:
                            jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',', ': ')))
                    
            else:
                with open("problem_book/"+str(f),'w') as jsonFile:
                    jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',',': ')))
#                problem_json.append(json.load(item))
            #print json_item['isbn']
            #print book_isbn



#print problem_json

        #open file get isbn
        #look up isbn on loc

