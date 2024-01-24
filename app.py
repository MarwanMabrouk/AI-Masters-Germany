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

app = Flask(__name__)
aim = AIM()  # Object that allows clustering etc.

def get_data():
    data=pd.read_excel("University Data LA Project(4).xlsx")
    course_name=data['Course Name'].tolist()
    degree_Name=data['Degree Name'].unique().tolist()
    uni_fachhochschule_tu=data['Uni/Fachhochschule/TU'].unique().tolist()
    #uni_name=data['Uni Name'].unique().tolist()
    ccn=len(course_name)
    cdn=len(degree_Name)
    cuft=len(uni_fachhochschule_tu)
    return course_name, degree_Name,uni_fachhochschule_tu,ccn,cdn,cuft


def get_data():
    data = pd.read_excel("University Data LA Project(4).xlsx")
    course_name = data['Course Name'].tolist()
    degree_Name = data['Degree Name'].unique().tolist()
    uni_fachhochschule_tu = data['Uni/Fachhochschule/TU'].unique().tolist()
    # uni_name=data['Uni Name'].unique().tolist()
    ccn = len(course_name)
    cdn = len(degree_Name)
    cuft = len(uni_fachhochschule_tu)
    return course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft


@app.route("/")
def firstPage():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("firstPage.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)

@app.route("/visualization")
def third_page():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("third_page.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)

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

        data = clusters[credits_condition & lecture_type_condition]

    else:
        min_credits = 1
        max_credits = int(database["ECTS"].max())

        lecture_type = "all"

        data = clusters

    fig = plotting.plot_clusters(data, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("course_clustering.html",
                           fig_json=fig_json,
                           min_credits=min_credits, max_credits=max_credits,
                           lecture_type=lecture_type)

  
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
    load_database_thread = threading.Thread(target=aim.load_database, args=(DATASET_PATH,))
    course_clustering_thread = threading.Thread(target=aim.cluster_courses, args=())

    load_database_thread.start()
    load_database_thread.join()
    course_clustering_thread.start()

    app.debug = True
    app.run()