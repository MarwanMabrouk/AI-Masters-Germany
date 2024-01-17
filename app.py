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


@app.route("/")
def firstPage():
    return render_template("firstPage.html")


@app.route("/course_clustering", methods=['GET', 'POST'])
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
        if lecture_type == 'all':
            lecture_type_condition = pd.Series([True] * len(database["Type"]))
        elif lecture_type == 'Obligatory':
            lecture_type_condition = database["Type"] == "Obligatory"
        else:
            lecture_type_condition = database["Type"] == "Elective"

        data = clusters[credits_condition & lecture_type_condition]

    else:
        min_credits = 1
        max_credits = int(database["ECTS"].max())

        lecture_type = 'all'

        data = clusters

    fig = plotting.plot_clusters(data, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("course_clustering.html",
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
