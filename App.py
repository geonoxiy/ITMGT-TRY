import pandas as pd
import streamlit as st
import time
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Cache the data loading function to avoid reloading data on each interaction
@st.cache_resource
def load_data(sheet_id):
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")

sheet_idA = '16CwByzI3-J0o36W7vs4hZ1Ovmyc2uV0DhJH4Cj96rU8'
dfA = load_data(sheet_idA)

st.set_page_config(
    page_title="A-Hatid!",
    page_icon="https://cdn-icons-png.freepik.com/512/6984/6984901.png"
)

line = st.selectbox(label="Select E-Jeep Line to view", options=["LINE A", "LINE B"])

def plot_map(title, cell_value, coords, place_coords, place_labels):
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the width and height as needed
    icon_path = 'pin.png'
    icon = plt.imread(icon_path)
    # Add icons and labels to the map
    for (x, y), label in zip(place_coords, place_labels):
        im = OffsetImage(icon, zoom=0.005)
        ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False)
        ax.add_artist(ab)
        ax.text(x + 0.1, y + 0.2, f' {label}', fontsize=8, verticalalignment='center_baseline', zorder=10)
    ax.plot(*zip(*coords), color='lightgray', label='Route')  
    ax.set_title(title, fontsize=14, pad=20)
    ax.axis('off')
    return fig, ax

def highlight_route(ax, start, end, line_coords):
    start_index = line_coords["coords"].index(line_coords["place_coords"][line_coords["place_labels"].index(start)])
    end_index = line_coords["coords"].index(line_coords["place_coords"][line_coords["place_labels"].index(end)])
    if start_index <= end_index:
        highlighted_x = [line_coords["coords"][i][0] for i in range(start_index, end_index + 1)]
        highlighted_y = [line_coords["coords"][i][1] for i in range(start_index, end_index + 1)]
    else:
        highlighted_x = [line_coords["coords"][i][0] for i in range(start_index, len(line_coords["coords"]))]
        highlighted_x += [line_coords["coords"][i][0] for i in range(0, end_index + 1)]
        highlighted_y = [line_coords["coords"][i][1] for i in range(start_index, len(line_coords["coords"]))]
        highlighted_y += [line_coords["coords"][i][1] for i in range(0, end_index + 1)]
    
    ax.plot(highlighted_x, highlighted_y, color='#0305C6', linewidth=2, label=f'Route {start} to {end}')
    ax.legend()

line_coords = {
    "LINE A": {
        "coords": [(15, 1), (10, 1), (10, 3), (10, 4), (8, 4), (8, 4.5), (11, 4.5), (11, 5), (12.5, 5), (14.5, 5), (15, 5), (15, 1)],
        "place_coords": [(15, 1), (10, 3), (8, 4), (11, 4.5), (12.5, 5), (14.5, 5), (15, 1)],
        "place_labels": ['Hagdan na Bato', 'Old Comm', 'Gate 1', 'Gate 2.5', 'Leong Hall', 'Xavier Hall', 'Hagdan na Bato']
    }, 
    "LINE B":{
        "coords": [(11,1),(15,1),(15,10),(15,17),(15,20),(14,20),(14,7.5),(10,7.5),(8,7.5),(8,5),(9,5),(9,1),(11,1)],
        "place_coords": [(11,1),(15,10),(15,17),(10,7.5),(8,5), (11, 1)],
        "place_labels": ['Xavier Hall','AJHS','ASHS FLC Building','ISO','Arete', 'Xavier Hall']
    }
}

if line == "LINE A":
    st.title("Line A")
    st.write(dfA.head(3))
    
    # A1
    A1 = dfA.iloc[0, 1] 
    fig, ax = plot_map("A1", A1, line_coords["LINE A"]["coords"], line_coords["LINE A"]["place_coords"], line_coords["LINE A"]["place_labels"])
    try:
        last_item = A1
        if last_item == "Hagdan na Bato":
            highlight_route(ax, "Hagdan na Bato", "Old Comm", line_coords["LINE A"])
        elif last_item == "Old Comm":
            highlight_route(ax, "Old Comm", "Gate 1", line_coords["LINE A"])
        elif last_item == "Gate 1":
            highlight_route(ax, "Gate 1", "Gate 2.5", line_coords["LINE A"])
        elif last_item == "Gate 2.5":
            highlight_route(ax, "Gate 2.5", "Leong Hall", line_coords["LINE A"])
        elif last_item == "Leong Hall":
            highlight_route(ax, "Leong Hall", "Xavier Hall", line_coords["LINE A"])
        elif last_item == "Xavier Hall":
            highlight_route(ax, "Xavier Hall", "Hagdan na Bato", line_coords["LINE A"])
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error highlighting route: {e}")
    if dfA.iloc[0, 3] == "For Charging":
        st.write('This E-jeep is only until Gate 1.')
    
    # A2
    A2 = dfA.iloc[1, 1]  
    fig, ax = plot_map("A2", A2, line_coords["LINE A"]["coords"], line_coords["LINE A"]["place_coords"], line_coords["LINE A"]["place_labels"])
    
    try:
        last_item = A2
        if last_item == "Hagdan na Bato":
            highlight_route(ax, "Hagdan na Bato", "Old Comm", line_coords["LINE A"])
        elif last_item == "Old Comm":
            highlight_route(ax, "Old Comm", "Gate 1", line_coords["LINE A"])
        elif last_item == "Gate 1":
            highlight_route(ax, "Gate 1", "Gate 2.5", line_coords["LINE A"])
        elif last_item == "Gate 2.5":
            highlight_route(ax, "Gate 2.5", "Leong Hall", line_coords["LINE A"])
        elif last_item == "Leong Hall":
            highlight_route(ax, "Leong Hall", "Xavier Hall", line_coords["LINE A"])
        elif last_item == "Xavier Hall":
            highlight_route(ax, "Xavier Hall", "Hagdan na Bato", line_coords["LINE A"])
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error highlighting route: {e}")
    if dfA.iloc[1, 3] == "For Charging":
        st.write('This E-jeep is only until Gate 1.')
    # A3
    A3 = dfA.iloc[2, 1]  
    fig, ax = plot_map("A3", A3, line_coords["LINE A"]["coords"], line_coords["LINE A"]["place_coords"], line_coords["LINE A"]["place_labels"])
    
    try:
        last_item = A3
        if last_item == "Hagdan na Bato":
            highlight_route(ax, "Hagdan na Bato", "Old Comm", line_coords["LINE A"])
        elif last_item == "Old Comm":
            highlight_route(ax, "Old Comm", "Gate 1", line_coords["LINE A"])
        elif last_item == "Gate 1":
            highlight_route(ax, "Gate 1", "Gate 2.5", line_coords["LINE A"])
        elif last_item == "Gate 2.5":
            highlight_route(ax, "Gate 2.5", "Leong Hall", line_coords["LINE A"])
        elif last_item == "Leong Hall":
            highlight_route(ax, "Leong Hall", "Xavier Hall", line_coords["LINE A"])
        elif last_item == "Xavier Hall":
            highlight_route(ax, "Xavier Hall", "Hagdan na Bato", line_coords["LINE A"])
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error highlighting route: {e}")
    if dfA.iloc[7, 3] == "For Charging":
        st.write('This E-jeep is only until Gate 1.')
