import requests
import bs4
from bs4 import BeautifulSoup
import urllib.request
import time
from random import choice
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import os
import pymysql.cursors


"""
host - portaljobs.database.windows.net:1433d - 
db - portaljobs
id - nwadmin
pass - adhoc@#@!123
"""


desktop_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36']
USER_AGENT = {'User-Agent': choice(desktop_agents)}

#extracting urls for alphabetical order of company names

def browse_all_companies_list(companies_urls= []):
	try:
		page = requests.get("https://www.naukri.com/top-company-jobs", headers= USER_AGENT, timeout=10)
		if page.status_code==200:
			soup = BeautifulSoup(page.text, 'lxml')
			for div in soup.find_all("div", attrs={"class":"tabs"}):
				for a in div.find_all("a", attrs={"class":"tab"}):
						#company_initials.append(a.get_text())
						companies_urls.append(a.get('href'))
			companies_urls.pop(0)
			return browse_company_names(companies_urls)
		else:
			return browse_all_companies_list()	


	except Exception as e:
		return browse_all_companies_list()

	finally:
		time.sleep(20)
		return "timeout"

#extracting all company names and links of companies on naukri

def browse_company_names(companies_urls, company_names = [], company_links = []):
	for urls_company in companies_urls:
		try:
			page_next = requests.get(urls_company, headers= USER_AGENT, timeout=10)
			if page_next.status_code==200:
				soup1 = BeautifulSoup(page_next.text, 'lxml')
				for div2 in soup1.find_all("div", attrs={"id":"tabs_job"}):
					for div3 in div2.find_all("div", attrs={"id":"tabJ-A"}):
						for link in div3.find_all("a"):
							company_names.append(link.get_text())
							company_links.append(link.get('href'))
		except:
			return browse_company_names()
	return jobs_list_by_companies(company_links)

#entering companie's naukri urls for job list

def jobs_list_by_companies(company_links, company_jobs_urls= [], job_title= [], job_location= [], job_experience= []):
	for job_search in company_links:
		try:
			page_company = requests.get(job_search, headers= USER_AGENT, timeout=10)
			if page_company.status_code==200:
				soup2 = BeautifulSoup(page_company.text, 'lxml')
				for div_joblist in soup2.find_all("div", attrs={"class":"row"}):
					for a_joblist in div_joblist.find_all("a", attrs={"class":"content"}):
						company_jobs_urls.append(a_joblist.get('href'))
						for job_opening in a_joblist.find_all('li', attrs= {"class":"desig"}):
							job_title.append(job_opening.get('title'))
						for span in a_joblist.find_all('span', attrs= {"class":"loc"}):
							job_location.append(span.get_text())
						for span2 in a_joblist.find_all('span', attrs= {"class":"exp"}):
							job_experience.append(span2.get_text())
			else:
				return jobs_list_by_companies()
		except Exception as e2:
			return jobs_list_by_companies()
	return job_title,job_experience, job_location, jobs_details(company_jobs_urls)
	

#opening jobs list and extracting details of job

def jobs_details(company_jobs_urls, salary=[], skills= [], industry= []):
	for jobs_by_companies in company_jobs_urls:
		try:
			page_jobs = requests.get(jobs_by_companies, headers= USER_AGENT, timeout=10)
			if page_jobs.status_code==200:
				soup3= BeautifulSoup(page_jobs.text, 'lxml')
				div_description= soup3.find("div", attrs={"class":"JD"})
				ul= div_description.find('ul', attrs= {"class":"listing mt10 wb"})
				description= ul.get_text()
				div2_description= div_description.find('div', attrs= {"class":"jDisc mt20"})
				for p in div2_description.find_all('p'):
					for span_salary in p.find_all('span', attrs= {"class":"salary"}):
						salary.append(span_salary.get_text())
					for span_industry in p.find_all('span', attrs={"itemprop":"industry"}):
						industry.append(span_industry.get_text())
				div3_skills= div_description.find('div', attrs= {"class":"ksTags"})
				for a_description in div3_skills.find_all('a'):
					skills.append(a_description.get_text())
			else:
				return jobs_details
		except Exception as e3:
			return jobs_details()
	return description, salary, skills, industry
				
		
browse_all_companies_list()
