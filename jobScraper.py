import time
import csv
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.indeed.com/jobs?q=Python&l=Denver%2C+CO&sort=date')

soup = BeautifulSoup(page.text, 'html.parser')

f = csv.writer(open('Jobs.csv', 'w'))
f.writerow(['Number', 'Job', 'Company', 'Location', 'URL'])

pages = []

for i in range(0, 30, 10):
    url = 'https://www.indeed.com/jobs?q=Python&l=Denver%2C+CO&sort=date&start=' + str(i)
    pages.append(url)

for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    card_list = soup.find(id="resultsCol")
    job_name_list_items = card_list.find_all('h2', class_="jobtitle")
    company_name_list_items = card_list.find_all('span', class_="company")

    #This just repeats 1-10, need to fix to go past 10 later
    for j in range(1, len(job_name_list_items)+1):
        f.writerow([j])

    for job_name in job_name_list_items:
        names = job_name.a.get_text()        
        f.writerow([names])
        

    for company_name in company_name_list_items:
        try:
            print(company_name.a.get_text())
        except:
            print(company_name.get_text())
