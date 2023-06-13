import webbrowser
import schedule
import time

def open_url():
    url = "https://example.com"  # Replace with your desired URL
    webbrowser.open(url)

# Schedule the job to run every day at 9 PM
schedule.every().day.at("21:00").do(open_url)

while True:
    schedule.run_pending()
    time.sleep(1)
