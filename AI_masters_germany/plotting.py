import pandas as pd
import plotly.express as px


def plot_institute_types(database, show_plot=False):
    """
    Generate bar chart to visualize amount of different types of institutes in the database.

    :param database: Database in the form of a pands Dataframe.
    :param show_plot: Boolean value specifying if plot should be shown.
                      In case of set to False, only return Plotly figure but don't show it directly.
                      Defaults is False.

    :return: Plotly figure bar chart visualizing amount of different types of institutes in the database.
    """    

    institutes = database[["Uni/Fachhochschule/TU", "Uni Name"]]
    institutes = institutes.drop_duplicates()

    institute_counts = institutes["Uni/Fachhochschule/TU"].value_counts()
    institutes["Amount_Institute_Type"] = institutes["Uni/Fachhochschule/TU"].map(institute_counts)

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


def plot_lecture_types(database, show_plot=False):
    """
    Generates bar chart for the visualization of amount of different types of lectures in database
    (i.e., amount of obligatory and elective courses).

    :param database: Database in the form of a pands Dataframe.
    :param show_plot: Boolean value specifying if plot should be shown.
                      In case of set to False, only return Plotly figure but don't show it directly.
                      Defaults is False.

    :return: Plotly figure bar chart visualizing the amount of different types of lectures in database.
    """    
    database = database.copy()
    database["Name"] = database["Uni Name"] + " - " + database["Degree Name"]

    lectures = database[["Name", "Type"]]
    lectures = lectures.drop_duplicates()

    lectures["Amount"] = lectures.apply(
        lambda row: database[(database["Name"] == row["Name"]) & (database["Type"] == row["Type"])].shape[0], axis=1
    )

    fig = px.bar(
        lectures,
        x="Amount",
        y="Name",
        color="Type",
        barmode="group"
    )

    fig.update_layout(
        xaxis_title="Entries in the database",
        yaxis_title="Study degree"
    )

    if show_plot:
        fig.show()

    return fig


def plot_clusters(clustering_result, show_plot=False):
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


def plot_popular_courses(data, show_plot=False):
    """
    Generates bar chart to visualize density of each cluster.

    :param data: Database of institutes in the form of a pands Dataframe.
    :param show_plot: Boolean value specifying if plot should be shown.
                      In case of set to False, only return Plotly figure but don't show it directly.
                      Defaults is False.

    :return: Plotly figure bar chart visualizing the densities of each cluster.
    """    
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


