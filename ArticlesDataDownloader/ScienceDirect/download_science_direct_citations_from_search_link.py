import os
import shutil
import sys
import time

from selenium.webdriver.support.wait import WebDriverWait

from ArticlesDataDownloader.download_utilities import download_file_from_click_of_button
from ArticlesDataDownloader.getDriver import getDriver


def download_acm_citations_from_search_link(driver, link, output_directory):
    driver.get(link)
    time.sleep(3)
    MAX_PAGES = 50
    for page_no in range(1, MAX_PAGES + 1):
        output_filename = os.path.join(output_directory, 'science_direct_auto_' + str(page_no) + '.ris')

        select_all_checkbox = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//label[@for='select-all-results']/span"))


        desired_y = (select_all_checkbox.size['height'] / 2) + select_all_checkbox.location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

        select_all_checkbox.click()

        export_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[@class='export-all-link-text']"))
        export_button.click()

        ris_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[contains(text(),'Export citation to RIS')]"))

        file = download_file_from_click_of_button(driver, ris_button)
        if file:
            shutil.move(file, output_filename)

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                lambda x: x.find_element_by_xpath("//a[@data-aa-name='srp-next-page']"))
            link = next_page_button.get_attribute('href')
            driver.get(link)
        except:
            break


def __main():
    link = 'https://www.sciencedirect.com/search?qs=mutation%20testing&show=25&tak=%22mutation%20testing%22'
    output_dir = '.server_files/InputFiles/Science_direct'
    driver = getDriver(proxyFile='proxy_auth_plugin.zip')
    download_acm_citations_from_search_link(driver, link, output_dir)


if __name__ == '__main__':
    sys.exit(__main())
