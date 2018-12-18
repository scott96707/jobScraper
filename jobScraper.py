import time
import csv
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.indeed.com/jobs?q=Python&l=Denver%2C+CO&sort=date')

soup = BeautifulSoup(page.text, 'html.parser')

f = csv.writer(open('Jobs.csv', 'w'))
f.writerow(['Job', 'Company'])

#job_name_list = soup.find(id="resultsCol")
#job_name_list_items = job_name_list.find_all('h2', class_="jobtitle")

pages = []

for i in range(0, 30, 10):
    url = 'https://www.indeed.com/jobs?q=Python&l=Denver%2C+CO&sort=date&start=' + str(i)
    pages.append(url)

for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    job_name_list = soup.find(id="resultsCol")
    job_name_list_items = job_name_list.find_all('h2', class_="jobtitle")
    
    for job in job_name_list_items:
        print(job.a.text())
    '''
    for job_name in job_name_list_items:
        names = job_name.contents[0]
        #companies = 'https://web.archive.org' + job_name.get('href')
        print(names)
        #f.writerow([names])
        '''
