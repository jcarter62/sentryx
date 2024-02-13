import plotly.express as px
import pandas as pd

class Plotting:
    def __init__(self):
        pass

    def plot_readings(self, id, data, dest):
        dest_file = dest + '/' + id + '.html'
        # convert metered to numeric
        for d in data:
            d['metered'] = pd.to_numeric(d['metered'])
        # fig = px.line(data, x='yearmonth', y='metered')
        fig = px.bar(data, x='yearmonth', y='metered', title='Meter Readings for ' + id, labels={'metered': 'ACFT', 'yearmonth': 'Month'})
        fig.write_html(dest_file)
        # return the relative path to the file
        rel_path = '/static' + dest_file.split('static')[1]
        return rel_path
