# Scape and Email Bot

This repository contains a Python-based bot designed to scrape job listings from specific websites and send email notifications when a new job matching specified criteria is found. This file is configured for tracking job posts on the NYFA (New York Foundation for the Arts) website with specific criteria.

## Features

- **Web Scraping**: Utilizes the `beautifulsoup4` and `lxml` libraries to extract job data from targeted websites.
- **Email Alerts**: Sends email notifications when a new job matching the desired criteria is found.
- **Automation**: Configurable via a YAML file to run on a schedule using tools like cron.
- **Customizable**: Users can define the job search criteria, including job titles, locations, and salary ranges, within the configuration file.

## Requirements

You can install all the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Configuration

The bot is configured via the `main.yml` file. This YAML file allows you to define:

- **Search criteria**: Specify the job titles, locations, and salary ranges.
- **Email settings**: Configure the email sender, recipient, and SMTP server details.
- **Schedule**: Define how often the bot should run.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/k-hurl-e/scape-and-email-bot.git
    cd scape-and-email-bot
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the bot by editing the `main.yml` file to fit your needs.

4. Run the bot:

    ```bash
    python runbot.py
    ```

5. (Optional) Set up a cron job to run the bot automatically at the specified intervals.

If you want to adjust the parameters, simple change the `SCRAPE_URL` with a link that includes all your criteria and adjust the `title`, `link`, `company`, and `description` criteria in `runbot.py` to match the websites HTML. 
