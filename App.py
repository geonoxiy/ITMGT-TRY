import pandas as pd
import streamlit as st
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import time
import numpy as np
from matplotlib.lines import Line2D

#web icon and title
st.set_page_config(
    page_title="A-Hatid!",
    page_icon="https://cdn-icons-png.freepik.com/512/6984/6984901.png"
)

#welcome page - load for 3 seconds c/o Love
if 'welcome_shown' not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    st.markdown("<h1 style='text-align: center;'>Welcome to A-Hatid!</h1>", unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.welcome_shown = True
    st.experimental_rerun()

#cache the data loading function to avoid reloading data on each interaction c/o Ju
@st.cache_data(ttl=300)
def load_data(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return pd.read_csv(url)

sheet_idA = '16CwByzI3-J0o36W7vs4hZ1Ovmyc2uV0DhJH4Cj96rU8'
dfA = load_data(sheet_idA)

line = st.selectbox(label="Select an E-Jeep Line", options=["LINE A", "LINE B"])

# plotting the general map c/o madie
def plot_map(title, coords, place_coords, place_labels):
    # fig, ax prepares a 6 by 4 space to plot points // destinations later 
    fig, ax = plt.subplots(figsize=(6, 4))  # This code helps adjust the height and width of the figure//graph
    # loads the image file (pin) meant to represent the e-jeep terminal stops 
    icon_path = 'pin.png'
    icon = plt.imread(icon_path)

    # starts a loop that iterates over pairs of coordinates and corresponding labels
    for (x, y), label in zip(place_coords, place_labels):
        im = OffsetImage(icon, zoom=0.005) # resizes the image
        ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False)  #takes the image (im), the coordinates (x, y) where the image should be placed, and xycoords='data' specifies that the coordinates are in data units
        ax.add_artist(ab) #adds the icon to the figure 
        ax.text(x + 0.1, y + 0.25, f' {label}', fontsize=6, verticalalignment='center_baseline', zorder=10) # settings for the size and placement of the terminal labels

    line_style = 'solid'
    for i in range(len(coords) - 1):
        x_start, y_start = coords[i]
        x_end, y_end = coords[i + 1]
        ax.plot([x_start, x_end], [y_start, y_end], linestyle='solid', color='darkgrey')

    # arrows indicating direction
    for i in range(len(coords) - 1):
        x_start, y_start = coords[i]
        x_end, y_end = coords[i + 1]
        midpoint = ((x_start + x_end) / 2, (y_start + y_end) / 2)
        dx = x_end - x_start
        dy = y_end - y_start
        rotation = np.degrees(np.arctan2(dy, dx))
        ax.text(midpoint[0], midpoint[1], "▸", fontsize=10, rotation=rotation, ha='center', va='center', color='darkgrey')

    # title settings
    ax.set_title(title, fontsize=10, pad=20)
    ax.axis('off') # to only show the graph itself and replicate an image of the route
    return fig, ax

def highlight_route(ax, start, end, line_coords, color): # defines the route to be highlighted 
    start_index = line_coords["coords"].index(line_coords["place_coords"][line_coords["place_labels"].index(start)]) # finds index of starting point
    end_index = line_coords["coords"].index(line_coords["place_coords"][line_coords["place_labels"].index(end)]) # finds index of end point 
    
    if start_index <= end_index: # if the start index <= end index, highlight all points end to end 
        highlighted_x = [line_coords["coords"][i][0] for i in range(start_index, end_index + 1)]
        highlighted_y = [line_coords["coords"][i][1] for i in range(start_index, end_index + 1)]
    else: # for the last stops // looping 
        highlighted_x = [line_coords["coords"][i][0] for i in range(start_index, len(line_coords["coords"]))]
        highlighted_x += [line_coords["coords"][i][0] for i in range(0, end_index + 1)]
        highlighted_y = [line_coords["coords"][i][1] for i in range(start_index, len(line_coords["coords"]))]
        highlighted_y += [line_coords["coords"][i][1] for i in range(0, end_index + 1)]
    
    ax.plot(highlighted_x, highlighted_y, color=color, linewidth=1, label=f'Route {start} to {end}') # labels and plots
    ax.legend(fontsize=6)
    
#dictionary of line coordinates for the map
line_coords = {
    "LINE A": {
        "coords": [(15, 1), (10, 1), (10, 3), (10, 4), (8, 4), (8, 4.5), (11, 4.5), (11, 5), (12.5, 5), (14.5, 5), (15, 5), (15, 1)],
        "place_coords": [(15, 1), (10, 3), (8, 4), (11, 4.5), (12.5, 5), (14.5, 5), (15, 1)],
        "place_labels": ['Hagdan na Bato','Old Comm', 'Gate 1', 'Gate 2.5', 'Leong Hall', 'Xavier Hall', 'Hagdan na Bato']
    }, 
    "LINE B": {
        "coords": [(11,1),(15,1),(15,10),(15,17),(15,20),(14,20),(14,7.5),(10,7.5),(8,7.5),(8,5),(9,5),(9,1),(11,1)],
        "place_coords": [(11,1),(15,10),(15,17),(10,7.5),(8,5), (11, 1)],
        "place_labels": ['Xavier Hall','AJHS','ASHS FLC Building','ISO','Arete', 'Xavier Hall']
    }
}

if line == "LINE A":
    st.title("Line A")
    st.write("If an E-jeep is marked For Charging, its final stop will be at Gate 1. The E-jeep will continue to make all stops up to Gate 1, as indicated on the map below.")
    st.write(dfA.head(3))


    # calls the plot_map function to create a map for "Line A Routes". It uses coordinates and place labels from line_coords["LINE A"] to plot the route.
    fig, ax = plot_map("Line A Routes", line_coords["LINE A"]["coords"], line_coords["LINE A"]["place_coords"], line_coords["LINE A"]["place_labels"])

    # retrieves the values of the cells from the gsheet, to be used for the conditional statements in highlighting a certain route
    try:
        A1 = dfA.iloc[0, 1]
        A2 = dfA.iloc[1, 1]
        A3 = dfA.iloc[2, 1]
        N1 = dfA.iloc[0, 2]
        N2 = dfA.iloc[1, 2]
        N3 = dfA.iloc[2, 2]

        def highlight(ax, last_item, next_item, color):
            if last_item == next_item: # prevents the code from creating a new highlight (ex. if Xavier is for charging, it should not highlight the next route: Xavier to AJHS)
                highlight_route(ax, last_item, last_item, line_coords["LINE A"], color)
            elif last_item == "Hagdan na Bato":
                highlight_route(ax, "Hagdan na Bato", "Old Comm", line_coords["LINE A"], color)
            elif last_item == "Old Comm":
                highlight_route(ax, "Old Comm", "Gate 1", line_coords["LINE A"], color)
            elif last_item == "Gate 1":
                highlight_route(ax, "Gate 1", "Gate 2.5", line_coords["LINE A"], color)
            elif last_item == "Gate 2.5":
                highlight_route(ax, "Gate 2.5", "Leong Hall", line_coords["LINE A"], color)
            elif last_item == "Leong Hall":
                highlight_route(ax, "Leong Hall", "Xavier Hall", line_coords["LINE A"], color)
            elif last_item == "Xavier Hall":
                highlight_route(ax, "Xavier Hall", "Hagdan na Bato", line_coords["LINE A"], color)

        highlight(ax, A1, N1, "red")
        highlight(ax, A2, N2, "blue")
        highlight(ax, A3, N3, "green")

        ax.legend(fontsize=6, bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
    
    except Exception as e:
        st.error(f"Error highlighting route: {e}")
    
    if dfA.iloc[0, 3] == "For Charging":
        st.write('A1: This E-jeep is only until Gate 1. This will still pass through stops before Gate 1.')
    if dfA.iloc[1, 3] == "For Charging":
        st.write('A2: This E-jeep is only until Gate 1. This will still pass through stops before Gate 1.')
    if dfA.iloc[2, 3] == "For Charging":
        st.write('A3: This E-jeep is only until Gate 1. This will still pass through stops before Gate 1.')

if line == "LINE B":
    st.title("Line B")
    st.write("If an E-jeep is marked For Charging, its final stop will be at Xavier Hall. The E-jeep will continue to make all stops up to Xavier Hall, as indicated on the map below.")
    st.write(dfA.iloc[5:8])

    # calls the plot_map function to create a map for "Line B Routes". It uses coordinates and place labels from line_coords["LINE B"] to plot the route.    
    fig, ax = plot_map("Line B Routes", line_coords["LINE B"]["coords"], line_coords["LINE B"]["place_coords"], line_coords["LINE B"]["place_labels"])

    # retrieves the values of the cells from the gsheet, to be used for the conditional statements in highlighting a certain route
    try:
        B1 = dfA.iloc[5, 1]
        B2 = dfA.iloc[6, 1]
        B3 = dfA.iloc[7, 1]
        M1 = dfA.iloc[5, 2]
        M2 = dfA.iloc[6, 2]
        M3 = dfA.iloc[7, 2]

        def highlight(ax, last_item, next_item, color):
            if last_item == next_item: # prevents the code from creating a new highlight (ex. if Xavier is for charging, it should not highlight the next route: Xavier to AJHS)
                highlight_route(ax, last_item, last_item, line_coords["LINE B"], color)
            elif last_item == "Xavier Hall":
                highlight_route(ax, "Xavier Hall", "AJHS", line_coords["LINE B"], color)
            elif last_item == "AJHS":
                highlight_route(ax, "AJHS", "ASHS FLC Building", line_coords["LINE B"], color)
            elif last_item == "ASHS FLC Building":
                highlight_route(ax, "ASHS FLC Building", "ISO", line_coords["LINE B"], color)
            elif last_item == "ISO":
                highlight_route(ax, "ISO", "Arete", line_coords["LINE B"], color)
            elif last_item == "Arete":
                highlight_route(ax, "Arete", "Xavier Hall", line_coords["LINE B"], color)

        highlight(ax, B1, M1, "red")
        highlight(ax, B2, M2, "blue")
        highlight(ax, B3, M3, "green")

        ax.legend(fontsize=6, bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
    
    except Exception as e:
        st.error(f"Error highlighting route: {e}")
    
    if dfA.iloc[5, 3] == "For Charging":
        st.write('B1: This E-jeep is only until Xavier Hall. This will still pass through stops before Xavier Hall.')
    if dfA.iloc[6, 3] == "For Charging":
        st.write('B2: This E-jeep is only until Xavier Hall. This will still pass through stops before Xavier Hall.')
    if dfA.iloc[7, 3] == "For Charging":
        st.write('B3: This E-jeep is only until Xavier Hall. This will still pass through stops before Xavier Hall.')

# indication of the last time the code was refreshed
local_tz = pytz.timezone('Asia/Manila')
local_time = datetime.datetime.now(local_tz)

st.write("Last updated:", local_time.strftime("%Y-%m-%d %H:%M:%S"), "  -/  Occasionally refresh the website to get updates!")
