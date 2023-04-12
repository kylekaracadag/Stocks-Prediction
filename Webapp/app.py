from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import *


app = Dash(__name__)

# This pulls the csv file straight from github so everyone can use it
data = pd.read_csv('https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Webapp/CompanyList.csv')
data2 = pd.read_csv('https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Webapp/Prediction.csv')
# layout for the divs
app.layout = html.Div([
    #title 
    html.H4('Stocks Prediction Data Visualization', id="H4", className="H4"),
    html.P("Line Graphs", id="H3", className="des"),
    dcc.Dropdown(
                id='file',
                className="dropdown",
                options = data['.csv File'].unique(),
                value = 'A_data.csv'# starting selection not needed but good to have
                ,style={'color': 'blue', 'backgroundColor': 'white'} 
            ),
    dcc.RadioItems(
        id='hovermode',
        className="hovermode",
        inline=True,
        options=['x', 'x unified', 'closest'], 
        value='x' # what the starting selection will be
    ),
    dcc.RadioItems(
        id ='Data',
        className="hovermode",
        inline =True,
        options =['Close', 'Open', 'High'],
        value ='Close'# what the starting selection will be
    ),

    dcc.Graph(id="graph", className="Graph1"),# What shows our graph grabs the output from our callback output
    
    dcc.Dropdown(
            options = data2['.csv'].unique(),
            value ='3-13-2023_Altered_Predictions.csv',# starting selection not needed but good to have
            id ='file1',
            style={'color': 'black'},
        ),
    dcc.RadioItems(
        id='hovermode1',
        className="hovermode",
        inline=True,
        options=['x', 'x unified', 'closest'], 
        value='x' # what the starting selection will be
    ),
    dcc.RadioItems(
            id='Data1',
            className="hovermode",
            inline=True,
            options=['Close', 'Open', 'High'],
            value='Close'# what the starting selection will be
            ),
             
        
    dcc.Graph(id="graph2"),  
    html.H4('', id="spacer", className="spacer"),
    html.H4('Candle Sticks: ', className="candle", id="candle"),
    dcc.Dropdown(
        id='compare1',
        className="dropdown",
        options = data['.csv File'].unique(),
        value = 'A_data.csv',# starting selection not needed but good to have
        style={'color': 'black'},
    ),
    dcc.Checklist(
        id='toggle-rangeslider',
        className="hovermode",
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
 
    dcc.Graph(id="graph1"),# shows actual candle sticks 
    
    dcc.Dropdown(
        data2['.csv'].unique(),
        value= '3-13-2023_Altered_Predictions.csv',# starting selection not needed but good to have
        id='candlestick_predictions',
        style={'color': 'black'},
    ),
     dcc.Checklist(
        id='toggle-rangeslider1',
        className="hovermode",
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph3"),# shows actual candle sticks 
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
    # df1 = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Datasets/" + compare1)

    fig = px.scatter(
        df, x="Date", y=mode1, 
        title= file + " " +  mode1 + " price",
        render_mode='svg')
    #fig.add_scatter(x=df1, y=mode1)
    fig.update_traces(
        mode="lines", hovertemplate=None)
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]) , # hide weekends
            dict(bounds=[16, 9.5], pattern="hour"), #hide hours outside of 9am-5pm
        ]
    )
        
    

     
    fig.update_layout(
        hovermode=mode,
        paper_bgcolor="#313338", plot_bgcolor="#313338",
        font_color="white",
        title_font_color="white",
        legend_title_font_color="white"
    )

    return fig
#--------------------------------------------------------

#For Candle sticks 
@app.callback(
    Output("graph1", "figure"), 
    Input("compare1","value"),
    Input("toggle-rangeslider", "value"))
def update_Graph(file,value):

    # This now allows anyone to use the site without changing the path to the file 
    df = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Datasets/" + file)
    
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open = df["Open"],
            high = df["High"],
            low = df["Low"],
            close = df["Close"]
        )
    )

    fig.update_yaxes(fixedrange=False)
    fig.update_layout(xaxis_rangeslider_visible = False, title = 'MSFT SHARE PRICE')
    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = 'MSFT Close Price', tickprefix = '$')
    fig.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            dict(bounds=["sat", "mon"]), #hide weekends
            dict(bounds=[16, 9.5], pattern="hour"), #hide hours outside of 9am-5pm
        ]
    )
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value,
        paper_bgcolor="#313338", plot_bgcolor="#313338",
        font_color="white",
        title_font_color="white",
        legend_title_font_color="white"
    )
    return fig


@app.callback(
    Output("graph3", "figure"), 
    Input("candlestick_predictions","value"),
    Input("toggle-rangeslider1", "value"))
def update_Graph(file,value):

    fig = go.Figure()
    # This now allows anyone to use the site without changing the path to the file 
    df = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Predictions/" + file)
    
   
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open = df["Open"],
            high = df["High"],
            low = df["Low"],
            close = df["Close"]
        )
    )

    fig.update_yaxes(fixedrange=False)
    fig.update_layout(xaxis_rangeslider_visible = False, title = 'MSFT SHARE PRICE')
    fig.update_xaxes(title_text = 'Date')
    fig.update_yaxes(title_text = 'MSFT Close Price', tickprefix = '$')
    fig.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            dict(bounds=["sat", "mon"]), #hide weekends
            dict(bounds=[16, 9.5], pattern="hour"), #hide hours outside of 9am-5pm
        ]
    )
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value,
        paper_bgcolor="#313338", plot_bgcolor="#313338",
        font_color="white",
        title_font_color="white",
        legend_title_font_color="white"
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
    df = pd.read_csv("https://raw.githubusercontent.com/kylekaracadag/Stocks-Prediction/main/Predictions/" + file)
 
    fig = px.scatter(
        df, x="Date", y=mode1, 
        title= file + " " +  mode1 + " price", render_mode='svg')
    fig.update_traces(
        mode="lines", hovertemplate=None)
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]) , # hide weekends
            dict(bounds=[16, 9.5], pattern="hour"), #hide hours outside of 9am-5pm
        ]
    )
    fig.update_layout(
         hovermode=mode,
        paper_bgcolor="#313338", plot_bgcolor="#313338",
        font_color="white",
        title_font_color="white",
        legend_title_font_color="white"
    )
    return fig

app.run_server(debug=True)