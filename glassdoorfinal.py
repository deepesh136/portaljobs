from lxml import html, etree
import requests
from bs4 import BeautifulSoup
import re

total = 1
headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'accept-encoding': 'gzip, deflate, sdch, br',
           'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
           'referer': 'https://www.glassdoor.com/',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
           'Cache-Control': 'no-cache',
           'Connection': 'keep-alive'
           }

job_litsting_url = "https://www.glassdoor.co.in/Job/india-jobs-SRCH_IL.0,5_IN115.htm"
job_listing_main = "https://www.glassdoor.co.in/Job/india-jobs-SRCH_IL.0,5_IN115"
base_url = "https://www.glassdoor.com"

response = requests.post(job_litsting_url, headers=headers)
parser = html.fromstring(response.text)
soup = BeautifulSoup(response.text, "lxml")
number_box = soup.find("div", attrs={"class": "cell middle hideMob padVertSm"})
number = number_box.text.strip()
total = int(number[9:])

job_listings = []

for i in range(1,total):
    job_listings = []

    job_litsting_url = job_listing_main+"_IP"+str(i)+".htm"
    print(job_litsting_url)
    response = requests.post(job_litsting_url, headers=headers)
    parser = html.fromstring(response.text)


    XPATH_ALL_JOB = '//li[@class="jl"]'
    XPATH_NAME = './/a/text()'
    XPATH_JOB_URL = './/a/@href'
    XPATH_LOC = './/span[@class="subtle loc"]/text()'
    XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
    XPATH_SALARY = './/span[@class="green small"]/text()'

    listings = parser.xpath(XPATH_ALL_JOB)
    for job in listings:
        raw_job_name = job.xpath(XPATH_NAME)
        raw_job_url = job.xpath(XPATH_JOB_URL)
        raw_lob_loc = job.xpath(XPATH_LOC)
        raw_company = job.xpath(XPATH_COMPANY)
        raw_salary = job.xpath(XPATH_SALARY)

        # Cleaning data
        job_name = ''.join(raw_job_name).strip('–') if raw_job_name else None
        job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
        raw_state = re.findall(",\s?(.*)\s?", job_location)
        state = ''.join(raw_state).strip()
        raw_city = job_location.replace(state, '')
        city = raw_city.replace(',', '').strip()
        company = ''.join(raw_company).replace('–', '')
        salary = ''.join(raw_salary).strip()
        job_url = raw_job_url[0] if raw_job_url else None

        #Extracting Description
        try:
            response = requests.post(base_url+job_url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            desc_box = soup.find("div", attrs={"class": "jobDescriptionContent desc module pad noMargBot"})
            desc = desc_box.text.strip()
        except AttributeError:
            pass

        jobs = {
            "Name": job_name,
            "Company": company,
          #  "State": state,
            "City": city,
          #  "Salary": salary,
          #  "Location": job_location,
            "Url": job_url,
            "Description": desc
        }
        job_listings.append(jobs)

    print (job_listings)
