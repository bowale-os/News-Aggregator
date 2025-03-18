import requests
import sqlite3
import streamlit as st

API_KEY = '7ad8fc5d5de54be1b09d7ebf727673a0'
category = 'health'  

header = {
    'X-Api-Key': '7ad8fc5d5de54be1b09d7ebf727673a0'
}

endpoints = f'https://newsapi.org/v2/top-headlines?country=us&pageSize=50category={category}&apiKey={API_KEY}'
response = requests.get(endpoints)
news_data = response.json()

conn = sqlite3.connect('news.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS aticles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    source TEXT,
    url TEXT UNIQUE,
    published_at TEXT,
    category TEXT
)
""")

def assign_category(title):
    title = title.lower()
    
    if any(word in title for word in ["stock", "market", "economy", "finance"]):
        return "business"
    elif any(word in title for word in ["movie", "music", "entertainment", "celebrity"]):
        return "entertainment"
    elif any(word in title for word in ["covid", "health", "disease", "medicine"]):
        return "health"
    elif any(word in title for word in ["science", "discovery", "research"]):
        return "science"
    elif any(word in title for word in ["soccer", "nba", "football", "tennis"]):
        return "sports"
    elif any(word in title for word in ["ai", "technology", "software", "app"]):
        return "technology"
    else:
        return "general"


for article in news_data["articles"]:
    title = article["title"]
    source = article["source"]["name"]
    url = article["url"]
    published_at = article["publishedAt"]
    try:
        # Insert data into the articles table
        category = assign_category(title)
        cursor.execute("""
        INSERT INTO aticles (title, source, url, published_at, category)
        VALUES (?, ?, ?, ?, ?)
        """, (title, source, url, published_at, category))
    except sqlite3.IntegrityError:
        # Skip duplicates based on the URL (as it's unique)
        continue

conn.commit()


print("Data inserted successfully into the database.")

cursor.execute("SELECT * FROM aticles WHERE category = ? ORDER BY published_at DESC LIMIT 5", ('general',))
cursor.execute("SELECT * FROM aticles WHERE source = ? ORDER BY published_at DESC LIMIT 5", ('BBC.com',))

articles = cursor.fetchall()

for article in articles:
    print(f"Title: {article[1]}")
    print(f"Source: {article[2]}")
    print(f"URL: {article[3]}\n")