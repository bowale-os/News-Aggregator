import os
import sqlite3
import streamlit as st
from email_handler import send_keyword_news  # Import the email handler function

# Define the path to the database
db_path = os.path.abspath("news.db")

# Function to get database connection
def get_db_connection():
    return sqlite3.connect(db_path, check_same_thread=False)

# Get the database connection
conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    keyword TEXT NOT NULL
)
"""
            )
conn.commit()



# Streamlit UI
st.title('News Aggregator with Email Subscription')
st.write("Stay updated with the latest news articles.")

#Input for email subscription
email = st.text_input("Enter your email:", key="email_input")

# Input for keyword search
keyword = st.text_input("Search for news articles by keyword:")

#Submit button for email subscription
subscribe_button = st.button("Subscribe to News")
if subscribe_button and email.endswith(".com"):
        if email and keyword:
            #save subscription to database
            cursor.execute("""
                INSERT INTO user_subscriptions (email, keyword)
                VALUES(?,?)
    """,(email, keyword))
            conn.commit()
            st.success("You have successfully subscribed to email alerts!")
        else:
            st.error("Please fill in both fields!")

cursor.execute("SELECT * FROM user_subscriptions")
subscriptions = cursor.fetchall()

if subscriptions:
    st.write("Current Subscriptions:")
    for subscription in subscriptions:
        st.write(f"Email: {subscription[1]} - Keyword: {subscription[2]}")

send_keyword_news()  
st.write("Email notifications sent successfully!")
# Call the function to send email notifications based on subscriptions
# Note: The database connection is not closed here because Streamlit manages the connection across runs.


#Function to delete subscription
def delete_subscription(email, keyword):
    db_path = "news.db"
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM user_subscriptions WHERE email = ? AND keyword = ?", (email, keyword))
        conn.commit()
        
        print(f"Deleted subscription for {email} on keyword '{keyword}'")

# Example Usage
delete_subscription("danny2show@gmail.com", "Code, TypeScript")





