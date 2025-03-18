import streamlit as st
import sqlite3
import os

# Define the path to the database
db_path = os.path.abspath("news.db")
st.write(f"Using database: {db_path}")

# Function to get database connection (no need to cache)
def get_db_connection():
    return sqlite3.connect(db_path, check_same_thread=False)

# Get the database connection
conn = get_db_connection()
cursor = conn.cursor()

# Streamlit title
st.title('News Aggregator')

# Input for keyword search
keyword = st.text_input("Search for news articles by keyword:")

# Query based on the keyword or display the latest articles
if keyword:
    cursor.execute("SELECT * FROM articles WHERE title LIKE ? ORDER BY published_at DESC", ('%' + keyword + '%',))
    articles = cursor.fetchall()
else:
    st.write("Displaying the latest articles...")
    cursor.execute("SELECT * FROM articles ORDER BY published_at DESC LIMIT 10")
    articles = cursor.fetchall()

# Display articles
for article in articles:
    st.write(f"**Title:** {article[1]}")
    st.write(f"**Source:** {article[2]}")
    st.write(f"**Published At:** {article[4]}")
    st.write(f"[Read more]({article[3]})")
    st.write("---")

# Keep the connection open while Streamlit is running
# Don't close the connection here! Let Streamlit manage it across runs.


# cursor.execute("SELECT COUNT(id) FROM articles")
# categories = cursor.fetchall()
# print(categories)

