# Tony Bui
# Software Engineering Intern at Quantium Virtual Experience Program

import pandas as pd
import glob
import re
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

candy_type = "pink morsel"
csv_files = glob.glob("data/*.csv")
output_file_path = "data/all_data.csv"
new_header = "sales,date,region\n"

# Data Processing
with open(output_file_path, "w") as all_data_file:
    all_data_file.write(new_header)
    for file_name in csv_files:
        with open(file_name, 'r') as file:
            header = file.readline().strip().split(',')
            for line in file:
                product,price ,quantity ,date, region = line.strip().split(',')
                if product == candy_type:
                    quantity = int(quantity)
                    price = float(re.sub(r'\$', '', price))
                    sales = quantity * price
                    all_data_file.write(f"{sales},{date},{region}\n")
                
# Data Visualization
app = dash.Dash(__name__)
df = pd.read_csv(output_file_path)
df['date'] = pd.to_datetime(df['date'])
df_sorted = df.sort_values('date')

regions = ['all'] + list(df['region'].unique())

app.layout = html.Div([
    html.H1("Sales Data Visualizer", style={'textAlign': 'center'}),
    
    dcc.Graph(id='sales-line-chart'),
    
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in regions],
        value='all',
        style={'width': '50%'}
    ),

    html.Img(src="/assets/pink_morsel.jpg", style={'width': '15%', 'display': 'flex', 'margin-left': 'auto'})
])

@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('region-dropdown', 'value')]
)

def update_graph(selected_region):
    if selected_region == 'all':
       fig = px.line(df_sorted, x='date', y='sales', title=f"Pink Morsel Sales Over Time for {selected_region} Region",
                  labels={'date': 'Date', 'sales': 'Sales'},
                  line_shape='linear')
    else:
        df_filtered = df_sorted[df_sorted['region'] == selected_region]

        fig = px.line(df_filtered, x='date', y='sales', title=f"Pink Morsel Sales Over Time for {selected_region} Region",
                    labels={'date': 'Date', 'sales': 'Sales'},
                    line_shape='linear')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)