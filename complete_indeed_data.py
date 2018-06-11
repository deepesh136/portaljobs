import indeed_urls_scraper
import requests
import bs4
from bs4 import BeautifulSoup
import time
from random import choice

#desktop_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36']
desktop_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:31.0) Gecko/20100101 Firefox/31.0 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36']
USER_AGENT = {'User-Agent': choice(desktop_agents)}

urls1 = indeed_urls_scraper.extracting_urls()
#print(urls1)

def extracting_by_job(urls1, job_title= [], companies= [], locations= [], salaries= [], job_links= [], description= []):
	for page_urls in urls1:
		try:
			page_entered = requests.get(page_urls, headers= USER_AGENT, timeout=10)
			if page_entered.status_code==200:
				print("if condition")
				soup_entered= BeautifulSoup(page_entered.text, 'lxml')
				for div in soup_entered.find_all(name="div", attrs={"class":"row"}):
					for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
						job_title.append(a.get('title'))
						job_links.append(a.get('href')) 
					company = div.find_all(name="span", attrs={"class":'company'})
					if len(company) > 0:
						for b in company:
							companies.append(b.text.strip())
					else:
						sec_try = div.find_all(name="span", attrs={"class":'result-link-source'})
						for span in sec_try:
							companies.append(span.text.strip())
					for location in div.find_all(name="span", attrs={"class":'location'}):
						locations.append(location.text.strip())
					salary = div.find_all(name="span", attrs={"class":'no-wrap'})
					if len(salary) > 0:
						for c in salary:
							salaries.append(c.text.strip())
					else:
						salaries.append("not provided by recruiter")
					for span_description in div.find_all('span', attrs={"class":"summary"}):
						description.append(span_description.get_text())
			else:
				return extracting_by_job
		except Exception as e:
			return extracting_by_job

		finally:
			time.sleep(10)
		return job_title, companies, locations, salaries, description
		#return job_links for job complete description
extracting_by_job()

#if description needed
'''
def browse_job_description(job_links, desc= ""):
	for info in job_links:
		try:
			job_page= requests.get(info, headers= USER_AGENT, timeout=30)
			if job_page.status_code==200:
				soup_info= BeautifulSoup(job_page.text, 'lxml')
				div_info= soup_info.find_all('div', attrs={"class":"jobsearch-JobComponent-description icl-u-xs-mt--md"}):
				p = div_info.find_all('p')
				desc= p.get_text()
'''

