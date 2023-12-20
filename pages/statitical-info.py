import dash
import dash_bootstrap_components as dbc
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
#dash.register_page(__name__)
from dash import Dash, dcc, html, Input, Output, callback,dash_table
import plotly.express as px
import pandas as pd

# df = pd.read_csv('data\OOSC Conference participants.csv')
# Types = df.Type.unique()
df = pd.read_csv('data\WCD participants list confirmation.csv')
Types = df.Type.unique()
confimby=df.ConfirmedBy.unique()
emails=df.groupby('Type')[['Email Address']].count().reset_index()
current=df.groupby('Type')[['Email Address','Contact No']].count().sort_values(by='Email Address',ascending=False).reset_index()
dept=df.groupby('Type')['Department'].count().sort_values(ascending=False).reset_index()
#wcdstatus2 = df.Status.value_counts().reset_index()
wcdstatus2=df.groupby('ConfirmedBy')['Status'].value_counts().unstack().reset_index()
# days = df.day.unique()
#fig = px.bar(current, x='Type', y='Contact No', barmode="group") #, barmode="group"
fig2=px.bar(dept, x='Type', y='Department', barmode="group")
dash.register_page(__name__, path="/",name='PhoneBook DashBoard', external_stylesheets=[dbc.themes.SPACELAB])
layout = html.Div([

                dbc.Container(
                    [
                    
                        dbc.Row(
                            [
                                dbc.Col(


                        [
                            html.H4("RSU Digital Directory Dashboard Info:"),
                            dash_table.DataTable(id='ooscdatatable-output', data=current.to_dict('records'),
                                                    columns=[{'id': c, 'name': c} for c in current.columns],
                                                    page_action='native',   # all data is passed to the table up-front
                                                    #page_size=10,           # only 10 rows are displayed at a time
                                                    
                                                    fixed_rows={'headers':True},
                                                  style_table={'height': '200px', 'overflowY': 'auto'},
                                                    style_cell={'color':'dark', 'text-align':'left','width':'200px'},
                                                    
                                                    ),]),
                 dbc.Col(


               
                        [   
                            html.Br(),
                            html.Hr(),
                            dcc.Graph(id="SCbar-chart", figure=fig2),
                html.H4("WCD-World Childrens' Day Event: Participnt's Summary "),
        dash_table.DataTable(id='status-output2',data=wcdstatus2.to_dict('records'),
                                columns=[{'id': d, 'name': d} for d in wcdstatus2.columns],
                                page_action='native',   # all data is passed to the table up-front
                                page_size=10,           # only 10 rows are displayed at a time
                                
                                style_table={'height': '200px', 'overflowY': 'auto'},
                                style_cell={'color':'dark', 'text-align':'left','width':'2px'},
                                
                                ),]),


        # dcc.Dropdown(
        #     id="ooscdropdown",
        #     options=[{"label": x, "value": x} for x in Types],
        #     #value=Types[0],
        #     clearable=False,
        #     disabled=False,
        #     style={"width": "50%"}
            
        # ),
        
        #dcc.Graph(id="SCbar-chart", figure=fig2),
                       


                           
                    
    
        ], style={'border': '1px solid #ccc', 'padding': '20px', 'background-color': '#f2f2f2', 'position': 'relative','display':' -ms-flexbox'},
                                           ),
    ]),
])


# @callback(
#         #    Output('ooscdatatable-output', 'data'),
#         #    Output('ooscdatatable-output', 'columns'),
#            Output("SCbar-chart", "figure"),
#            Input("ooscdropdown", "value"),
#            allow_duplicate=True,
#            prevent_initial_call=True,

#            )

# def update_bar_chart(tt):
#     #print(tt)
#     mask = current['Type'] == tt
#    # print(current[mask])
#     fig = px.bar(current[mask], x='Type', y='Status', barmode="group") #, barmode="group"
#     return fig
 