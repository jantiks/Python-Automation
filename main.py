import smtplib
from selenium import webdriver
from bs4 import BeautifulSoup
import Emails

class RequestManager:
    __URl = "https://www.upwork.com/ab/jobs/search/?q=iOS%20swift&sort=recency"

    def getData(self):
        print("Scraping completed")

        driver = webdriver.Firefox()
        driver.get(self.__URl)
        source = driver.page_source
        driver.close()

        return source
class JobPosting:
    title = ""
    link = ""
    budget = ""

    def __init__(self, title, link, budget):
        self.title = title
        self.link = link
        self.budget = budget


manager = RequestManager()
soup = BeautifulSoup(manager.getData(), 'html.parser')

sections = soup.find_all("section")
print("Starting to scrap data")
# Getting job postings
job_postings = []
for section in sections:
    job_postings.append(section.find(
        id=soup.get("jobSearchUtils.jobTileResponsive.JobTileResponsiveController as jobTileResponsiveCtrl")))

# Extracting data form job posting
filtered_postings = []
for posting in job_postings:
    title = posting.find(id=posting.get("job-title m-xs-top-bottom p-sm-right")).text

    budget_arr = posting.find_all("strong")
    if len(budget_arr) == 1:
        budget = budget_arr[0].text
        filtered_postings.append(JobPosting(title=title, budget=budget, link=""))
print("Sending email messages")

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(Emails.sender_email, Emails.password)
for posting in filtered_postings:
    server.sendmail(Emails.sender_email, Emails.reciever_email, "Title: " + posting.title +  " budget " + posting.budget)