import streamlit as st
from kloppy import metrica
from st_soccer import TrackingComponent
import pandas as pd
import numpy as np
import time


BLUE = "#2b83ba"
RED = "#d7191c"

#sourced from streamlit example, git here: https://github.com/devinpleuler/streamlit-soccer/tree/master
#TODO: Replace with actual match data from example match
def get_sample_data(limit=1000):

    #load sample data
    dataset = metrica.load_tracking_csv(
        home_data="https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv",
        away_data="https://raw.githubusercontent.com/metrica-sports/sample-data/master/data/Sample_Game_1/Sample_Game_1_RawTrackingData_Away_Team.csv",
        limit=limit,
        coordinates="metrica",
    )

    #populate frame data from sample dataset
    frames = []
    home_team = dataset.metadata.teams[0]
    for f in dataset.frames:
        frame_data = []
        for player, coordinates in f.players_coordinates.items():
            attrs = {
                "x": coordinates.x,
                "y": coordinates.y,
                "team": "home" if player.team == home_team else "away",
            }
            frame_data.append(attrs)

        try:
            ball_x, ball_y = f.ball_coordinates.x, f.ball_coordinates.y
            attrs = {
                "x": ball_x,
                "y": ball_y,
                "team": "ball",
            }
            frame_data.append(attrs)
        except AttributeError:
            pass  # No ball coordinates

        frames.append(frame_data)

    return frames

def main():
    st.set_page_config(page_title="Tactics Board", page_icon=":soccer:")
    frames = get_sample_data()
    n_frames = len(frames)

    #Initialize session state
    if "frame_index" not in st.session_state:
        st.session_state.frame_index = 0
    if "playing" not in st.session_state:
        st.session_state.playing = False
    if "chunk" not in st.session_state:
        st.session_state.chunk = (0, min(200, n_frames - 1))
    

    st.subheader("Select Replay Range")
    st.session_state.chunk = st.slider(
        "Frame Range",
        0, n_frames - 1,
        st.session_state.chunk,
        step=1
    )
    start, end = st.session_state.chunk

    if "curr_start" not in st.session_state:
        st.session_state.curr_start = start
    
    st.subheader("Playback Controls")
    col1, col2, col3 =st.columns([1,2,3])

    with col1:
        if st.button("Play"):
            st.session_state.playing = True
            st.rerun()

    with col2:
        if st.button("Pause"):
            st.session_state.playing = False

    with col3:
        st.session_state.frame_index = st.slider(
            "Frame",
            start, end,
            st.session_state.frame_index,
            step=1
        )

    #Display current frames
    if st.session_state.playing:
        st.write(st.session_state.frame_index)
        TrackingComponent(frames=frames[st.session_state.curr_start:end], home_color=RED, away_color=BLUE, loop="no")
        st.session_state.frame_index += 1
        if st.session_state.frame_index > end:
            st.session_state.frame_index = start
        time.sleep(0.033)
        st.rerun()
    else:
        st.session_state.curr_start = st.session_state.frame_index
        #If pause button is clicked, stop animation
        st.write(st.session_state.frame_index)
        #Needs to have frame:frame+2 because of js animation limitation, will not run on only 1 frame
        TrackingComponent(frames=frames[st.session_state.frame_index:st.session_state.frame_index + 2], home_color=RED, away_color=BLUE, loop="no")

    #TODO Data visualization using skill corner

st.set_page_config(page_title="Tactics Board", page_icon=":soccer:")
if __name__ == "__main__":
    main()