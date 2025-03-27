# News Aggregator with Email Subscription

## Overview
The **News Aggregator with Email Subscription** is a Streamlit-based web application designed to keep users updated with the latest news articles. Users can subscribe with their email addresses and specify keywords of interest. The application automatically sends personalized news articles directly to the user's email inbox.

## Key Features
- **User Subscription**: Users can subscribe by providing their email and a keyword of interest.
- **Database Integration**: Uses **SQLite** to store and manage user subscriptions.
- **Automated Email Notifications**: Leverages the `send_keyword_news()` function from `email_handler.py` to send relevant news articles via email.
- **Streamlit Interface**: Provides a simple and interactive web interface for user interaction.

## Installation
### Prerequisites
- Python 3.7 or higher
- Streamlit
- SQLite3

### Clone the Repository
```bash
git clone https://github.com/bowale-os/news-aggregator.git
cd news-aggregator
```

### Create a Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage
### 1. **Run the Application**
```bash
streamlit run app.py
```

### 2. **Subscribe to News**
- Open the Streamlit web interface.
- Enter your email address and a keyword to search for news articles.
- Click **"Subscribe to News"** to save your preferences.

### 3. **View Current Subscriptions**
- The current subscriptions are displayed in the interface.

### 4. **Email Notifications**
- The `send_keyword_news()` function is automatically called to send keyword-specific news articles.

## Database
- The **SQLite** database `news.db` stores user subscriptions with the following schema:

```sql
CREATE TABLE IF NOT EXISTS user_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    keyword TEXT NOT NULL
);
```

## How to Delete a Subscription
The function `delete_subscription()` can be called to remove specific subscriptions by email and keyword.

```python
# Example Usage
delete_subscription("example@gmail.com", "Technology")
```

## Project Structure
```
news-aggregator/
├── app.py
├── email_handler.py
├── news.db
├── requirements.txt
├── README.md
```

## Future Improvements
- Add OAuth or other authentication mechanisms for secure login.
- Implement a scheduling system for sending emails at specific intervals.
- Add support for multiple keywords per user.

## License
This project is licensed under the **MIT License**.

---

**Author:** Daniel Sobowale

