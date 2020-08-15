import shutil
import sys
import time

from selenium.webdriver.support.wait import WebDriverWait

from ArticlesDataDownloader.download_utilities import download_file_from_click_of_button
from ArticlesDataDownloader.getDriver import getDriver


def download_citations_from_search_link(driver, link, output_directory, output_name_base):
    driver.get(link)
    MAX_PAGES = 50
    for page_no in range(1, MAX_PAGES + 1):
        time.sleep(2)
        export_citations_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//i[@class='icon-quote']"))
        export_citations_button.click()

        time.sleep(1)
        checkboxes = WebDriverWait(driver, 10).until(
            lambda x: x.find_elements_by_xpath("//label[@class='checkbox--primary']/span[@class='label-txt']"))

        for checkbox in checkboxes:
            desired_y = (checkbox.size['height'] / 2) + checkbox.location['y']
            window_h = driver.execute_script('return window.innerHeight')
            window_y = driver.execute_script('return window.pageYOffset')
            current_y = (window_h / 2) + window_y
            scroll_y_by = desired_y - current_y
            driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            checkbox.click()



        next_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//button[text()='Next']"))
        next_button.click()

        ris_option = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[text()='BibTex']"))
        ris_option.click()

        export_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//button[text()='Export']"))

        file = download_file_from_click_of_button(driver, export_button)
        output_filename = output_directory + '/' + output_name_base + '_' + str(page_no) + '.bib'
        if file:
            shutil.move(file, output_filename)

        cancel_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@id='exportCitation']/div/div/button/i[@class='icon-close_thin']"))
        cancel_button.click()

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                lambda x: x.find_element_by_xpath("//a[@aria-label='Next page link']"))
            next_page_button.click()
        except:
            break


def __main():
    output_dir = '.server_files/InputFiles/Willey'
    driver = getDriver(proxyFile='proxy_auth_plugin.zip')

    link = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=%22mutation+testing%22&content=articlesChapters&target=default&startPage=&ConceptID=68'
    download_citations_from_search_link(driver, link, output_dir, 'willey_auto_mutation_testing')

    link = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=%22mutant+analysis%22&startPage=&ConceptID=68'
    download_citations_from_search_link(driver, link, output_dir, 'mutant_analysis')

    link = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=%22mutation+analysis%22&startPage=&ConceptID=68'
    download_citations_from_search_link(driver, link, output_dir, 'mutation_analysis')



if __name__ == '__main__':
    sys.exit(__main())
