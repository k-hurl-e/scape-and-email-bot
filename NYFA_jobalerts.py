from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os

SCRAPE_URL = os.getenv('SCRAPE_URL')
API_KEY = os.getenv('API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')

def check_jobs(driver):
    # Navigate to the page
    driver.get(SCRAPE_URL)

    # Let the page load completely
    driver.implicitly_wait(10)  # Waits for 10 seconds

    # Parse the fully loaded page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all job postings (adjust the class name based on the actual HTML structure)
    jobs = soup.find_all('div', class_="RegularJob")  # Adjust this selector if necessary

    job_results = []

    for job in jobs:
        title = job.find('h3').text if job.find('h3') else "No title"
        link = job.find('a')['href'] if job.find('a') else "No link"
        company = job.find('b', class_='nyfa-orange-color').text if job.find('b') else "No company"
        description = job.find('div', class_='grey').text.strip() if job.find('div', class_='grey') else "No description"

        job_results.append(f"Title: {title}\nCompany: {company}\nDescription: {description}\nLink: nyfa.org{link}")
        
    return job_results

# Function to send email using Mailgun
def send_email(subject, body):
    api_key = os.getenv("API_KEY")  # Use environment variables
    domain = os.getenv("MAILGUN_DOMAIN")
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")

    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={"from": sender,
              "to": [recipient],
              "subject": subject,
              "text": body})

# Main function
def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = "/usr/bin/google-chrome"  # Specify the path to the Chrome binary


    driver = webdriver.Chrome(options=options)
    
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
