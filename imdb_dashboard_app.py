
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np # For numerical operations, e.g., handling inf/NaN for scatter plot scaling

# Set a clean plotting style for Matplotlib/Seaborn for better aesthetics
plt.style.use('ggplot')
sns.set_palette('deep') # A good default color palette for charts

# --- Data Loading (Cached for performance) ---
@st.cache_data
def load_data():
    """
    Loads movie data from the SQLite database.
    Uses st.cache_data to cache the data, so it's only loaded once across reruns.
    """
    try:
        conn = sqlite3.connect("imdb_2024.db")
        query = "SELECT * FROM movies"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading data from 'imdb_2024.db': {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

# Load the entire dataset
movies_df = load_data()

# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="IMDb 2024 Movie Analysis")

st.title("🎬 IMDb 2024 Data Analysis and Visualizations")
st.markdown("Explore insights from IMDb's 2024 movie list with interactive filters and dynamic charts.")

if movies_df.empty:
    st.warning("No movie data available to display. Please ensure your 'imdb_2024.db' database and 'movies' table are populated correctly from your data processing script.")
else:
    # --- Interactive Filtering Functionality (Sidebar) ---
    st.sidebar.header("Filter Movies 📊")
    st.sidebar.markdown("Use the controls below to refine the dataset.")

    # Ensure 'genre' column is string type for consistent filtering
    movies_df['genre'] = movies_df['genre'].astype(str)

    # Genre filter: Allow users to filter movies within specific genres
    all_genres = sorted(movies_df['genre'].unique().tolist())
    selected_genres = st.sidebar.multiselect(
        "Select Genre(s):",
        options=all_genres,
        default=all_genres # Select all by default
    )

    # Apply genre filter first to make other slider ranges dynamic
    filtered_df_genre = movies_df[movies_df['genre'].isin(selected_genres)].copy()

    # Dynamic sliders for other filters based on the currently genre-filtered data
    # Ratings filter: Filter movies based on IMDb ratings (e.g., > 8.0)
    if not filtered_df_genre.empty:
        min_rating_val, max_rating_val = float(filtered_df_genre['rating'].min()), float(filtered_df_genre['rating'].max())
        rating_range = st.sidebar.slider(
            "Rating Range:",
            min_value=min_rating_val,
            max_value=max_rating_val,
            value=(min_rating_val, max_rating_val),
            step=0.1,
            format="%.1f"
        )
    else: # Fallback if genre filter makes the DataFrame empty
        min_rating_val, max_rating_val = 0.0, 10.0
        rating_range = st.sidebar.slider("Rating Range:", min_value=min_rating_val, max_value=max_rating_val, value=(min_rating_val, max_rating_val), step=0.1, format="%.1f")


    # Duration (Hrs) filter: Filter movies based on their runtime (e.g., < 2 hrs, 2–3 hrs, > 3 hrs)
    if not filtered_df_genre.empty:
        min_duration_val, max_duration_val = int(filtered_df_genre['duration_minutes'].min()), int(filtered_df_genre['duration_minutes'].max())
        duration_range = st.sidebar.slider(
            "Duration (minutes):",
            min_value=min_duration_val,
            max_value=max_duration_val,
            value=(min_duration_val, max_duration_val),
            step=5 # Step by 5 minutes
        )
    else: # Fallback
        min_duration_val, max_duration_val = 0, 300 # Default max 5 hours
        duration_range = st.sidebar.slider("Duration (minutes):", min_value=min_duration_val, max_value=max_duration_val, value=(min_duration_val, max_duration_val), step=5)


    # Voting Counts filter: Filter based on the number of votes received (e.g., > 10,000 votes)
    if not filtered_df_genre.empty:
        min_votes_val, max_votes_val = int(filtered_df_genre['voting_counts'].min()), int(filtered_df_genre['voting_counts'].max())
        vote_range = st.sidebar.slider(
            "Voting Counts:",
            min_value=min_votes_val,
            max_value=max_votes_val,
            value=(min_votes_val, max_votes_val),
            step=1000 # Step by 1000 votes
        )
    else: # Fallback
        min_votes_val, max_votes_val = 0, 1000000 # Default to 1M votes
        vote_range = st.sidebar.slider("Voting Counts:", min_value=min_votes_val, max_value=max_votes_val, value=(min_votes_val, max_votes_val), step=1000)


    # Apply all filters to create the final filtered DataFrame
    # This also combines filtering options so users can apply multiple filters simultaneously
    final_filtered_df = filtered_df_genre[
        (filtered_df_genre['rating'] >= rating_range[0]) &
        (filtered_df_genre['rating'] <= rating_range[1]) &
        (filtered_df_genre['duration_minutes'] >= duration_range[0]) &
        (filtered_df_genre['duration_minutes'] <= duration_range[1]) &
        (filtered_df_genre['voting_counts'] >= vote_range[0]) &
        (filtered_df_genre['voting_counts'] <= vote_range[1])
    ].copy() # Use .copy() to avoid SettingWithCopyWarning with filtered data

    # --- Display Filtered Results in a dynamic DataFrame ---
    st.header("Filtered Movie Data 🎥")
    st.dataframe(final_filtered_df)
    st.write(f"Displaying {len(final_filtered_df)} movies matching your criteria (out of {len(movies_df)} total movies).")

    if final_filtered_df.empty:
        st.info("No movies match the selected filter criteria. Adjust your filters to see results.")
    else:
        st.header("Interactive Visualizations 📈")

        # --- Top 10 Movies by Rating and Voting Counts ---
        # Visualization 1a: Top 10 Movies by Rating
        st.markdown("### Top 10 Movies by Rating")
        top_rated_movies = final_filtered_df.sort_values(by='rating', ascending=False).head(10)
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='rating', y='movie_name', data=top_rated_movies, ax=ax1, palette='viridis')
        ax1.set_title('Top 10 Movies by IMDb Rating (Filtered Data)')
        ax1.set_xlabel('Rating')
        ax1.set_ylabel('Movie Name')
        plt.xticks(rotation=0) # Ensure x-axis labels are horizontal
        plt.tight_layout()
        st.pyplot(fig1)

        # Visualization 1b: Top 10 Movies by Voting Counts
        st.markdown("### Top 10 Movies by Voting Counts")
        top_voted_movies = final_filtered_df.sort_values(by='voting_counts', ascending=False).head(10)
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='voting_counts', y='movie_name', data=top_voted_movies, ax=ax2, palette='cividis')
        ax2.set_title('Top 10 Movies by Voting Counts (Filtered Data)')
        ax2.set_xlabel('Voting Counts')
        ax2.set_ylabel('Movie Name')
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig2)

        # --- Genre Distribution ---
        # Plot the count of movies for each genre in a bar chart.
        st.markdown("### Genre Distribution")
        genre_counts = final_filtered_df['genre'].value_counts().sort_values(ascending=False)
        fig3, ax3 = plt.subplots(figsize=(12, 7))
        sns.barplot(x=genre_counts.index, y=genre_counts.values, ax=ax3, palette='coolwarm')
        ax3.set_title('Distribution of Movies Across Genres (Filtered Data)')
        ax3.set_xlabel('Genre')
        ax3.set_ylabel('Number of Movies')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig3)

        # --- Average Duration by Genre ---
        # Show the average movie duration per genre in a horizontal bar chart.
        st.markdown("### Average Duration by Genre")
        avg_duration_genre = final_filtered_df.groupby('genre')['duration_minutes'].mean().sort_values(ascending=False)
        fig4, ax4 = plt.subplots(figsize=(12, 8))
        sns.barplot(x=avg_duration_genre.values, y=avg_duration_genre.index, ax=ax4, palette='plasma')
        ax4.set_title('Average Movie Duration by Genre (Minutes) (Filtered Data)')
        ax4.set_xlabel('Average Duration (Minutes)')
        ax4.set_ylabel('Genre')
        plt.tight_layout()
        st.pyplot(fig4)

        # --- Voting Trends by Genre (Average Voting Counts) ---
        # Visualize average voting counts across different genres.
        st.markdown("### Average Voting Counts by Genre")
        avg_votes_genre = final_filtered_df.groupby('genre')['voting_counts'].mean().sort_values(ascending=False)
        fig5, ax5 = plt.subplots(figsize=(12, 8))
        sns.barplot(x=avg_votes_genre.values, y=avg_votes_genre.index, ax=ax5, palette='magma')
        ax5.set_title('Average Voting Counts by Genre (Filtered Data)')
        ax5.set_xlabel('Average Voting Counts')
        ax5.set_ylabel('Genre')
        plt.tight_layout()
        st.pyplot(fig5)

        # --- Rating Distribution ---
        # Display a histogram or boxplot of movie ratings.
        st.markdown("### Rating Distribution")
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        sns.histplot(final_filtered_df['rating'], kde=True, bins=10, ax=ax6, color='skyblue')
        ax6.set_title('Distribution of IMDb Ratings (Filtered Data)')
        ax6.set_xlabel('Rating')
        ax6.set_ylabel('Number of Movies')
        plt.tight_layout()
        st.pyplot(fig6)

        # --- Genre-Based Rating Leaders ---
        # Highlight the top-rated movie for each genre in a table.
        st.markdown("### Top-Rated Movie for Each Genre")
        if not final_filtered_df.empty:
            # Find the movie with the highest rating for each genre
            idx = final_filtered_df.groupby('genre')['rating'].idxmax()
            genre_rating_leaders = final_filtered_df.loc[idx][['genre', 'movie_name', 'rating', 'voting_counts']].reset_index(drop=True)
            genre_rating_leaders = genre_rating_leaders.sort_values(by='rating', ascending=False)
            st.dataframe(genre_rating_leaders)
        else:
            st.info("No data available to determine genre-based rating leaders.")

        # --- Most Popular Genres by Voting ---
        # Identify genres with the highest total voting counts in a pie chart.
        st.markdown("### Most Popular Genres by Total Voting Counts")
        # Group by genre and sum voting counts
        total_votes_by_genre = final_filtered_df.groupby('genre')['voting_counts'].sum().sort_values(ascending=False)
        
        # Limit to top N genres for readability in pie chart, group others into 'Other'
        top_n_genres_for_pie = 10 
        if len(total_votes_by_genre) > top_n_genres_for_pie:
            other_votes = total_votes_by_genre.iloc[top_n_genres_for_pie:].sum()
            total_votes_by_genre = total_votes_by_genre.head(top_n_genres_for_pie)
            if other_votes > 0:
                total_votes_by_genre['Other'] = other_votes

        fig7, ax7 = plt.subplots(figsize=(10, 10))
        # Use autopct for percentages, startangle for orientation, wedgeprops for borders
        ax7.pie(total_votes_by_genre, labels=total_votes_by_genre.index, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
        ax7.set_title('Distribution of Total Voting Counts by Genre (Filtered Data)')
        ax7.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.tight_layout()
        st.pyplot(fig7)

        # --- Duration Extremes ---
        # Use a table or card display to show the shortest and longest movies.
        st.markdown("### Duration Extremes: Shortest and Longest Movies")
        if not final_filtered_df.empty:
            shortest_movie = final_filtered_df.loc[final_filtered_df['duration_minutes'].idxmin()]
            longest_movie = final_filtered_df.loc[final_filtered_df['duration_minutes'].idxmax()]

            col_short, col_long = st.columns(2)
            with col_short:
                st.info("#### Shortest Movie 📉")
                st.write(f"**Movie:** {shortest_movie['movie_name']}")
                st.write(f"**Genre:** {shortest_movie['genre']}")
                st.write(f"**Duration:** {shortest_movie['duration_minutes']} minutes")
                st.write(f"**Rating:** {shortest_movie['rating']}")
            with col_long:
                st.warning("#### Longest Movie 📈")
                st.write(f"**Movie:** {longest_movie['movie_name']}")
                st.write(f"**Genre:** {longest_movie['genre']}")
                st.write(f"**Duration:** {longest_movie['duration_minutes']} minutes")
                st.write(f"**Rating:** {longest_movie['rating']}")
        else:
            st.info("No data available to determine duration extremes.")

        # --- Ratings by Genre (Comparison) ---
        # Compare the average ratings for each genre.
        # While a heatmap is mentioned, for simple comparison of average ratings per genre, a bar chart is clearer.
        # A heatmap would be more suitable if comparing ratings across two categorical variables (e.g., Genre vs. Decade).
        st.markdown("### Average Ratings by Genre (Comparison)")
        avg_ratings_genre = final_filtered_df.groupby('genre')['rating'].mean().sort_values(ascending=False)
        fig9, ax9 = plt.subplots(figsize=(12, 8))
        sns.barplot(x=avg_ratings_genre.values, y=avg_ratings_genre.index, ax=ax9, palette='cool_r') # 'cool_r' is a reversed coolwarm
        ax9.set_title('Average Ratings by Genre (Filtered Data)')
        ax9.set_xlabel('Average Rating')
        ax9.set_ylabel('Genre')
        plt.tight_layout()
        st.pyplot(fig9)


        # --- Correlation Analysis: Ratings vs. Voting Counts ---
        # Analyze the relationship between ratings and voting counts using a scatter plot.
        st.markdown("### Rating vs. Voting Counts (Correlation)")
        fig10, ax10 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='voting_counts', y='rating', data=final_filtered_df, ax=ax10, hue='genre', size='duration_minutes', sizes=(20, 400), alpha=0.7)
        ax10.set_title('Rating vs. Voting Counts (Filtered Data)')
        ax10.set_xlabel('Voting Counts (Log Scale)')
        ax10.set_ylabel('Rating')
        ax10.set_xscale('log') # Use log scale for voting counts as values can vary widely, making small counts hard to see
        plt.grid(True, which="both", ls="--", c='0.7')
        plt.tight_layout()
        st.pyplot(fig10)



# %%

# %%
