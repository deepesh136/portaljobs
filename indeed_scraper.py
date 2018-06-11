import requests
import bs4
from bs4 import BeautifulSoup
import urllib.request
import time
from random import choice

desktop_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36']
USER_AGENT = {'User-Agent': choice(desktop_agents)}

#getting indeed jobs urls by categories
class getting_complete_indeed_urls():
	def _init_(category= "", indeed_urls= []):
		try:
			page = requests.get("https://www.indeed.co.in/jobs",headers= USER_AGENT, timeout=10) #requesting 1st page
			if page.status_code==200:
				soup = BeautifulSoup(page.text, 'lxml') #parsing 1st page
				for table in soup.find_all(name="table", attrs={"id":"populartable"}):
					for href in table.find_all(name="a"):
						ab= href.get('href')
						bc = ab.replace('-', '+')
						category = bc.replace('/', '')
						for i in range(0, 1010, 10):
							indeed_urls.append("https://www.indeed.co.in/jobs?q=%s&start=%d" % (category, i))
				print(indeed_urls)
				print(len(indeed_urls))

			else:
				print(page.status_code)
		except requests.Timeout as e:
			print(str(e))
		finally:
			time.sleep(30)
	_init_()
