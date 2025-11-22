# Materials Graph App (Data-Driven Version)
# Loads JSON material files from data/materials/

import json
from pathlib import Path

import dash
from dash import html, dcc, no_update
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "materials"
DERIV_DIR = BASE_DIR / "data" / "derivations"


def load_materials():
    materials = {}
    if not DATA_DIR.exists():
        return materials

    for file in DATA_DIR.glob("*.json"):
        try:
            material = json.loads(file.read_text())
            materials[material["id"]] = material
        except Exception:
            pass
    return materials


def load_derivations():
    derivations = {}
    if not DERIV_DIR.exists():
        return derivations

    for file in DERIV_DIR.glob("*.json"):
        try:
            d = json.loads(file.read_text())
            derivations[d["id"]] = d
        except Exception:
            pass
    return derivations


def build_graph_elements(materials, derivations=None):
    nodes = {}
    edges = []

    def ensure_node(node_id, label=None, info=""):
        if not node_id:
            return
        if node_id not in nodes:
            nodes[node_id] = {
                "data": {
                    "id": node_id,
                    "label": label or node_id,
                    "info": info or ""
                }
            }

    def add_edge(source, target):
        if source and target:
            edges.append({"data": {"source": source, "target": target, "label": "→"}})

    # Nodes and edges from material files
    for mat in materials.values():
        ensure_node(mat["id"], mat.get("label", mat["id"]), mat.get("info", ""))
        for src in mat.get("derived_from", []):
            ensure_node(src)  # show referenced materials even if not yet researched
            add_edge(src, mat["id"])

    # Nodes and edges from derivations (may reference materials not yet researched)
    if derivations:
        for der in derivations.values():
            tgt = der.get("id")
            ensure_node(tgt)
            for s in der.get("derived_from", []):
                ensure_node(s)
                add_edge(s, tgt)
            for m in der.get("makes", []):
                ensure_node(m)
                add_edge(tgt, m)

    return list(nodes.values()) + edges

app.layout = html.Div([
    html.H2("Materials Knowledge Graph - Data-Driven"),

    dcc.Store(id='materials-store'),
    dcc.Store(id='derivations-store'),
    dcc.Interval(id='data-refresh', interval=5_000, n_intervals=0),

    cyto.Cytoscape(
        id='materials-graph',
        elements=[],
        style={'width': '100%', 'height': '500px'},
        layout={'name': 'cose'},
        stylesheet=[
            {'selector': 'node', 'style': {'content': 'data(label)', 'background-color': '#88c0d0', 'font-size': '16px'}},
            {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle'}},
        ]
    ),

    html.Div(id='info-panel', style={'padding': '1em', 'background': '#eee', 'margin-top': '20px'})
])


@app.callback(
    Output('materials-graph', 'elements'),
    Output('materials-store', 'data'),
    Output('derivations-store', 'data'),
    Input('data-refresh', 'n_intervals'),
    State('materials-store', 'data'),
    State('derivations-store', 'data'),
)
def refresh_data(_, prev_materials, prev_derivations):
    materials = load_materials()
    derivations = load_derivations()
    prev_materials = prev_materials or {}
    prev_derivations = prev_derivations or {}

    if materials == prev_materials and derivations == prev_derivations:
        return no_update, no_update, no_update

    elements = build_graph_elements(materials, derivations)
    return elements, materials, derivations


@app.callback(
    Output('info-panel', 'children'),
    Input('materials-graph', 'tapNodeData'),
    Input('materials-store', 'data'),
)
def display_info(data, materials):
    if not data:
        return "Click a material to see details."

    materials = materials or {}
    mat = materials.get(data.get("id"))
    if not mat:
        return "No data available."

    return html.Div([
        html.H3(mat.get("label")),
        html.P(mat.get("info")),
        html.H4("Found In"),
        html.Ul([html.Li(x) for x in mat.get("found_in", [])]),

        html.H4("Discovery"),
        html.Ul([
            html.Li(f"Locations: {', '.join(mat['discovery'].get('locations', []))}"),
            html.Li(f"Season: {mat['discovery'].get('season')}") if mat['discovery'].get('season') else None,
            html.Li(f"Appearance: {mat['discovery'].get('appearance')}") if mat['discovery'].get('appearance') else None,
        ]),

        html.H4("Recipe"),
        html.Ol([html.Li(step) for step in mat.get("recipe", [])]),

        html.P("(Media, videos, images, and more can be added here.)")
    ])


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
