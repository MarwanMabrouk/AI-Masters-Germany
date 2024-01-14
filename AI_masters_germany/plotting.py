import pandas as pd
import plotly.express as px


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
        lambda x: ', <br>'.join(database[database["Uni/Fachhochschule/TU"] == x]["Uni Name"].unique())
    )

    fig = px.bar(
        institutes,
        x="Uni/Fachhochschule/TU",
        y="Amount_Institute_Type",
        hover_data=["Names"],
        color="Uni/Fachhochschule/TU",
        color_discrete_sequence=['black', 'red', 'yellow']
    )

    fig.update_layout(
        xaxis_title="Institute type",
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
        hover_data=["Course Name"]
    )

    if show_plot:
        fig.show()

    return fig


def plot_popular_courses(data, show_plot):
    # todo: Fill with code
    return None