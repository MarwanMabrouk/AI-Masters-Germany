import pandas as pd
from AI_masters_germany import utils, clustering, plotting
from flask import Flask,render_template, request
import numpy as np
import json
import plotly

app = Flask(__name__)

database = pd.read_csv("dataset.csv")
database = utils.database_preprocessing(database, remove_stopwords=False)
database_without_stopwords = utils.database_preprocessing(database, remove_stopwords=True)


# We need already do the clustering
# Doing this at the time the user wants to see the clustering site takes to long!
clustering_result = clustering.cluster_courses(
    df=database_without_stopwords,
    k_ranges=np.linspace(80, 111, 30)
)

@app.route("/")
def firstPage():
    return render_template("firstPage.html")

@app.route("/course_clustering")
def course_clustering():
    fig = plotting.plot_clusters(clustering_result, show_plot=False)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("course_clustering.html", graphJSON=graphJSON)


if __name__ == '__main__':
    app.debug = True
    app.run()
