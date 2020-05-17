import shutil
import sys
import time

from selenium.webdriver.support.wait import WebDriverWait

from ArticlesDataDownloader.download_utilities import download_file_from_click_of_button
from ArticlesDataDownloader.getDriver import getDriver


def download_acm_citations_from_search_link(driver, link, output_directory):
    driver.get(link)
    MAX_PAGES = 50
    for page_no in range(1, MAX_PAGES + 1):
        select_all_checkbox = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@class='item-results__checkbox']"))
        select_all_checkbox.click()

        export_popup = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//i[@class='icon-export']"))
        export_popup.click()

        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@class='csl-right-inline']"))

        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[@title='Download citation']/i[@class='icon-Icon_Download']"))

        download_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//a[@title='Download citation']"))

        file = download_file_from_click_of_button(driver, download_button)
        output_filename = output_directory + '/acm_auto_search_' + str(page_no) + '.bib'
        if file:
            shutil.move(file, output_filename)

        cancel_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@class='modal__header']/button[@class='close']"))
        cancel_button.click()

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                lambda x: x.find_element_by_xpath("//a[@class='pagination__btn--next']"))
            link = next_page_button.get_attribute('href')
            driver.get(link)
        except:
            break


def __main():
    link = 'https://dl.acm.org/action/doSearch?AllField=%22mutation+testing%22'
    output_dir = '/home/l/ArticlesInputFiles/ACM'
    driver = getDriver(proxyFile='proxy_auth_plugin.zip')
    download_acm_citations_from_search_link(driver, link, output_dir)


if __name__ == '__main__':
    sys.exit(__main())
