import dash
from dash import dcc, html, callback, Output, Input,dash_table,State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from clipboard import copy


dash.register_page(__name__, name='RSU-PhoneBook', external_stylesheets=[dbc.themes.SPACELAB]) 

#-----------------------------------------------------------------------------
df= pd.read_csv('data\WCD participants list confirmation.csv')
total = html.Div(id="total", style={"textAlign": "right"})
# 
#-----------------------------------------------------------------------------

layout =  dbc.Container([
        
    dbc.Row([
           dbc.Col([dcc.Clipboard(id="clip", style={"fontSize": 20}),
             html.Div(id='output-container',children=["Digital Directory: you can make a copy here:"]),
            ],width=6),
            
            
            # dbc.Col([
            #     dcc.Clipboard(id="clip", style={"fontSize": 20}),
                # html.Div("Digital Directory: you can make a copy here:"),
            #  ],width=6),
                             
            ]),
            html.Hr(),

    dbc.Row([
            
            
            dbc.Col([
                dcc.Input(id='search-input', type='text', placeholder='Enter search criteria'),
                dash_table.DataTable(id="table",
                          
                                data=df.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in df.columns],
                      
                    #-----------------------------------------------------------------------------
# Vertical Scroll (without Pagination)
#-----------------------------------------------------------------------------
    page_size=10,
    page_action='none',     # render all of the data at once
    row_selectable="multi",
    row_deletable=False,
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
    # https://dash.plotly.com/datatable/callbacks

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
),]),
])
])
@callback(
    # [Output("clip", "content"),
    Output("output-container", "children"),
   
    [Input("clip", "n_clicks"),
    Input("store", "data")],
    [State("table", "data"),
     State("table", "selected_rows")],
    prevent_initial_call=True,
    allow_duplicate=True
    ) 
def custom_copy(n_clicks, content, data, selected_rows):
    if not selected_rows:
        dff = pd.DataFrame(data)
        copy(dff.to_csv(index=False))
        
        return "No rows selected, All data copied in clipboard."

    text_values=''
    for row in selected_rows:
            selected_data = data[row]
            for value in selected_data.values():
                    text_values += f"{value}\n" 


    
            #    print(text_values)         


    # print(type(text_values)) 
   
    
    
       
    # Extract data for the selected rows
    selected_data = [data[row] for row in selected_rows]
    
        
    #   selected_data = [f"{key}: {value}" for key, value in selected_rows.items()]

    # # Format and copy selected data
    # selected_data_str = "\n".join([str(row) for row in selected_data])
    
    # print(selected_data_str)
    # text_representation = ""
    # for entry in selected_data:
    #     text_representation = ""
    # for key, value in entry():
    #     text_representation += f"{key}: {value}\n"
   
    # text_representation= "\n".join([f"{key}: {value}" for key, value in selected_data.items()])
    
    try:
        copy(text_values)
        return f"Selected {len(selected_data)} rows copied to clipboard."
    except Exception as e:
        return f"Error copying data: {e}"

   
# def custom_copy(n_clicks,content, data, selected_rows ):
#      if not selected_rows:
            
#             dff = pd.DataFrame(data)
#             copy(dff.to_csv(index=False)) # do not include row names
#             return "No rows selected, All data copied in clipboard."
#        # do not include row names
#            # return "No rows selected, All data copied in clipboard."
   
#      else:
#             # Extract data for the select   ed rows
#             # selected_data = [data[row] for row in selected_rows]
#             selected_data=[f"{key}: {value}" for key, value in selected_rows.items()]
#     # Format the selected data as a string
#             selected_data_str = "\n".join(str(row) for row in selected_data)
#             # Create a string representation of dictionary values
#             text_representation = "\n".format([f"{key}: {value}" for key, value in selected_data_str.items()])


#     # Copy to clipboard
#             copy(text_representation )

#             return f"Selected {len(selected_rows)} rows copied to clipboard."
       


@callback(
    Output('table', 'data'),
    [Input('search-input', 'value')],
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_table(search_input):
    if not search_input:
        return df.to_dict('records')  # If search input is empty, display all data
    else:
        # Filter the DataFrame based on the search criteria
        filtered_df = df[df.apply(lambda row: any(search_input.lower() in str(cell).lower() for cell in row), axis=1)]

        return filtered_df.to_dict('records')

# if __name__ == '__main__':
#     app.run_server(debug=True)
