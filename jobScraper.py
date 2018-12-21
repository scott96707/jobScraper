import time
import csv
import requests
import urllib
from bs4 import BeautifulSoup

class JobScraper:
    keywords = ""
    number_of_pages = 0
    pages = []

    def getKeywords(self):
        JobScraper.keywords = urllib.parse.quote_plus(input('Enter search terms: '))

    def numberOfPages(self):
        try:
            JobScraper.number_of_pages = (int(input("Enter the number of pages: "))) * 10
        except ValueError:
            print("Input an integer. Try again.")
            exit()
        if JobScraper.number_of_pages > 200:
            JobScraper.number_of_pages //= 10
            print(str(JobScraper.number_of_pages) + " pages are way too many. Try for under 20")
            exit()

    def getPages(self, keywords, number_of_pages):
        # Gather URLs for each page
        for i in range(0, number_of_pages, 10):
            url = 'https://www.indeed.com/jobs?q='+ keywords +'&l=Denver%2C+CO&sort=date&start=' + str(i)
            JobScraper.pages.append(url)

    def parsePages(self, pages):   
        # Loop to get and write cards with job info from web pages
        f = csv.writer(open('Jobs.csv', 'w'))
        f.writerow(['Job Title', 'Company', 'Location', 'Posted Date', 'Summary', 'Link'])
        for item in JobScraper.pages:
            try:
                page = requests.get(item)
            except requests.ConnectionError: 
                print("Connection Error. Check your internet connection.")
                exit()
            soup = BeautifulSoup(page.text, 'html.parser')
            all_job_posts = soup.find(id="resultsCol")
            cards = all_job_posts.find_all(class_="jobsearch-SerpJobCard")
            time.sleep(1)
            # Parse job specifics from each job card, post to csv
            for posts in cards:
                job_titles = posts.a.get_text()        
                company = posts.find('span', class_="company").get_text().strip()
                # Location and posted_date contained in either spans or divs
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
        

def main():
    j = JobScraper()
    j.getKeywords()
    j.numberOfPages()
    j.getPages(j.keywords, j.number_of_pages)
    j.parsePages(j.pages)

if __name__ == "__main__":
    main()
