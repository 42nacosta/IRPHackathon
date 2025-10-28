import streamlit as st
from kloppy import metrica
from st_soccer import TrackingComponent

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
    st.markdown("## Streamlit Soccer Demo")
    tc = TrackingComponent(frames=frames, home_color=RED, away_color=BLUE, loop="yes")


st.set_page_config(page_title="Tactics Board", page_icon=":soccer:")
if __name__ == "__main__":
    main()