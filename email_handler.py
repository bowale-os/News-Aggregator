# email_handler.py
import os
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv('APP_PASSWORD')

# Email sending function
def send_email(subject, body, to_email):
    from_email = "danbowale@gmail.com"
    from_password = secret_key  

    # Prepare the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
        print(f"Email sent to {to_email}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication error: Check your email/password or enable App Passwords.")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
    except Exception as e:
        print(f"❌ General error sending email: {e}")
#function to get database connection

# Function to fetch subscriptions and send email notifications
def send_keyword_news():
    db_path = os.path.abspath("news.db")
    with sqlite3.connect(db_path, check_same_thread=False) as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT email, keyword FROM user_subscriptions')
        subscriptions = cursor.fetchall()

        for sub in subscriptions:
            email, keyword = sub
            # Here you would fetch the latest news articles based on the keyword
            cursor.execute("""
                SELECT * FROM articles WHERE title LIKE ? ORDER BY published_at DESC LIMIT 5
            """, ('%' + keyword + '%',))
            articles = cursor.fetchall()

            if articles:
                email_body = f"Latest news articles for keyword '{keyword}':\n\n"
                for article in articles:
                    email_body += f"Title: {article[1]}\nSource: {article[2]}\nURL: {article[3]}\nPublished At: {article[4]}\n\n"
                
                send_email(f"Latest News for {keyword}", email_body, email)
            else:
                send_email(f"No news found for {keyword}", f"No articles found for your keyword '{keyword}'.", email)
