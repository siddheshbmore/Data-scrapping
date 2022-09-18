from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import re
import csv


# The chromedriver should be in the same directory
driver = webdriver.Chrome('./chromedriver')
# page_url = "https://www.indeed.com/jobs?q=Data+Scientist&l=Silicon+Valley&start=" + str(10)
# driver.get(page_url)

# wait until the page is loaded
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resultsBody")))


# Remove non-alphabets including punctuations and numbers from job description
pattern = re.compile(r'[^a-zA-Z]', re.UNICODE)


with open("jobs_indeed.csv", "a", encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file, delimiter=',')

    for job_type in ["Data+Scientist", "software+engineer"]:
        for page in range(0, 2): # only 2 pages but change this for more pages (each page has 15 jobs listed)
            page_url = "https://www.indeed.com/jobs?q="+ job_type +"&l=Silicon+Valley&start=" + str(page*10)
            driver.get(page_url)
            rows = driver.find_elements_by_class_name('row')
            for row in rows:
                driver.switch_to.default_content()
                row.click()
                # wait
                # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "viewJobSSRRoot")))
                driver.switch_to.frame(driver.find_element_by_id("vjs-container-iframe"))
                content = driver.find_element_by_id('jobDescriptionText')
                job_desc = content.text
                job_desc = content.text
                # remove non-alphabets
                job_desc = pattern.sub(' ', job_desc)
                job_desc = re.sub(r'\s+', ' ', job_desc).strip()
                # Convert to lowercase
                job_desc = job_desc.lower()

                # write to csv
                csv_writer.writerow([job_desc, job_type.replace("+", " ")])
                driver.implicitly_wait(2) # seconds
            
            print('Page number ', page, ' read')
            

driver.close()

