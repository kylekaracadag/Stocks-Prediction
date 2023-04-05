from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import *


app = Dash(__name__)

# will be changed later just for testing am pulling file like so, will prbably change to pulling straight from the git to make work for everyone
data = pd.read_csv('https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Webapp/CompanyList.csv')
data2 = pd.read_csv('https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Webapp/Prediction.csv')
# layout for the divs
app.layout = html.Div([
    #title 
    html.H4('Ai club Stocks predictor website', id="H4"),
    html.P("Premade Graphs", id="H3", className="des"),
    dcc.Dropdown(
                id='file',
                className="dropdown",
                options = data['.csv File'].unique(),
                value = 'A_data.csv'# starting selection not needed but good to have
            ),
            html.H4('Graph to compare to: '),
            dcc.Dropdown(
                id='compare1',
                className="dropdown",
                options = data['.csv File'].unique(),
                value = 'A_data.csv'# starting selection not needed but good to have
            ),
    dcc.RadioItems(
        id='hovermode',
        className="hovermode",
        inline=True,
        options=['x', 'x unified', 'closest'], 
        value='x' # what the starting selection will be
    ),
    dcc.RadioItems(
        id='Data',
        inline=True,
        options=['Close', 'Open', 'High'],
        value='Close'# what the starting selection will be
    ),

    dcc.Graph(id="graph", className="Graph1"),# What shows our graph grabs the output from our callback output
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph1"),# shows actual candle sticks 
    html.H3(
         dcc.Dropdown(
            data2['.csv'].unique(),
            'Altered Predictions.csv',# starting selection not needed but good to have
            id='file1'
        ),
    ),
   
    dcc.RadioItems(
        id='hovermode1',
        inline=True,
        options=['x', 'x unified', 'closest'], 
        value='x' # what the starting selection will be
    ),
    dcc.RadioItems(
            id='Data1',
            inline=True,
            options=['Close', 'Open', 'High'],
            value='Close'# what the starting selection will be
            ),
    dcc.Graph(id="graph2")
])      
                       

# for Acutal Data graphs
@app.callback(
    Output("graph", "figure"), 
    Input("hovermode","value"),
    Input("Data","value"),
    Input("file","value"),
    Input("compare1", "value"))

def update_Graph(mode,mode1,file,compare1):
 

    # This now allows anyone to use the site without changing the path to the file 
    df = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Datasets/" + file)
    df1 = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Datasets/" + compare1)

    fig = px.scatter(
        df, x="Date", y=mode1, 
        title= file + " " +  mode1 + " price")
    fig.add_scatter(x=df1, y=mode1)
    fig.update_traces(
        mode="lines", hovertemplate=None)
    fig.update_layout(hovermode=mode,paper_bgcolor="lightslategray", plot_bgcolor="lightslategray")

    return fig
#--------------------------------------------------------

#For Candle sticks 
@app.callback(
    Output("graph1", "figure"), 
    Input("file","value"),
    Input("toggle-rangeslider", "value"))
def update_Graph(file,value):

    # This now allows anyone to use the site without changing the path to the file 
    df = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Datasets/" + file)
    
    fig = go.Figure(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    ))
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value,
        paper_bgcolor="lightslategray", plot_bgcolor="lightslategray"
    )
    return fig

#------------------------------------
@app.callback(
    Output("graph2", "figure"), 
    Input("hovermode1","value"),
    Input("Data1","value"),
    Input("file1","value"))

def update_Graph(mode,mode1,file):

    # This now allows anyone to use the site without changing the path to the file 
    df = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Predictions/Old%20Predictions/" + file)
    
    fig = px.scatter(
        df, x="Unnamed: 0", y=mode1, 
        title= file + " " +  mode1 + " price")
    fig.update_traces(
        mode="lines", hovertemplate=None)
    fig.update_layout(hovermode=mode,paper_bgcolor="lightslategray", plot_bgcolor="lightslategray")
    return fig
  

app.run_server(debug=True)