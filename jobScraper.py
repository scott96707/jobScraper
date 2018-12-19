import time
import csv
import requests
import urllib
from bs4 import BeautifulSoup

class jobScraper:
    # Get user input for search terms and # of pages
    print()
    keywords = urllib.parse.quote_plus(input('Enter search terms: '))
    try:
        number_of_pages = (int(input("Enter the number of pages: "))) * 10
    except ValueError:
        print("Invalid number, try again.")
        exit()
    if number_of_pages > 200:
        number_of_pages //= 10
        print(str(number_of_pages) + " pages is way too many. Try for under 20")
        exit()
    
    # Create csv file to collect data
    f = csv.writer(open('Jobs.csv', 'w'))
    f.writerow(['Job Title', 'Company', 'Location', 'Posted Date', 'Summary', 'Link'])

    pages = []

    # Gather URLs for each page
    for i in range(0, number_of_pages, 10):
        url = 'https://www.indeed.com/jobs?q=' + keywords +'&l=Denver%2C+CO&sort=date&start=' + str(i)
        pages.append(url)

    # Loop to fetch page URLs, inner loop to gather and write data
    for item in pages:
        page = requests.get(item)
        soup = BeautifulSoup(page.text, 'html.parser')
        all_job_posts = soup.find(id="resultsCol")
        cards = all_job_posts.find_all(class_="jobsearch-SerpJobCard")
        time.sleep(1)

        # Get job specifics from each job card, post to csv
        for posts in cards:
            job_titles = posts.a.get_text()        
            company = posts.find('span', class_="company").get_text().strip()
            #Location and posted_date contained in either spans or divs
            try:
                location = posts.find('span', class_="location").get_text()
            except AttributeError:
                location = posts.find('div', class_="location").get_text()
            try:
                posted_date = posts.find('span', class_="date").get_text()
            except AttributeError:
                posted_date = "No date listed"
            summary = posts.find('span', class_="summary").get_text().strip()
            link_root = posts.get('data-jk')
            link = "https://www.indeed.com/viewjob?jk=" + link_root
            f.writerow([job_titles, company, location, posted_date, summary, link])
