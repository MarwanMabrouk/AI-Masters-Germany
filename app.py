import threading
import subprocess
import json
import numpy as np
import pandas as pd
import plotly
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from AI_masters_germany import plotting, map, similarity
from AI_masters_germany.aim import AIM
from config import CONNECTION_STRING

#TODO: convert credentials to environment variables
print('Connecting to database...')
client = MongoClient(CONNECTION_STRING)

db = client['data']
collection = db['data']
print('Done connecting to database!')

app = Flask(__name__)

# Start clustering courses in a thread
aim = AIM(collection_object=collection)
course_clustering_thread = threading.Thread(target=aim.cluster_courses, args=())
course_clustering_thread.start()

# Load sentece transformer
print('Loading sentence transformer model...')
sentence_transformer_model = 'sentence-transformers/msmarco-distilbert-multilingual-en-de-v2-tmp-lng-aligned'
embedder = SentenceTransformer(sentence_transformer_model)
print('Done loading sentence transformer model!')
corpus_embeddings=None

@app.route("/", methods=["GET", "POST"])
def first_page():
    """
    Main site showing information like
    - total number of degrees
    - total number of institutes
    - total number of courses
    """
    course_name = collection.distinct("Course Name")
    degree_Name = collection.distinct("Degree Name")
    uni_fachhochschule_tu = collection.distinct("Uni/Fachhochschule/TU")
    uni_amount = len(collection.distinct("Uni Name", {"Uni/Fachhochschule/TU": "Universität"}))
    tu_amount = len(collection.distinct("Uni Name", {"Uni/Fachhochschule/TU": "TU"}))
    hochschule_amount = len(collection.distinct("Uni Name", {"Uni/Fachhochschule/TU": "Hochschule"}))

    # Get amount of unique Uni
    cuft = len(collection.distinct("Uni Name"))

    # Get amount of unique Degree Uni Pairs
    result = collection.aggregate(
        [
            {"$group": {"_id": {"Uni Name": "$Uni Name", "Degree Name": "$Degree Name"}}}
        ]
    )
    cdn = 0
    for _ in result:
        cdn += 1
    # Get amount of unique Course Name
    ccn = collection.count_documents({})

    return render_template(
        "firstPage.html",
        course_name=course_name,
        degree_Name=degree_Name,
        uft=uni_fachhochschule_tu,
        ccn=ccn,
        cdn=cdn,
        cuft=cuft,
        uni_amount=uni_amount,
        tu_amount=tu_amount,
        hochschule_amount=hochschule_amount
    )

@app.route("/visualization")
def third_page():
    return render_template("third_page.html")


@app.route("/search")
def second_page():
    """
    Search page that allows you to select a study degree and then returns
    a list of courses contained in the corresponding study degree.
    """
    database = aim.get_database(unprocessed=True).copy()
    database["degree_choices"] = database["Degree Name"] + " - " + database["Uni Name"]
    degree_choices = database["degree_choices"].unique()
    degree_choices = np.sort(degree_choices)

    return render_template("search_db.html", degree_choices=degree_choices)


@app.route('/search-update_selected_degree', methods=['POST'])
def search__update_selected_degree():

    data = request.get_json()
    selected_degree = data.get('selectedValue')

    database = aim.get_database(unprocessed=True).copy()
    database["degree_choices"] = database["Degree Name"] + " - " + database["Uni Name"]

    courses = database[database["degree_choices"] == selected_degree]["Course Name"].to_list()
    courses.sort()

    return jsonify(courses)


@app.route("/institute_types")
def institute_types():
    """
    Site that shows amount of different institute (types) in dataset (e.g., amount of universities, amount of TU's etc.).
    """

    database = aim.get_database()
    fig = plotting.plot_institute_types(database, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("institute_types.html", fig_json=fig_json)


@app.route("/map_view")
def map_view():
    """
    Site showing the location of the institutes in our dataset.
    """
    database = aim.get_database()
    fig = map.get_map(database)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("map_view.html", fig_json=fig_json)


@app.route("/lecture_types")
def lecture_types():
    """
    Site showing the amount of obligatory and elective courses per study degree.
    """

    database = aim.get_database()
    fig = plotting.plot_lecture_types(database, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("lecture_types.html", fig_json=fig_json)


@app.route("/course_clustering", methods=["GET", "POST"])
def course_clustering():
    """
    Site showing the result of course clustering and the density of the clusters.
    """
    
    database = aim.get_database()
    clusters = aim.get_clustered_courses()

    if request.method == "POST":
        top_freq = int(request.form["top_freq"])
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
        top_freq = 10
        min_credits = 1
        max_credits = int(database["ECTS"].max())

        lecture_type = "all"

        data = clusters

        checked_specialisations = ["AI", "DS", "DA", "ML", "other"]

    fig = plotting.plot_clusters(data, show_plot=False)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    grouped_data = data.groupby(["Cluster", "Cluster Name"]).size().reset_index(name='Cluster Count')
    grouped_data = grouped_data.sort_values(by="Cluster Count", ascending=False)
    fig_density = plotting.plot_popular_courses(grouped_data[:top_freq], show_plot=False)
    fig_density_html = fig_density.to_html()
    return render_template("course_clustering.html",
                           fig_json=fig_json,
                           fig_density_html=fig_density_html,
                           top_freq=top_freq,
                           min_credits=min_credits, max_credits=max_credits,
                           lecture_type=lecture_type,
                           checked_specialisations=checked_specialisations)


@app.route("/search_courses", methods=["GET", "POST"])
def search_courses():
    """
    Site allowing the user to search for similar courses.
    """
    database = aim.get_database()
    if request.method == "POST":
        search_query=request.form["search_query"]
        top_freq = 10

        data = database
        global corpus_embeddings
        if corpus_embeddings is None:
            print('Running Corpus Embedding')
            corpus_embeddings = similarity.encode_text(
                df=data,
                embedder=embedder,
                features=['Course Name', 'Course Description', 'Goals']
            )
            print('Done Embedding')
        search_results = similarity.text_similarity(
            query=search_query,
            embedder=embedder,
            corpus_embeddings=corpus_embeddings,
            top_k=top_freq
        )
    
        data = data.iloc[search_results[1]]
        data["Similarity Score"] = [f"{score.item()*100:.2f}"+"%" for score in search_results[0]]
        data["score"] = search_results[0]
        data = data[["Uni Name", "Course Name", "Course Description", "Goals", "Similarity Score"]].reset_index(drop=True)
        table_html = data.to_html()
    else:
        search_query = ""
        table_html = None
    
    return render_template("search_courses.html",
                           table_html=table_html,
                           search_query=search_query)

@app.route("/github_webhook", methods=["GET", "POST"])
def github_webhook():
    #do git pull inside of a specific folder
    print('Pulling from github...')

    process = subprocess.Popen("git pull", shell=True)

    return "Done"


if __name__ == '__main__':
    
    app.debug = True
    app.run()
