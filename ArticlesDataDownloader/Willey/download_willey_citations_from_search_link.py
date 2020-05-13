import shutil
import sys
import time

from selenium.webdriver.support.wait import WebDriverWait

from ArticlesDataDownloader.download_utilities import download_file_from_click_of_button
from ArticlesDataDownloader.getDriver import getDriver


def download_citations_from_search_link(driver, link, output_directory):
    driver.get(link)
    MAX_PAGES = 50
    for page_no in range(1, MAX_PAGES + 1):
        select_all_checkbox = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[@aria-label='Select all articles']"))
        select_all_checkbox.click()

        export_options_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[text()='Export Citation(s)']"))
        export_options_button.click()

        ris_option = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[text()='RIS (ProCite, Reference Manager)']"))
        ris_option.click()

        export_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//button[@form='export-citations-form']"))
        file = download_file_from_click_of_button(driver, export_button)
        output_filename = output_directory + '/willey_auto_search_' + str(page_no) + '.ris'
        if file:
            shutil.move(file, output_filename)

        cancel_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@class='modal__footer-right']/button[@data-dismiss='modal']"))
        cancel_button.click()

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                lambda x: x.find_element_by_xpath("//a[@aria-label='Next page link']"))
            next_page_button.click()
        except:
            break


def __main():
    link = 'https://onlinelibrary.wiley.com/action/doSearch?AllField=%22mutation+testing%22&content=articlesChapters&target=default&startPage=&ConceptID=68'
    output_dir = '/home/l/ArticlesInputFiles/Willey'
    driver = getDriver(proxyFile='proxy_auth_plugin.zip')
    download_citations_from_search_link(driver, link, output_dir)


if __name__ == '__main__':
    sys.exit(__main())
