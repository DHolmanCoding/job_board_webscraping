import requests
from bs4 import BeautifulSoup
import pandas as pd
import math


def extract_job_title(soup):
    jobs = []
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
            jobs.append(a['title'])
    return jobs


def get_indeed_search_ct(soup):
    num_jobs = str(soup.find_all(name='div', attrs={'id': 'searchCount'})).split('of ')[-1].split(' jobs')[0]
    num_results_pages = math.ceil(int(num_jobs.replace(',', '')) / 16)
    return num_results_pages


def extract_companyName(soup):
    companies = []
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        company = div.find_all(name='span', attrs={'class': 'company'})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name='span', attrs={'class': 'result - link - source'})
            for span in sec_try:
                companies.append(span.text.strip())
    return companies


def extract_location_from_result(soup):
  locations = []
  spans = soup.findAll('span', attrs={'class': 'location'})
  for span in spans:
    locations.append(span.text)
  return locations


def extract_summary_from_result(soup):
  summaries = []
  spans = soup.findAll('span', attrs={'class': 'summary'})
  for span in spans:
    summaries.append(span.text.strip())
  return summaries


job_title = 'Data Scientist'
salary = '20000'
# cities = ['Seattle', 'Portland', 'New York', 'San Francisco']
location = 'New York'
excluded_words = 'senior'

# Process user-defined inputs
job_title = job_title.lower().split(' ')
salary = [salary[::-1][i:i+3][::-1] for i in range(0, len(salary), 3)][::-1]
location = location.lower().split(' ')

URL = 'https://www.indeed.com/jobs?q={}+{}+%24{}%2C{}+-{}&l={}+{}&start=10'.format(*job_title, *salary, excluded_words, *location)
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')

n = get_indeed_search_ct(soup)
page_extensions = [10*i for i in range(n)]

# extract_location_from_result(soup)
summaries = extract_summary_from_result(soup)


max_results_per_city = 100

exit()

# for page in page_extensions:

# companies = extract_companyName(soup)
# titles = extract_jobTitle(soup)
#
# print(companies, '\n', titles)
# print(len(companies), len(titles))
