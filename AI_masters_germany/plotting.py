import plotly.express as px


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
        color='Cluster',
        title='Course clustering result',
        hover_data=['Course Name']
    )

    if show_plot:
        fig.show()

    return fig


def plot_popular_courses(data, show_plot):
    # todo: Fill with code
    return None