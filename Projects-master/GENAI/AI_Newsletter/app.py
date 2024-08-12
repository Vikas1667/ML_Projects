from flask import Flask, request, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from newsletter_extraction import fetch_ai_news,news_fetcher
import sqlite3
import webbrowser

NEWS_API_URL = " https://newsapi.ai/v1/articles"  # Example endpoint for AI news
app = Flask(__name__)


# Email configuration
sender_email = "vikas.kumbharkar308@gmail.com"
# receiver_email = "vikas.kumbharkar308@gmail.com"
password = ""
# password = ""
# conn = sqlite3.connect('newsletterdb.db',check_same_thread=False)
# conn = sqlite3.connect('E:/mydatabase.db')  # Windows
# cursor = conn.cursor()

# Function to fetch AI news
# def fetch_ai_news():
#     try:
#         params = {
#             'apiKey': API_KEY,
#             'category': 'technology',
#             'language': 'en',
#             'pageSize': 10
#         }
#         response = requests.get(NEWS_API_URL, params=params)
#         articles = response.json().get('articles', [])
#
#         for article in articles:
#             store_in_faiss(article)
#     except Exception as e:
#         print("Unable to fetch news for faiss")

def rendering_template():
    ## we are check if datetime
    # Attach the HTML content
    # articles = fetch_ai_news()

    articles=news_fetcher()
    html_content = render_template('newsletter.html', articles=articles)
    return html_content

# Function to send email
def send_email(email):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "AI News Newsletter"



    # with open('saving.html', 'w') as f:
    #     f.write(html_content)
    # webbrowser.open('saving.html')
    try:
        html_content = rendering_template()
        msg.attach(MIMEText(html_content, 'html'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"Email sent to {email} successfully!")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

# HTML page for subscription
@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        # Store the email in your database
        send_email(email)  # Send the newsletter email
        return f"Thank you for subscribing with {email}!"
        # return ("<p>" + "</p><p>".join(list) + "</p>")

    return render_template('subscribe.html')

# Main execution
if __name__ == "__main__":
    app.run(debug=True)
