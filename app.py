from flask import Flask, render_template, request
import pandas as pd
import openpyxl
import pandas as pd
from AI_masters_germany import utils, clustering, plotting
from AI_masters_germany.aim import AIM
from flask import Flask,render_template, request
import numpy as np
import json
import plotly
import threading
from pymongo import MongoClient

#TODO: convert credentials to environment variables
print('Connecting to database...')
USERNAME = "doadmin"
PASSWORD = "Rj5M6X7e219DvQ43"
DB_NAME = "data"
CONNECTION_STRING = 'mongodb+srv://{username}:{password}@{host}/{dbname}?{options}'.\
    format(username=USERNAME,
           password=PASSWORD,
           host='ai-masters-8e63c445.mongo.ondigitalocean.com',
           dbname=DB_NAME,
           options='tls=true&authSource=admin&replicaSet=ai-masters')
client = MongoClient(CONNECTION_STRING)

db = client['data']
collection = db['data']
print('Done connecting to database!')

app = Flask(__name__)
aim = AIM(collection_object=collection)


def get_data():
    course_name=collection.distinct("Course Name")
    degree_Name = collection.distinct("Degree Name")
    uni_fachhochschule_tu = collection.distinct("Uni/Fachhochschule/TU")

    #get no of unique Uni
    cuft = len(collection.distinct("Uni Name"))

    #get no of unique Degree 
    cdn = len(collection.distinct("Degree Name"))
    
    #get no of unique Course Name
    ccn = collection.count_documents({})

    return course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft


@app.route("/")
def firstPage():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("firstPage.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)

@app.route("/visualization")
def third_page():
    return render_template("third_page.html")

@app.route("/search")
def second_page():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("second_page.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)
@app.route("/institute_types")
def institute_types():

    database = aim.get_database()
    fig = plotting.plot_institute_types(database, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("institute_types.html", fig_json=fig_json)

@app.route("/lecture_types")
def lecture_types():

    database = aim.get_database()
    fig = plotting.plot_lecture_types(database, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("lecture_types.html", fig_json=fig_json)


@app.route("/course_clustering", methods=["GET", "POST"])
def course_clustering():

    database = aim.get_database()
    clusters = aim.get_clustered_courses()

    if request.method == "POST":

        specialisation_conditions = pd.Series([False] * len(database["Uni Name"]))
        checked_specialisations = request.form.getlist("specialisation")
        ai_rows = database["Degree Name Tokens"].str.contains("Artificial Intelligence", na=False)
        ds_rows = database["Degree Name Tokens"].str.contains("Data Science", na=False)
        da_rows = database["Degree Name Tokens"].str.contains("Data Analytics", na=False)
        ml_rows = database["Degree Name Tokens"].str.contains("Machine Learning", na=False)
        other_rows = ~ai_rows & ~ds_rows & ~da_rows & ~ml_rows

        if "AI" in checked_specialisations:
            specialisation_conditions |= ai_rows
        if "DS" in checked_specialisations:
            specialisation_conditions |= ds_rows
        if "DA" in checked_specialisations:
            specialisation_conditions |= da_rows
        if "ML" in checked_specialisations:
            specialisation_conditions |= ml_rows
        if "other" in checked_specialisations:
            specialisation_conditions |= other_rows

        min_credits = int(request.form["min_credits"])
        max_credits = int(request.form["max_credits"])

        credits_condition = (
            (database["ECTS"] >= min_credits) &
            (database["ECTS"] <= max_credits)
        )

        lecture_type = request.form["lecture_type"]
        if lecture_type == "all":
            lecture_type_condition = pd.Series([True] * len(database["Type"]))
        elif lecture_type == "Obligatory":
            lecture_type_condition = database["Type"] == "Obligatory"
        else:
            lecture_type_condition = database["Type"] == "Elective"

        data = clusters[credits_condition & lecture_type_condition & specialisation_conditions]

    else:
        min_credits = 1
        max_credits = int(database["ECTS"].max())

        lecture_type = "all"

        data = clusters

        checked_specialisations = ["AI", "DS", "DA", "ML", "other"]

    fig = plotting.plot_clusters(data, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("course_clustering.html",
                           fig_json=fig_json,
                           min_credits=min_credits, max_credits=max_credits,
                           lecture_type=lecture_type,
                           checked_specialisations=checked_specialisations)

  
@app.route("/popular_courses", methods=["GET", "POST"])
def popular_courses():

    database = aim.get_database()
    clusters = aim.get_clustered_courses()

    if request.method == "POST":
        min_credits = int(request.form["min_credits"])
        max_credits = int(request.form["max_credits"])

        credits_condition = (
            (database["ECTS"] >= min_credits) &
            (database["ECTS"] <= max_credits)
        )

        lecture_type = request.form["lecture_type"]
        if lecture_type == "all":
            lecture_type_condition = pd.Series([True] * len(database["Type"]))
        elif lecture_type == "Obligatory":
            lecture_type_condition = database["Type"] == "Obligatory"
        else:
            lecture_type_condition = database["Type"] == "Elective"

        data = clusters[credits_condition & lecture_type_condition]  # todo: adapt for popular courses instead of clustering

    else:
        min_credits = 1
        max_credits = int(database["ECTS"].max())

        lecture_type = "all"

        data = clusters

    fig = plotting.plot_popular_courses(data, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("popular_courses.html",
                           fig_json=fig_json,
                           min_credits=min_credits, max_credits=max_credits,
                           lecture_type=lecture_type)


if __name__ == '__main__':
    DATASET_PATH = './dataset.csv'
    course_clustering_thread = threading.Thread(target=aim.cluster_courses, args=())
    course_clustering_thread.start()

    app.debug = True
    app.run()