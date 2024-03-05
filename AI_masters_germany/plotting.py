import pandas as pd
import plotly.express as px


def plot_institute_types(database, show_plot=False):
    """generates bar chart to visualize types of institutes in the database

    Args:
        database (PandasDataframe): Database of insitutes loaded as a pandas dataframe
        show_plot (bool, optional): specifies if plot should be shown seperately. Defaults to True.

    Returns:
        Plotly Figure: Bar chart of typres of institutes in database
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
    """generates bar chart for the visualization of types of lectures in database

    Args:
        database (Pandas Dataframe): Database of insitutes loaded as a pandas dataframe
        show_plot (bool, optional): specifies if plot should be shown seperately. Defaults to False.

    Returns:
        Plotly Figure: Bar chart of typres of institutes in database
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
    """generates bar chart to visualize density of each cluster

    Args:
        data (Pandas Dataframe): Database of insitutes loaded as a pandas dataframe
        show_plot (bool, optional): specifies if plot should be shown seperately. Defaults to False.

    Returns:
        Plotly Figure: Bar chart to represent density of courses clusters
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


