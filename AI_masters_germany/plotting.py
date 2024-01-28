import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_institute_types(database, show_plot=True):

    institutes = database[["Uni/Fachhochschule/TU", "Uni Name"]]
    institutes = institutes.drop_duplicates()
    # Now we have one entry per school

    institute_counts = institutes["Uni/Fachhochschule/TU"].value_counts()
    institutes["Amount_Institute_Type"] = institutes["Uni/Fachhochschule/TU"].map(institute_counts)
    # Now we know how many Unis, TU's etc. are in the dataset

    # We have a lot of repetition we are now going to remove
    institutes = institutes[["Uni/Fachhochschule/TU", "Amount_Institute_Type"]]
    institutes = institutes.drop_duplicates()


    institutes["Names"] = institutes["Uni/Fachhochschule/TU"].apply(
        lambda x: ", <br>".join(database[database["Uni/Fachhochschule/TU"] == x]["Uni Name"].unique())
    )

    fig = px.bar(
        institutes,
        x="Uni/Fachhochschule/TU",
        y="Amount_Institute_Type",
        hover_data=["Names"],
        color="Uni/Fachhochschule/TU",
        color_discrete_sequence=["black", "red", "yellow"]
    )

    fig.update_layout(
        xaxis_title="Institute type",
        yaxis_title="Entries in the database"
    )

    if show_plot:
        fig.show()

    return fig


def plot_lecture_types(database, show_plot):
    database = database.copy()
    database["Name"] = database["Uni Name"] + " - " + database["Degree Name"]

    lectures = database[["Name", "Type"]]
    lectures = lectures.drop_duplicates()

    lectures["Amount"] = lectures.apply(
        lambda row: database[(database["Name"] == row["Name"]) & (database["Type"] == row["Type"])].shape[0], axis=1
    )

    fig = px.bar(
        lectures,
        x="Name",
        y="Amount",
        color="Type",
        barmode="group"
    )

    fig.update_layout(
        xaxis_title="Study degree",
        yaxis_title="Entries in the database"
    )

    if show_plot:
        fig.show()

    return fig


def plot_clusters(clustering_result, show_plot=True):
    """
    Plot course clustering result.

    :param clustering_result: Result of cluster_courses method.
    :param show_plot: Set to True to show the plot.
    :return: Plotly figure object.
    """

    fig = px.scatter(
        clustering_result,
        x="Component_1",
        y="Component_2",
        color="Cluster",
        title="Course clustering result",
        hover_data=["Course Name", "Degree Name", "Uni Name"]
    )

    if show_plot:
        fig.show()

    return fig

def plot_popular_courses(data, show_plot=True):
    # todo: Fill with code
    fig=px.bar(
        data,
        x="Cluster Count",
        y="Cluster Name",
        color="Cluster",
        title="Cluster Density",
        hover_data=["Cluster Name"]
    )
    if show_plot:
        fig.show()

    return fig

def plot_similar_courses(data,show_plot):
    
    fig=px.bar(
        data,
        x="Course Name",
        y="score",
        color="Course Name",
        title="Course Similarity Plot",
        hover_data=["Uni Name","Course Description","Goals"]
    )
    print(data["Course Name"])
    if show_plot:
        fig.show()
    
    return fig
