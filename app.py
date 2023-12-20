import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask import Flask
from flask import request
import dash_auth

VALID_USERNAME_PASSWORD_PAIRS = {"admin": "rwp123", "RSU": "lsu2023"}
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc_css])

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server
pages = [
     {"name": "PhoneBook DashBoard", "path":"/"}, 
    {"name": "RSU-PhoneBook", "path":"/contact-info"},
    {"name": "LSU Data Entry Form", "path":"/lsu-data-entry"},
    # {"name": "PhoneBook DashBoard", "path":"/statitical-info"},    
    {"name": "WCD Event Status", "path":"/wcdevent"},
]
lsupages = [
    {"name": "PhoneBook DashBoard", "path":"/"},  
    {"name": "LSU-PhoneBook", "path":"/lsu-contct-info"},
    {"name": "LSU Data Entry Form", "path":"/lsu-data-entry"},
    # {"name": "OOSC Event Status", "path":"/statitical-info"},    
    # {"name": "WCD Event Status", "path":"/wcdevent"},
]
img = html.Img(src="assets\images\logo.jpg", height="80px")
lsusidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in lsupages
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in pages
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dcc.Store(id="store", data={}),
                dbc.Col(html.Div(img), width=1),
                dbc.Col(
                    html.Div(
                        "Reform Support Unit-Digital Directory",
                    ),
                    style={"padding": "0.1rem", "fontSize": 50, "textAlign": "center"},
                    width=11,
                ),
            ]
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [  
                dbc.Col(
                    [
                        # sidebar,
                        dcc.Location(id="url", refresh=False),
                        html.Div(id="pages"),
                    ],
                    xs=2,
                    sm=2,
                    md=2,
                    lg=2,
                    xl=2,
                    xxl=2,
                ),
                dbc.Col(
                    [
                      
                        #html.Div(id="page-content"),
                        dash.page_container,
                    ],
                    xs=10,
                    sm=10,
                    md=10,
                    lg=10,
                    xl=10,
                    xxl=10,
                ),
            ]
        ),
    ],
    fluid=True,
)

# Callback to determine which pages are accessible based on the logged-in user
@app.callback(
    Output("pages", "children"),
    [Input("url", "pathname")],
    prevent_initial_call=True,
)
def display_page(pathname):
    # Check the role of the logged-in user
    # authorization_header = request.headers.get("Authorization")
    # print(authorization_header)
    
    # accessible_pages = []
    # username = request.authorization['username']
    password =request.authorization['password']
    # print(user_role)
    if auth.is_authorized() and password=='rwp123':
        accessible_pages = pages
        return sidebar
    #     return [
    #     dbc.NavLink(
    #         [
    #             html.Div(page["name"], className="ms-2"),
    #         ],
    #         href=page["path"],
    #         active="exact",
    #     )
    #     for page in accessible_pages
    # ]
    elif auth.is_authorized() and password=='lsu2023':
        accessible_pages = [page for page in lsupages if page["name"] =="LSU Data Entry Form"]
        return lsusidebar
        # print(accessible_pages)
        # return [
        # dbc.NavLink(
        #     [
        #         html.Div(page["name"], className="ms-2"),
        #     ],
        #     href=page["path"],
        #     active="exact",
        # )
        # for page in accessible_pages
        #      ]
    else:
        accessible_pages = []
    return sidebar

    # return [
    #     dbc.NavLink(
    #         [
    #             html.Div(page["name"], className="ms-2"),
    #         ],
    #         href=page["path"],
    #         active="exact",
    #          vertical=True,
    #         pills=True,
    #         className="bg-light",
    #     )
    #     for page in accessible_pages
    # ]


# Define callback to update page content
# @app.callback(
#     Output("page-content", "children"),
#     [Input("url", "pathname")],
# )
# def display_page_content(pathname):
#     # You can customize this function to load the content of each page dynamically
    
#     return html.Div(f"Content for {pathname}")


if __name__ == "__main__":
    app.run_server(debug=True, port=8000)
