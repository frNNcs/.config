import json
import re
import uuid

# Read the original text
with open("/Users/francisco/.local/share/opencode/tool-output/tool_ce39af8a9001AooWAxfeRfoEGM", "r") as f:
    text = json.load(f)

# Regex to match headers
header_pattern = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)

sections = []
last_pos = 0
last_header = None
last_header_level = 0

for match in header_pattern.finditer(text):
    start_pos = match.start()
    
    # Text before this header
    if start_pos > last_pos:
        section_text = text[last_pos:start_pos].strip()
        if section_text:
            sections.append({
                "header": last_header if last_header else "Intro",
                "level": last_header_level,
                "text": section_text
            })
            
    last_header = match.group(2).strip()
    last_header_level = len(match.group(1))
    last_pos = match.start()  # Include the header in the section text for context

# Add the last section
if last_pos < len(text):
    section_text = text[last_pos:].strip()
    if section_text:
        sections.append({
            "header": last_header if last_header else "Intro",
            "level": last_header_level,
            "text": section_text
        })

print(f"Found {len(sections)} sections")

# Build Canvas JSON
nodes = []
edges = []

current_y = 0
x_pos = 0
width = 600
base_height = 200

# Top-down layout
# We will just put them in a vertical line, or a tree if we respect levels.
# The prompt says: "une todos los nodos generados con flechas en una disposición top-down (de arriba hacia abajo)"

parent_stack = []

for i, sec in enumerate(sections):
    node_id = uuid.uuid4().hex[:10]
    
    # Calculate height based on text length (roughly 1 line = 80 chars, line height 30px)
    lines = len(sec["text"]) // 80 + sec["text"].count("\n") + 2
    height = max(150, min(800, lines * 25))
    
    node = {
        "id": node_id,
        "type": "text",
        "text": sec["text"],
        "x": x_pos,
        "y": current_y,
        "width": width,
        "height": height
    }
    
    # If using colors based on level
    colors = ["1", "2", "3", "4", "5", "6"]
    color_idx = min(sec["level"], 5)
    node["color"] = colors[color_idx]
    
    nodes.append(node)
    
    # Add edge from previous node
    if i > 0:
        prev_node = nodes[i-1]
        edge_id = uuid.uuid4().hex[:10]
        edges.append({
            "id": edge_id,
            "fromNode": prev_node["id"],
            "fromSide": "bottom",
            "toNode": node_id,
            "toSide": "top",
            "color": "6"
        })
        
    current_y += height + 100

canvas_data = {
    "nodes": nodes,
    "edges": edges
}

with open("/Users/francisco/.config/003 Resources/Clippings/Guía Obsidian con sincronización instantánea, gratuita y autoalojada - Breakdown.canvas", "w", encoding="utf-8") as f:
    json.dump(canvas_data, f, indent=2, ensure_ascii=False)

print("Canvas created successfully.")
