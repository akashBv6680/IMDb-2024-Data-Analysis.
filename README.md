# IMDb-2024-Data-Analysis.
Explore 2024 IMDb movie data! 🎬 I scrape titles, genres, ratings, votes &amp; durations using Selenium. Data is cleaned, stored in SQL 💾, and visualized with interactive filters on a Streamlit dashboard 📊. Discover top movies, genre trends &amp; more! ✨🔍

# IMDb 2024 Movie Data Analysis and Visualization

This project is all about exploring 2024 movie data from IMDb! 🎬 I use automated tools to collect movie names, genres, ratings, votes, and durations. After gathering, data is cleaned ✨ & organized by genre into files, then combined into a central SQL database 💾. Finally, an interactive Streamlit dashboard 📊 visualizes trends, allows movie filtering by rating, genre, duration & votes, and helps discover cool insights! 🔍💡

## ✨ Features

* **Interactive Data Filtering:** Filter movies by genre, rating range, duration, and voting counts.
* **Top Movies Analysis:** Identify top 10 movies by rating and voting counts.
* **Genre Insights:** Visualize movie distribution, average duration, and average voting counts across different genres.
* **Rating Distribution:** Understand how movie ratings are spread.
* **Genre Leaders:** See the highest-rated movie for each genre.
* **Popular Genres:** Pie chart showing genres by total voting counts.
* **Duration Extremes:** Easily spot the shortest and longest movies.
* **Rating vs. Voting Correlation:** Scatter plot showing relationship between ratings and votes.
* **Dynamic Data Display:** Filtered data is displayed in a live table.

## 📂 Project Structure

first project/
├── genre_csvs/              # Raw CSV files, organized by genre (input)
├── imdb_2024.db             # Cleaned data in SQLite database (output)
├── imdb_dashboard_app.py    # Streamlit web application code
├── your_data_processing_script.py # Your initial data cleaning and DB loading script (adjust name)
├── README.md                # Project explanation (this file)
├── requirements.txt         # List of Python libraries needed
└── .gitignore               # Files/folders Git should ignore (e.g., .db files, virtual environments)


## 🚀 Setup and Installation

To set up and run this project locally, follow these steps:

### Prerequisites
* **Python 3.x** (latest version recommended)
* **MySQL Server** (running locally)
* **PyCharm** (or another Python IDE/editor)

### Python Environment Setup
1.  **Open PyCharm's Terminal** (at the bottom of the PyCharm window).
2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
3.  **Activate the virtual environment:**
    ```bash
    .\.venv\Scripts\activate
    ```
4.  **Install required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

### MySQL Database Setup
1.  **Log in to your MySQL server** (e.g., using MySQL Shell).
2.  **Create the database:**
    ```sql
    CREATE DATABASE IF NOT EXISTS imdb_db;
    USE imdb_db;
    ```
3.  **Create the `movies` table** (adjust schema if yours is different):
    ```sql
    CREATE TABLE IF NOT EXISTS movies (
        movie_name VARCHAR(255) NOT NULL,
        genre VARCHAR(255),
        rating DECIMAL(3, 1),
        voting_counts INT,
        duration_minutes INT
    );
    ```
4.  **Important:** Remember to replace `"your_mysql_root_password"` in your data processing script with your actual MySQL root password.

## ▶️ How to Run the Project

### Step 1: Prepare and Load Data
1.  **Create a folder** named `genre_csvs` in your project's main directory.
2.  **Place all your raw genre-wise CSV files** (e.g., `Action.csv`, `Drama.csv`, etc.) inside the `genre_csvs` folder.
3.  **Run the data processing script** to clean data and load it into MySQL and SQLite:
    ```bash
    python `GuviMiniPR_data_processing.py.py
    ```
### Step 2: Launch the Streamlit App
1.  **Ensure your virtual environment is active** in the PyCharm Terminal (you should see `(.venv)` at the start of your terminal prompt).
2.  **Run the Streamlit application:**
    ```bash
    streamlit run imdb_dashboard_app.py
    ```
3.  Your default web browser will automatically open, displaying the interactive IMDb 2024 Movie Analysis Dashboard.

## 📺 Demo Video

*(Will add LinkedIn post link here once the video is uploaded)*

## 🤝 Contributing

## 📄 License

This project is open-source. (Consider adding a specific license file like MIT or Apache 2.0 later).
