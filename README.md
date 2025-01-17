# Job Scraper README

## Overview
This script scrapes job listings from CareerJet (or similar job boards) using Python's `requests` and `BeautifulSoup` libraries. The collected data includes job titles, companies, locations, and salaries, which are then saved into a CSV file. 

## Features
- **Scrapes multiple pages** of job listings (default: 14 pages).
- **Handles pagination** using the `&p=` parameter.
- **Restricts results to the last 24 hours** using the `&nw=1` parameter.
- **Avoids blocking** by using headers and a delay.
- **Extracts structured data** using `BeautifulSoup`.
- **Saves results** into a CSV file.

## Installation
Ensure you have Python installed, then install the necessary dependencies:

```sh
pip install requests beautifulsoup4
```

## Usage
Run the script and input the base URL for the job search page:

```sh
python MyJobScraper.py
```

### Example Input
```
https://www.careerjet.com/jobs?s=software+engineer&l=California&nw=1
```

The script will then scrape job listings and save them in `jobs_scraped.csv`.

### Restricting Results to the Last 24 Hours
By appending `&nw=1` to the URL, the script will **only fetch jobs posted in the last 24 hours**. This prevents scraping an overwhelming number of job offers while ensuring the most recent listings are collected.

## Explanation of Key Features

### **1. Why Use Headers?**
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
```
#### **Purpose:**
- Websites often block requests from bots that do not provide a `User-Agent`.
- This header makes our request **appear like a real web browser**.

#### **Breakdown of the Header:**
- `Mozilla/5.0` → Mimics a standard browser request.
- `Windows NT 10.0; Win64; x64` → Tells the site we are using a **Windows 10 64-bit OS**.
- `AppleWebKit/537.36` → The rendering engine used by **Google Chrome**.
- `Chrome/91.0.4472.124` → Specific Chrome browser version.
- `Safari/537.36` → Included because Chrome is based on Safari’s WebKit engine.

### **2. Why Check for `response.status_code != 200`?**
```python
if response.status_code != 200:
    print(f"Failed to fetch page {current_page}. Status code: {response.status_code}")
    break
```
#### **Purpose:**
- Ensures the request was **successful** before parsing the page.
- `200` means **OK**; any other code (like `404` or `403`) means an error.
- If we don’t check this, the script might try to scrape a **failed or blocked page**.

### **3. Using `BeautifulSoup` to Parse HTML**
```python
soup = BeautifulSoup(response.text, 'html.parser')
jobs = soup.find_all('article', class_='job')
```
#### **Parameters Explained:**
- `response.text` → The raw HTML content of the webpage.
- `'html.parser'` → Tells `BeautifulSoup` to use Python’s built-in HTML parser.
- `soup.find_all('article', class_='job')` → Searches for **all `<article>` tags** with `class='job'`, which contain job listings.

### **4. Extracting Job Information from HTML**
```python
for job in jobs:
    jobTitle = job.find('a', title=True)
    company = job.find('p', class_='company')
    location = job.find('ul', class_='location')
    salary = job.find('ul', class_='salary')
```
#### **Why Use `title=True` and `class_`?**
- `job.find('a', title=True)` → Finds the job **title**, usually inside an `<a>` (anchor) tag.
- `job.find('p', class_='company')` → Finds the **company name** inside a `<p>` tag with `class='company'`.
- `job.find('ul', class_='location')` → Finds **location details**, which are inside an unordered list (`<ul>`).
- `job.find('ul', class_='salary')` → Extracts **salary details**, often stored in `<ul>` elements.

**HTML Structure Example:**
```html
<article class="job">
    <a title="Software Engineer">Software Engineer</a>
    <p class="company">Google</p>
    <ul class="location"><li>San Francisco, CA</li></ul>
    <ul class="salary"><li>$120,000 per year</li></ul>
</article>
```

### **5. Why Use Delay?**
```python
time.sleep(delay)
```
#### **Purpose:**
- Prevents **overloading the website** with too many rapid requests.
- Many sites block scrapers that send requests too quickly.
- Default **delay is 5 seconds**, but it can be increased if needed.

## Output
After scraping, the script creates `jobs_scraped.csv` containing:
```csv
Job Title,Company,Location,Salary
Software Engineer,Google,San Francisco, CA,$120,000 per year
Backend Developer,Microsoft,Seattle, WA,$110,000 per year
...
```

## Notes
- Ensure you **check the website's Terms of Service** before scraping.
- If the script stops working, inspect the **HTML structure** to update class names.


