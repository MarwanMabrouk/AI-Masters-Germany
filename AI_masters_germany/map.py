import plotly.express as px
import pandas as pd


def get_map(database):
    # Create scatter map
    fig = px.scatter_geo(database, lat='Latitude', lon='Longitude',
                        hover_name='Uni Name', #size='mag',
                        title='Geographical distribution of universities in Germany',
                        center=dict(lat=51.0057, lon=13.7274),
                        scope='europe')

    fig.update_layout(
        autosize=True,
        height=600,
        geo=dict(
            center=dict(
                lat=51.0057,
                lon=13.7274
            ),
            scope='europe',
            projection_scale=6
        )
    )

    return fig