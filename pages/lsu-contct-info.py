import dash
from dash import dcc, html, callback, Output, Input,dash_table,State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd


dash.register_page(__name__, name='LSU-PhoneBook', external_stylesheets=[dbc.themes.SPACELAB]) 

# Keep this out of source code repository - save in a file or a database

#app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


#dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

# (all code is from https://dash.plotly.com/datatable/height)

# app = dash.Dash(__name__)

#-----------------------------------------------------------------------------
df= pd.read_csv('data\contacts.csv')
total = html.Div(id="total", style={"textAlign": "left"})
# 
#-----------------------------------------------------------------------------

layout = html.Div([
    
    html.Div("Digital Directory: you can make a copy here:"),
    dcc.Clipboard(id="lsuclip", style={"fontSize": 20}),
    
    dash_table.DataTable(id="table",
                          
                                data=df.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in df.columns],
                      
                    #-----------------------------------------------------------------------------
# Vertical Scroll (without Pagination)
#-----------------------------------------------------------------------------
    page_size=10,
    page_action='none',     # render all of the data at once
    row_selectable="single",
    row_deletable=True,
    editable=True,
    

    filter_action="native",
    sort_action="native",
    #style_table={ 'overflowY': 'auto',"overflowX": "auto"},#'height': '600px',
    style_table={"overflowX": "auto"},
    fixed_rows={'headers': True},
    style_cell={'color':'dark', 'text-align':'left'},        
    
    # If you have more than 1000 rows, your browswer will slow down. Therefore,
    # for over 1000 rows, use pagination as per examples below or virtualization
    # as per last example.

#-----------------------------------------------------------------------------
# Fronent Pagination with Vertical Scroll
#-----------------------------------------------------------------------------
    # page_action='native',   # all data is passed to the table up-front
    # page_size=10,           # only 10 rows are displayed at a time
    # style_table={'height': '200px', 'overflowY': 'auto'}

#-----------------------------------------------------------------------------
# Fronent Pagination without Vertical Scroll
#-----------------------------------------------------------------------------
    # page_action='native',     # all data is passed to the table up-front
    # page_size=10,             # but only 10 rows are displayed at a time

    # If you have over 10,000 rows you should do pagination in the backend
    # to lower network costs and memory. See how with link below:
    # https://dash.plotly.com/datatable/ callbacks

#-----------------------------------------------------------------------------
# Vertical Scroll With Fixed Headers
#-----------------------------------------------------------------------------
    # fixed_rows={'headers': True},
    # style_table={'height': 400}  # defaults to 500

    # By default and without wrapping, each row takes up 30px. So 10 rows with
    # one header would set the table to be 330px tall.
    # Since here we have 18 rows+header, that would equal 570px.

#-----------------------------------------------------------------------------
# Width of Headers (partial text)
#-----------------------------------------------------------------------------

    # If the headers are wider than the cells and the table's container isn't wide
    # enough to display all of the headers, then the column headers will be truncated

    # data=df_numeric.to_dict('records'),
    # columns=[{'id': c, 'name': c} for c in df_numeric.columns],

    # fixed_rows={'headers': True}

#-----------------------------------------------------------------------------
# Width of Headers (full text)
#-----------------------------------------------------------------------------
    # fixed_rows={'headers': True},
    # style_cell={
    #     'minWidth': 95, 'maxWidth': 95, 'width': 95
    # }

#-----------------------------------------------------------------------------
# Vertical Scroll with Virtualization
#-----------------------------------------------------------------------------
    # virtualization=True,            # to use when you have over 1000 rows
    # fixed_rows={'headers': True},
    # style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95}, #set width when using virtualization
    # style_table={'height': 300}     # default is 500px

#----------------------------------------------------------------
),
])
@callback(
    Output("lsuclip", "content"),
    Input("lsuclip", "n_clicks"),
    Input("store", "data"),
    State("table", "data"),
    prevent_initial_call=True,
    allow_duplicate=True
    )
    
def custom_copy(n_clicks,content, data):
    dff = pd.DataFrame(data)
    return dff.to_csv(index=False)  # do not include row names
# if __name__ == '__main__':
#     app.run_server(debug=True)
