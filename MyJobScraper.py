import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_jobs(base_url, max_pages=5, delay=2):
    """
    Scrapes job postings from a job board.

    Args:
        base_url (str): The base URL of the job board page.
        max_pages (int): The maximum number of pages to scrape.
        delay (int): Delay between requests to avoid getting blocked.

    Returns:
        list: A list of dictionaries containing job information.
    """
    jobs_scraped = []
    current_page = 1

    while current_page <= max_pages:
        print(f"Scraping page {current_page}...")

        # Construct the URL correctly using `&p=` pagination
        url = f"{base_url}&p={current_page}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}. Status code: {response.status_code}")
            break

        # Debugging: Print part of the page source to verify correct content
        #print("Page source (first 500 chars):\n", response.text[:500])

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('article', class_='job')  # Verify correct class selector

        if not jobs:
            print("No job postings found on this page. Stopping...")
            break
        else:
            for job in jobs:
                jobTitle = job.find('a', title=True)
                company = job.find('p', class_='company')
                location = job.find('ul', class_='location')
                salary = job.find('ul', class_='salary')

                job_info = {
                    'Job Title': jobTitle.text.strip() if jobTitle else 'Job title not found!',
                    'Company': company.text.strip() if company else 'Company not found!',
                    'Location': location.find('li').text.strip() if location else 'Location not found!',
                    'Salary': salary.find('li').text.strip() if salary else 'Salary not found!',
                }
                jobs_scraped.append(job_info)

        # Delay to prevent overwhelming the server
        time.sleep(delay)
        current_page += 1

    return jobs_scraped

def save_jobs_to_csv(jobs, filename='jobs_scraped.csv'):
    """
    Saves job data to a CSV file.

    Args:
        jobs (list): A list of dictionaries containing job information.
        filename (str): The name of the CSV file to save the data.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Job Title', 'Company', 'Location', 'Salary']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for job in jobs:
            writer.writerow(job)

    print(f"Job data has been saved to '{filename}'.")

# Main script
if __name__ == '__main__':
    base_url = input("Enter the URL of the job board page: ").strip()
    # Copy & paste this as input: https://www.careerjet.com/jobs?s=software+engineer&l=California&nw=1
    jobs_scraped = scrape_jobs(base_url, max_pages=14, delay=5)  # Increase pages and delay if needed
    if jobs_scraped:
        save_jobs_to_csv(jobs_scraped)
    else:
        print("No jobs were scraped.")
