import dash
import json
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from src.main.service.DataAccessService import DataAccessService
from src.main.service.Dockerise import Dockerise
from src.resources.config import DATABASE_CONFIG
from random import randint
import re
import shutil

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.supress_callback_exceptions = True

app.layout = html.Div([
    html.Div([
        html.H3('Select Database Server', style={'margin': '20px'}),
        dcc.Dropdown(
            id='select_db',
            options=[
                {'label': 'Please Select', 'value': ''},
                {'label': 'My SQL', 'value': 'mysql+pymysql'},
                {'label': 'Sql Server', 'value': 'sqlserver'},
                {'label': 'Postgres', 'value': 'postgres'}
            ],
            value=''
        ),
    ], style={'columnCount': 1}),

    html.Div(
        [
            html.Label('DB Connection details'),
            html.Div(
                dcc.Input(
                    type='text',
                    placeholder='Host Name',
                    id='host',
                    style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'margin-top': '10px'},
                )
            ),
            html.Div(
                dcc.Input(
                    type='text',
                    placeholder='Port',
                    id='port',
                    style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'margin-top': '10px'},
                )
            ),
            html.Div(
                dcc.Input(
                    type='text',
                    placeholder='User Name',
                    id='username',
                    style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'margin-top': '10px'},
                )
            ),
            html.Div(
                dcc.Input(
                    type='password',
                    placeholder='Password',
                    id='password',
                    style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'margin-top': '10px'},
                )
            ),
            html.Div(
                dcc.Input(
                    type='text',
                    placeholder='DB Name',
                    id='db_name',
                    style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '30%', 'margin-top': '10px'},
                )
            ),
            html.Div(
                [
                    html.A(
                        html.Button(
                            id='submit',
                            children='Submit',
                            style={
                                'display': 'inline-block',
                                'verticalAlign': 'top',
                                'width': '20%',
                                'margin-top': '30px'
                            }
                        )
                    )
                ]),
            html.Div(
                id='table_names', style={'columnCount': 1}, children="",
            ),
            html.Div(
                id='column_names', style={'columnCount': 1}, children="",
            ),
            html.Div(
                id='records', style={'columnCount': 1}, children="",
            ),
            html.Div(
                id='query_result', style={'columnCount': 1}, children="",
            ),
            html.Div(
                id='api_response', style={'columnCount': 1}, children="",
            ),
        ], id='db_details', style={'display': 'none'})
    ])


@app.callback(
   Output(component_id='db_details', component_property='style'),
   [Input(component_id='select_db', component_property='value')])
def select_db(selected_value):

    if selected_value == 'mysql+pymysql':
        return {'display': 'block', 'padding-top': '50px'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('table_names', 'children'),
    [
     Input('submit', 'n_clicks')],
    [
        State('host', 'value'),
        State('port', 'value'),
        State('username', 'value'),
        State('password', 'value'),
        State('db_name', 'value'),
        State('select_db', 'value')
    ]
)
def connect(n_clicks, host, port, username, password, db_name, select_db):
    if n_clicks is not None:
        try:
            DATABASE_CONFIG["DB_USER"] = username
            DATABASE_CONFIG["DB_PWD"] = password
            DATABASE_CONFIG["DB_HOST"] = host
            DATABASE_CONFIG["DB_PORT"] = port
            DATABASE_CONFIG['DB_NAME'] = db_name
            DATABASE_CONFIG['DIALECT_DRIVER'] = select_db
            data_access_service = DataAccessService()
            rows = json.loads(data_access_service.get_tables())
            return html.Div([
                html.Label('Tables'),
                dcc.RadioItems(
                    id='table',
                    options=[{'label': i, 'value': i} for i in rows],
                    value='Total',
                    labelStyle={'display': 'inline-block'}
                ),
                html.Div(
                    [
                        html.A(
                            html.Button(
                                id='select_table',
                                children='Select Table',
                                style={
                                    'display': 'inline-block',
                                    'verticalAlign': 'top',
                                    'width': '20%',
                                    'margin-top': '30px'
                                }
                            )
                        )
                    ]),
                html.Label('Or Write a Query', style={'margin-top': '30px'}),
                dcc.Input(
                    type='text',
                    placeholder='Query',
                    id='query',
                    style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '80%', 'margin-top': '10px'},
                ),
                html.Div(
                    [
                        html.A(
                            html.Button(
                                id='execute_query',
                                children='Execute Query',
                                style={
                                    'display': 'inline-block',
                                    'verticalAlign': 'top',
                                    'width': '20%',
                                    'margin-top': '30px'
                                }
                            )
                        )
                    ])
            ], style={'margin-top': '20px'})
        except Exception as error:
            print(error)
            return "Not able to connect, connection parameters are wrong, Cause:"+str(error)


@app.callback(
    Output('column_names', 'children'),
    [
     Input('select_table', 'n_clicks')],
    [
        State('host', 'value'),
        State('port', 'value'),
        State('username', 'value'),
        State('password', 'value'),
        State('db_name', 'value'),
        State('select_db', 'value'),
        State('table', 'value')
    ]
)
def fetch_columns(n_clicks, host, port, username, password, db_name, select_db, table):
    if n_clicks is not None:
        try:
            DATABASE_CONFIG["DB_USER"] = username
            DATABASE_CONFIG["DB_PWD"] = password
            DATABASE_CONFIG["DB_HOST"] = host
            DATABASE_CONFIG["DB_PORT"] = port
            DATABASE_CONFIG['DB_NAME'] = db_name
            DATABASE_CONFIG['DIALECT_DRIVER'] = select_db
            DATABASE_CONFIG['TABLE_NAME'] = table
            data_access_service = DataAccessService()
            rows = data_access_service.get_columns()
            print(rows)
            return html.Div([
                html.Label('Columns'),
                dcc.Dropdown(
                    id='column_names',
                    options=[{'label': i, 'value': i} for i in rows],
                    multi=True
                ),
                html.Div(
                    [
                        html.A(
                            html.Button(
                                id='select_columns',
                                children='Select Columns',
                                style={
                                    'display': 'inline-block',
                                    'verticalAlign': 'top',
                                    'width': '20%',
                                    'margin-top': '30px'
                                }
                            )
                        )
                    ]),
            ], style={'margin-top': '20px'})
        except Exception as error:
            print(error)
            return "Not able to connect, connection parameters are wrong, Cause:"+str(error)


@app.callback(
    Output('records', 'children'),
    [
     Input('select_columns', 'n_clicks')],
    [
        State('host', 'value'),
        State('port', 'value'),
        State('username', 'value'),
        State('password', 'value'),
        State('db_name', 'value'),
        State('select_db', 'value'),
        State('table', 'value'),
        State('column_names', 'value')
    ]
)
def fetch_records(n_clicks, host, port, username, password, db_name, select_db, table, columns):

    if n_clicks is not None:
        try:
            DATABASE_CONFIG["DB_USER"] = username
            DATABASE_CONFIG["DB_PWD"] = password
            DATABASE_CONFIG["DB_HOST"] = host
            DATABASE_CONFIG["DB_PORT"] = port
            DATABASE_CONFIG['DB_NAME'] = db_name
            DATABASE_CONFIG['DIALECT_DRIVER'] = select_db
            DATABASE_CONFIG['TABLE_NAME'] = table
            data_access_service = DataAccessService()
            rows = data_access_service.get_data_records(columns)
            print(rows)
            return html.Div([
                html.Div([
                    html.P(rows),
                    html.Div(
                        [
                            html.A(
                                html.Button(
                                    id='expose_api',
                                    children='Expose API',
                                    style={
                                        'display': 'inline-block',
                                        'verticalAlign': 'top',
                                        'width': '20%',
                                        'margin-top': '30px'
                                    }
                                )
                            )
                        ])
                ]),
            ], style={'margin-top': '20px'})
        except Exception as error:
            print(error)
            return "Not able to connect, connection parameters are wrong, Cause:"+str(error)


@app.callback(
    Output('query_result', 'children'),
    [
     Input('execute_query', 'n_clicks')],
    [
        State('host', 'value'),
        State('port', 'value'),
        State('username', 'value'),
        State('password', 'value'),
        State('db_name', 'value'),
        State('select_db', 'value'),
        State('table', 'value'),
        State('query', 'value')
    ]
)
def execute_query(n_clicks, host, port, username, password, db_name, select_db, table, query):
    if n_clicks is not None:
        try:
            DATABASE_CONFIG["DB_USER"] = username
            DATABASE_CONFIG["DB_PWD"] = password
            DATABASE_CONFIG["DB_HOST"] = host
            DATABASE_CONFIG["DB_PORT"] = port
            DATABASE_CONFIG['DB_NAME'] = db_name
            DATABASE_CONFIG['DIALECT_DRIVER'] = select_db
            DATABASE_CONFIG['TABLE_NAME'] = table
            data_access_service = DataAccessService()
            rows = data_access_service.get_queried_results(query)
            return html.Div([
                html.Div([
                    html.P(rows),
                    html.Div(
                        html.A(
                            html.Button(
                                id='expose_api',
                                children='Expose API',
                                style={
                                    'display': 'inline-block',
                                    'verticalAlign': 'top',
                                    'width': '20%',
                                    'margin-top': '30px'
                                }
                            )
                        )
                    )
                ]),
            ], style={'margin-top': '20px'})
        except Exception as error:
            print(error)
            return "Not able to connect, connection parameters are wrong, Cause:"+str(error)


@app.callback(
    Output('api_response', 'children'),
    [
     Input('expose_api', 'n_clicks')],
    [
        State('host', 'value'),
        State('port', 'value'),
        State('username', 'value'),
        State('password', 'value'),
        State('db_name', 'value'),
        State('select_db', 'value'),
        State('table', 'value'),
        State('query', 'value')
    ]
)
def expose_api(n_clicks, host, port, username, password, db_name, select_db, table, query):
    if n_clicks is not None:
        try:
            shutil.copyfile("config.py", "../../docker/config.py")

            with open('../../docker/config.py', 'r') as f:
                content = f.read()
            with open('../../docker/config.py', 'w') as f:
                content = re.sub("<DB_HOST>", host, content, flags=re.M)
                content = re.sub("<DB_PORT>", str(port), content, flags=re.M)
                content = re.sub("<DB_USER>", username, content, flags=re.M)
                content = re.sub("<DB_PWD>", password, content, flags=re.M)
                content = re.sub("<DB_NAME>", db_name, content, flags=re.M)
                content = re.sub("<DIALECT_DRIVER>", select_db, content, flags=re.M)
                content = re.sub("<TABLE_NAME>", table, content, flags=re.M)
                content = re.sub("<QUERY>", query, content, flags=re.M)

                f.write(content)

            port = randint(1000, 9999)

            with open('../../Dockerfile', 'r') as f:
                content = f.read()
            with open('../../Dockerfile', 'w') as f:
                content = re.sub("(?is)EXPOSE.{5}", "EXPOSE " + str(port), content, flags=re.M)
                content = re.sub("(?is)port.{5}", "port " + str(port), content, flags=re.M)
                f.write(content)

            docker_service = Dockerise()
            docker_service.spin_docker_container(port)

            return html.Div([
                html.Div([
                    html.P("Exposed Successfully, here is the endpoint: http://192.168.99.100:"+str(port)),
                ]),
            ], style={'margin-top': '20px'})
        except Exception as error:
            print(error)
            return "Not able to expose:"+str(error)


if __name__ == '__main__':
    app.run_server(debug=True)

