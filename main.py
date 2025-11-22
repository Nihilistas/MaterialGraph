# Materials Graph App (Data-Driven Version)
# Loads JSON material files from data/materials/

import json
from pathlib import Path

import dash
from dash import html, dcc
import dash_cytoscape as cyto
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

DATA_DIR = Path(__file__).resolve().parent / "data" / "materials"


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


def build_graph_elements(materials, derivations=None):
    nodes = []
    edges = []

    for mat in materials.values():
        nodes.append({
            "data": {
                "id": mat["id"],
                "label": mat.get("label", mat["id"]),
                "info": mat.get("info", "")
            }
        })

        for src in mat.get("derived_from", []):
            if src in materials:
                edges.append({"data": {"source": src, "target": mat["id"], "label": "→"}})

        # Add edges from derivation.json data if provided
    if derivations:
        for der in derivations.values():
            srcs = der.get("derived_from", [])
            tgt = der.get("id")
            for s in srcs:
                if s in materials:
                    edges.append({"data": {"source": s, "target": tgt, "label": "→"}})
            # "makes" edges
            for m in der.get("makes", []):
                if m in materials:
                    edges.append({"data": {"source": tgt, "target": m, "label": "→"}})

    return nodes + edges


materials = load_materials()

# Load derivation.json files if they exist
DERIV_DIR = Path(__file__).resolve().parent / "data" / "derivations"
derivations = {}
if DERIV_DIR.exists():
    for file in DERIV_DIR.glob("*.json"):
        try:
            d = json.loads(file.read_text())
            derivations[d["id"]] = d
        except Exception:
            pass

elements = build_graph_elements(materials, derivations)

app.layout = html.Div([
    html.H2("Materials Knowledge Graph - Data-Driven"),

    cyto.Cytoscape(
        id='materials-graph',
        elements=elements,
        style={'width': '100%', 'height': '500px'},
        layout={'name': 'cose'},
        stylesheet=[
            {'selector': 'node', 'style': {'content': 'data(label)', 'background-color': '#88c0d0', 'font-size': '16px'}},
            {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle'}},
        ]
    ),

    html.Div(id='info-panel', style={'padding': '1em', 'background': '#eee', 'margin-top': '20px'})
])


@app.callback(Output('info-panel', 'children'), Input('materials-graph', 'tapNodeData'))
def display_info(data):
    if not data:
        return "Click a material to see details."

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
