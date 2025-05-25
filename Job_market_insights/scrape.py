from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd

# Set up Selenium WebDriver
driver = webdriver.Chrome()  

# Function to scrape LinkedIn Jobs
def scrape_linkedin():
    linkedin_jobs = []
    search_url = "https://www.linkedin.com/jobs/search/?keywords=web%20scraping"
    driver.get(search_url)
    time.sleep(5)  # Allow page to load

    # Scroll to load more job postings
    for _ in range(3):  # Adjust for more jobs
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(3)

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("div", class_="base-card")

    for job in job_cards:
        title = job.find("h3", class_="base-search-card__title")
        company = job.find("h4", class_="base-search-card__subtitle")
        location = job.find("span", class_="job-search-card__location")
        link = job.find("a", class_="base-card__full-link")

        if title and company and location and link:
            linkedin_jobs.append({
                "Job Title": title.text.strip(),
                "Company": company.text.strip(),
                "Location": location.text.strip(),
                "Source": "LinkedIn",
                "Job Link": link["href"]
            })

    return linkedin_jobs

linkedin_data = scrape_linkedin()
df = pd.DataFrame(linkedin_data)
df.to_csv("job_market_analysis.csv", index=False)

# Close driver
driver.quit()

print("✅ Job data scraped and saved to 'job_market_analysis.csv'.")