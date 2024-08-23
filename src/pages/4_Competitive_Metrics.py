import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from MetricsChefsHat.CalculateMetrics import calculate_scores, eccentricity_df
from MetricsChefsHat.PlotManager import PlayerAnalysis


# Function to load data from a .pkl file
# @st.cache
def load_data(filepath):
    df = pd.read_pickle(filepath)
    df = df.reset_index(drop=True)

    return df


# @st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


# Streamlit page setup

st.write("# Competitive Metrics! :dart:")
st.write(
    "Here you can calculate all the competitive metrics proposed by Laura Triglia (More information: https://github.com/lauratriglia/MetricsChefsHat) from a game dataset. These metrics measure the behavior of each agent when playing the game, and are ideal to describe the impact of each agent on the game dynamics."
)


# File uploader for user input
uploaded_file = st.file_uploader("Choose a PKL file", type="pkl")
if uploaded_file is not None:
    data = load_data(uploaded_file)
    if data.empty:
        st.write("No data found in the file.")
    else:

        my_bar = st.progress(0, text="Loading data...")

        matches = data["Match"].unique()[1:]

        first_person_df = []
        third_person_df = []

        for count, match in enumerate(matches):
            match_df = data[(data["Match"] == match) & (data["Source"] != "SYSTEM")]
            finish_index = match_df[match_df["Player_Finished"] == True].index.min()
            match_df = match_df.loc[:finish_index]
            third_person_df.append(calculate_scores(match_df, match))
            first_person_df.append(eccentricity_df(match_df, match)[0])
            my_bar.progress(int((count / len(matches)) * 100), text="Loading data...")

        my_bar.empty()

        third_person_df = pd.concat(third_person_df)
        third_person_csv = convert_df(third_person_df)

        first_person_df = pd.concat(first_person_df)
        first_person_csv = convert_df(first_person_df)

        st.write("Data loaded!")
        st.markdown("---")

        st.subheader("Available Metrics")
        st.download_button(
            "Download First Person Metrics",
            first_person_csv,
            "file.csv",
            "text/csv",
            key="download-csv-first",
        )

        st.download_button(
            "Download Third Person Metrics",
            third_person_csv,
            "file.csv",
            "text/csv",
            key="download-csv-third",
        )

        st.markdown("---")
        st.subheader("Visualize Metrics for Individual Matches ")

        matches_select = st.selectbox("Select a match:", matches)

        if matches_select:

            match_df = data[
                (data["Match"] == matches_select) & (data["Source"] != "SYSTEM")
            ]
            finish_index = match_df[match_df["Player_Finished"] == True].index.min()
            match_df = match_df.loc[:finish_index]

            this_match_score = calculate_scores(match_df, matches_select)

            print("--------Score---------")
            print(this_match_score)

            metrics_third_person = PlayerAnalysis(this_match_score)
            metrics_first_person = PlayerAnalysis(match_df)

            # st.dataframe(this_match_score)
            st.subheader("Third Person Metrics")
            st.write(
                f"Showing Attack / Defense / Vitality for match number {matches_select}"
            )
            col1, col2, col3 = st.columns(3)
            # with col2:
            fig_third_all = metrics_third_person.radar_chart_tot("")
            st.pyplot(fig_third_all)
            # fig_third_single = metrics_third_person.radar_chart("")

            # st.pyplot(fig_third_single)

            st.markdown("---")
            st.subheader("First Person Metrics")
            st.write(f"Showing Eccentricity for match number {matches_select}")
            fig_person_single = metrics_first_person.self_plots("")
            st.pyplot(fig_person_single)
