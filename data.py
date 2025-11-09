# Example material graph nodes & edges
elements = [
    # Nodes
    {"data": {"id": "wood", "label": "Wood", "info": "Found in forests. Used to make paper."}},
    {"data": {"id": "grass", "label": "Grass", "info": "Common plant. Can also produce paper."}},
    {"data": {"id": "paper", "label": "Paper", "info": "Derived from wood or grass."}},

    # Edges
    {"data": {"source": "wood", "target": "paper", "label": "→"}},
    {"data": {"source": "grass", "target": "paper", "label": "→"}},
]
