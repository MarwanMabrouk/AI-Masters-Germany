from flask import Flask, render_template, request
import pandas as pd
import openpyxl
import pymongo
from config import *
app = Flask(__name__)
db = pymongo.MongoClient()
DATABASE = db[DATABASE_NAME]
COLLECTION = DATABASE[COLLECTION_NAME]

#Calculate Unique Degrees
unique_degrees = 0
unique_set = set()
for i in COLLECTION.find({}, {"Uni Name": 1, "Degree Name": 1}):
    unique_set.add((i["Uni Name"], i["Degree Name"]))

unique_degrees = len(unique_set)

def get_data():
    
    course_name=COLLECTION.distinct("Course Name")
    degree_Name = COLLECTION.distinct("Degree Name")
    uni_fachhochschule_tu = COLLECTION.distinct("Uni/Fachhochschule/TU")

    #get no of unique Uni
    cuft = len(COLLECTION.distinct("Uni Name"))

    #get no of unique Degree 
    cdn = unique_degrees
    
    #get no of unique Course Name
    ccn = COLLECTION.count_documents({})



    return course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft


@app.route("/")
def firstPage():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("firstPage.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)


@app.route("/search")
def second_page():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("second_page.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)


if __name__ == '__main__':
    app.debug = True
    app.run()