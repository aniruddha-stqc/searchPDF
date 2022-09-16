import datetime
import os
import time

import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import globals


def execute():
    script_name = os.path.basename(__file__)
    print(script_name + " : " + "Launching Nu Html Checker in Selenium Gecko Browser headlessly")
    options = Options()
    options.headless = True
    # Invoke Firefox
    driver = webdriver.Firefox(options=options, executable_path=globals.gecko_path, service_log_path=os.devnull)
    # Access Tool site
    driver.get("https://validator.w3.org/nu/")
    # Provide URL to be tested
    driver.find_element_by_id("doc").send_keys(globals.target_website)
    # Click Submit
    driver.find_element_by_id("submit").click()

    print(script_name + " : " + "Scanning target website " + globals.target_website + " for HTML issues")
    time.sleep(globals.time_wait)

    # Collect the rendered page
    page_source = driver.page_source
    # Close the webdriver
    driver.close()

    print(script_name + " : " + "Parsing scan results using Beautiful Soup")
    # Selenium hands over the page source to Beautiful Soup for WebScraping
    page_soup = BeautifulSoup(page_source, "html.parser")
    # Parse the results section
    results = page_soup.find("div", {"id": "results"})

    globals.test_log = "logs/test_log_html.xlsx"
    workbook = xlsxwriter.Workbook(globals.test_log)
    worksheet = workbook.add_worksheet("html_checker")

    print(script_name + " : " + "Parsing HTML errors")

    # Iterate through each result row
    liTags = results.find_all("li")
    excel_row = 0
    worksheet.write(excel_row, 0, "issue_type")
    worksheet.write(excel_row, 1, "issue_summary")
    worksheet.write(excel_row, 2, "issue_location")
    worksheet.write(excel_row, 3, "issue_extract")

    for liTag in liTags:
        excel_row += 1
        issue_type = liTag.p.strong.text.strip()
        issue_summary = liTag.p.span.text.strip()
        issue_location = liTag.find("p", {"class": "location"}).text.strip()
        try:
            issue_extract = liTag.find("p", {"class": "extract"}).text.strip()
        except:
            issue_extract = "Not Applicable"
        worksheet.write(excel_row, 0, issue_type)
        worksheet.write(excel_row, 1, issue_summary)
        worksheet.write(excel_row, 2, issue_location)
        worksheet.write(excel_row, 3, issue_extract)

    print(script_name + " : " + "HTML error count " + str(excel_row))

    workbook.close()

    print(script_name + " : " + "All results written to file " + globals.test_log)


if __name__ == '__main__':
    script_name = os.path.basename(__file__)
    execute()
    print(script_name + " : " + "Finished in " + str(
        (datetime.datetime.now() - globals.time_start).total_seconds()) + " seconds")