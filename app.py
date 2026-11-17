from pathlib import Path

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_PATH = Path(__file__).parent / "data" / "solar.csv"
DATA = pd.read_csv(DATA_PATH)

METRICS = {
    "Number of Solar Plants": {
        "label": "Usinas solares",
        "unit": "usinas",
        "color": "#f4a261",
    },
    "Installed Capacity (MW)": {
        "label": "Capacidade instalada",
        "unit": "MW",
        "color": "#2a9d8f",
    },
    "Average MW Per Plant": {
        "label": "Média por usina",
        "unit": "MW/usina",
        "color": "#457b9d",
    },
    "Generation (GWh)": {
        "label": "Geração",
        "unit": "GWh",
        "color": "#805ad5",
    },
}

METRIC_OPTIONS = [
    {"label": config["label"], "value": column}
    for column, config in METRICS.items()
]

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Dashboard de Energia Solar",
)
server = app.server

total_states = DATA["State"].nunique()
total_plants = DATA["Number of Solar Plants"].sum()
installed_capacity = DATA["Installed Capacity (MW)"].sum()
total_generation = DATA["Generation (GWh)"].sum()


def summary_card(title: str, value: str, detail: str) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(title, className="text-secondary mb-2"),
                html.H3(value, className="mb-1"),
                html.Small(detail, className="text-secondary"),
            ]
        ),
        className="h-100 border-0 shadow-sm",
    )


app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.P("PORTFÓLIO • DADOS", className="text-primary fw-bold mb-2"),
                    html.H1("Energia solar por estado", className="display-6 fw-bold"),
                    html.P(
                        "Explore indicadores de usinas, capacidade instalada e geração "
                        "em um painel interativo.",
                        className="lead text-secondary",
                    ),
                ],
                className="py-4",
            )
        ),
        dbc.Alert(
            [
                html.Strong("Nota sobre os dados: "),
                "o arquivo de exemplo cobre oito estados e não informa fonte ou "
                "período de referência. Use-o como demonstração técnica, não como "
                "estatística nacional atual.",
            ],
            color="warning",
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    summary_card(
                        "Estados no conjunto",
                        f"{total_states}",
                        "registros distintos",
                    ),
                    xs=12,
                    md=6,
                    lg=3,
                    className="mb-3",
                ),
                dbc.Col(
                    summary_card(
                        "Usinas registradas",
                        f"{total_plants:,.0f}",
                        "soma dos registros fornecidos",
                    ),
                    xs=12,
                    md=6,
                    lg=3,
                    className="mb-3",
                ),
                dbc.Col(
                    summary_card(
                        "Capacidade instalada",
                        f"{installed_capacity:,.0f} MW",
                        "soma dos registros fornecidos",
                    ),
                    xs=12,
                    md=6,
                    lg=3,
                    className="mb-3",
                ),
                dbc.Col(
                    summary_card(
                        "Geração registrada",
                        f"{total_generation:,.0f} GWh",
                        "soma dos registros fornecidos",
                    ),
                    xs=12,
                    md=6,
                    lg=3,
                    className="mb-3",
                ),
            ],
            className="mb-2",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "Indicador para comparar",
                                        htmlFor="metric-select",
                                        className="fw-semibold mb-2",
                                    ),
                                    dcc.Dropdown(
                                        id="metric-select",
                                        options=METRIC_OPTIONS,
                                        value="Number of Solar Plants",
                                        clearable=False,
                                    ),
                                ],
                                xs=12,
                                md=5,
                                lg=4,
                            ),
                        ],
                        className="mb-3",
                    ),
                    dcc.Graph(
                        id="metric-chart",
                        config={"displaylogo": False, "responsive": True},
                    ),
                ]
            ),
            className="border-0 shadow-sm mb-4",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2("Dados por estado", className="h4 mb-3"),
                    dag.AgGrid(
                        id="solar-grid",
                        rowData=DATA.to_dict("records"),
                        columnDefs=[
                            {
                                "field": "State",
                                "headerName": "Estado",
                                "pinned": "left",
                            },
                            *[
                                {
                                    "field": column,
                                    "headerName": label,
                                    "filter": "agNumberColumnFilter",
                                    "type": "rightAligned",
                                }
                                for column, label in [
                                    ("Number of Solar Plants", "Usinas solares"),
                                    ("Installed Capacity (MW)", "Capacidade (MW)"),
                                    ("Average MW Per Plant", "Média por usina (MW)"),
                                    ("Generation (GWh)", "Geração (GWh)"),
                                ]
                            ],
                        ],
                        defaultColDef={
                            "sortable": True,
                            "filter": True,
                            "resizable": True,
                        },
                        dashGridOptions={
                            "pagination": True,
                            "paginationPageSize": 8,
                        },
                        columnSize="sizeToFit",
                        style={"height": "360px", "width": "100%"},
                    ),
                ]
            ),
            className="border-0 shadow-sm mb-5",
        ),
        html.Footer(
            "Projeto acadêmico de visualização de dados • Python, pandas e Plotly Dash",
            className="text-center text-secondary small py-4",
        ),
    ],
    fluid=True,
    className="px-3 px-md-5",
)


@app.callback(
    Output("metric-chart", "figure"),
    Input("metric-select", "value"),
)
def update_metric_chart(selected_metric: str):
    config = METRICS[selected_metric]
    chart_data = DATA.sort_values(selected_metric, ascending=False)

    figure = px.bar(
        chart_data,
        x="State",
        y=selected_metric,
        title=f'{config["label"]} por estado',
        labels={
            "State": "Estado",
            selected_metric: f'{config["label"]} ({config["unit"]})',
        },
        text=selected_metric,
        color_discrete_sequence=[config["color"]],
    )
    number_format = (
        "%{text:,.1f}"
        if selected_metric == "Average MW Per Plant"
        else "%{text:,.0f}"
    )
    figure.update_traces(
        texttemplate=number_format,
        textposition="outside",
        cliponaxis=False,
    )
    figure.update_layout(
        template="plotly_white",
        margin={"l": 20, "r": 20, "t": 60, "b": 20},
        yaxis={"title": config["unit"], "rangemode": "tozero"},
        xaxis={"title": None},
        showlegend=False,
    )
    return figure


if __name__ == "__main__":
    app.run(debug=True)
