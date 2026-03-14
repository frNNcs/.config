import json
import re
import uuid

with open("/Users/francisco/.local/share/opencode/tool-output/tool_ce39af8a9001AooWAxfeRfoEGM", "r") as f:
    text = json.load(f)

header_pattern = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)

sections = []
last_pos = 0
last_header = "Intro"
last_header_level = 0

for match in header_pattern.finditer(text):
    start_pos = match.start()
    if start_pos > last_pos:
        section_text = text[last_pos:start_pos].strip()
        if section_text:
            sections.append({
                "id": uuid.uuid4().hex[:10],
                "title": last_header,
                "level": last_header_level,
                "text": section_text
            })
            
    last_header = match.group(2).strip()
    last_header_level = len(match.group(1))
    last_pos = start_pos

if last_pos < len(text):
    section_text = text[last_pos:].strip()
    if section_text:
        sections.append({
            "id": uuid.uuid4().hex[:10],
            "title": last_header,
            "level": last_header_level,
            "text": section_text
        })

NODE_WIDTH = 550
Y_SPACING = 80
X_INDENT = 100

nodes_json = []
edges_json = []

current_y = 0

for i, sec in enumerate(sections):
    text_content = sec["text"]
    lines = len(text_content) // 60 + text_content.count("\n") + 1
    height = max(100, min(1000, lines * 22 + 40))
    
    lvl = sec["level"]
    x_pos = lvl * X_INDENT
    
    color_idx = str(min(lvl, 6)) if lvl > 0 else "1"
    if color_idx == "0": color_idx = "1"
    
    node = {
        "id": sec["id"],
        "type": "text",
        "text": text_content,
        "x": x_pos,
        "y": current_y,
        "width": NODE_WIDTH,
        "height": height,
        "color": color_idx
    }
    nodes_json.append(node)
    
    if i > 0:
        prev_id = sections[i-1]["id"]
        edges_json.append({
            "id": uuid.uuid4().hex[:10],
            "fromNode": prev_id,
            "fromSide": "bottom",
            "toNode": sec["id"],
            "toSide": "top",
            "color": "6"
        })
        
    current_y += height + Y_SPACING

canvas_data = {
    "nodes": nodes_json,
    "edges": edges_json
}

with open("/tmp/breakdown.canvas", "w", encoding="utf-8") as f:
    json.dump(canvas_data, f, indent=2, ensure_ascii=False)

print(f"Canvas built with {len(nodes_json)} nodes and {len(edges_json)} edges.")
