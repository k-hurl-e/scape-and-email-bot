from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import os

SCRAPE_URL = 'https://www.nyfa.org/jobs/?JobQ=Marketing&location=New+York%2C+NY&salary=60000%2Cinf'
API_KEY = os.getenv('API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Safari/537.36"

def check_jobs(driver):
    # Navigate to the page
    driver.get(SCRAPE_URL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'RegularJob')))

    current_url = driver.execute_script("return window.location.href")
    print(f"Currently parsing: {current_url}")

    # Parse the fully loaded page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all job postings (adjust the class name based on the actual HTML structure)
    jobs = soup.find_all('div', class_="RegularJob")  
    # jobs = soup.find_all('div')

    job_results = []

    # Define today's date, yesterday, and the day before
    today = datetime.today().strftime('%m/%d/%Y')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y')
    day_before_yesterday = (datetime.today() - timedelta(days=2)).strftime('%m/%d/%Y')

    for job in jobs:
        title = job.find('h3').text if job.find('h3') else "No title"
        link = job.find('a').get('href', "No link")
        company = job.find('b', class_='nyfa-orange-color').text if job.find('b') else "No company"
        description_block = job.find('div', class_='grey').text.strip() if job.find('div', class_='grey') else "No description"
        
        # Split the block into individual components
        description_parts = description_block.split('|')
        date = description_parts[0].strip() if len(description_parts) > 0 else "No date"
        location = description_parts[1].strip() if len(description_parts) > 1 else "No location"
        job_type = description_parts[2].strip() if len(description_parts) > 2 else "No job type"
        print(f"today: {today}, job date: {date}")
        # Only add jobs where the date matches today, yesterday, or the day before
        if date in [today, yesterday, day_before_yesterday]:
            job_results.append(f"Title: {title}\nCompany: {company}\nDate: {date}\nLocation: {location}\nType: {job_type}\nLink: nyfa.org{link}")

    return job_results


# Function to send email using Mailgun
def send_email(subject, body):
    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", API_KEY),
        data={"from": EMAIL_SENDER,
              "to": [EMAIL_RECIPIENT],
              "subject": subject,
              "text": body})

# Main function
def main():
    options = Options()
    options.add_argument("--headless=new")  # Use a more realistic headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/usr/bin/google-chrome"  # Specify the path to the Chrome binary
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--enable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    job_alert = check_jobs(driver)
    if job_alert:
        # Combine all job results into a single email body
        email_body = "\n\n".join(job_alert)  # Joins each job entry with two newlines for separation
        response = send_email('New Marketing Job Posting Alert', email_body)
        print(f"Email sent! Status code: {response.status_code}, Response: {response.text}")
    else:
        print("No matching job found.")

    driver.quit()

if __name__ == "__main__":
    main()
