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

try:
	# Connect to the database
	connection = pymysql.connect(host='localhost',
        	                     user='root',
        	                     password='',
        	                     db='portaljobs',
        	                     cursorclass=pymysql.cursors.DictCursor)

	page = requests.get("https://www.naukri.com/top-company-jobs", headers= USER_AGENT, timeout=10)
	if page.status_code==200:
		soup = BeautifulSoup(page.text, 'lxml')
		def browse_jobs_by_Companies(soup):
			companies_urls = []
			company_initials= []
			for div in soup.find_all("div", attrs={"class":"tabs"}):
				#print("loop1")
				for a in div.find_all("a", attrs={"class":"tab"}):
						company_initials.append(a.get_text())
						companies_urls.append(a.get('href'))

			for i in range(1, len(companies_urls)):
				page_next = requests.get(companies_urls[i], headers= USER_AGENT, timeout=10)
				if page_next.status_code==200:
					company_names = []
					company_links = []
					soup1 = BeautifulSoup(page_next.text, 'lxml')
					for div2 in soup1.find_all("div", attrs={"id":"tabs_job"}):
						for div3 in div2.find_all("div", attrs={"id":"tabJ-A"}):
							for link in div3.find_all("a"):
								company_names.append(link.get_text())
								company_links.append(link.get('href'))
					with open("naukri-companies.txt", 'a') as f:
						for j in range(len(company_names)):
							company = company_names[j]
							comlink = company_links[j]
							try:
    								with connection.cursor() as cursor:
									sql1 = "INSERT INTO company_urls (com_name, com_url) VALUES ("+company+", "+comlink+")"
									cursor.execute(sql1)
				else:
					print("page2 error", page_next.status_code)
		browse_jobs_by_Companies(soup)	
	else:
		print(page.status_code)	


except Exception as e:
	print(str(e))

finally:
	time.sleep(20)
	print("timeout")
