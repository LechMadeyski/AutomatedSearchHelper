
import time
import os
from os import path
from pathlib import Path
from selenium.webdriver.support.wait import WebDriverWait

from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExistsOrClean

DOWNLOAD_DIRECTORY = os.getcwd() + '/downloads'

def __download_indictor_is_present():
    for i in os.listdir("."):
        if ".crdownload" in i:
            return True
    return False


def wait_for_file_download(file_path, max_times=10):
    for i in range(max_times):
        if os.path.exists(file_path) and not __download_indictor_is_present():
            return True
        time.sleep(0.5)
    return False


def __every_downloads_chrome(driver):
    if not driver.current_url.startswith("chrome://downloads"):
        driver.get("chrome://downloads/")
    return driver.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl || e.file_url);
        """)


def wait_until_all_files_downloaded(driver):
    for _ in range(100):
        if os.listdir(DOWNLOAD_DIRECTORY):
            break
        time.sleep(0.01)

    for _ in range(60):
        chrome_temp_file = sorted(Path(DOWNLOAD_DIRECTORY).glob('*.crdownload'))
        downloaded_files = sorted(Path(DOWNLOAD_DIRECTORY).glob('*.*'))
        if (len(chrome_temp_file) == 0) and (len(downloaded_files) >= 1):
            return
        time.sleep(1)
    print('timeout for download')

def clear_download_directory():
    createDirectoryIfNotExistsOrClean(DOWNLOAD_DIRECTORY)


def download_file_from_link_to_path(driver, link, output_name):
    file_saver_min_js = '''
    (function(a,b){if("function"==typeof define&&define.amd)define([],b);else if("undefined"!=typeof exports)b();else{b(),a.FileSaver={exports:{}}.exports}})(this,function(){"use strict";function b(a,b){return"undefined"==typeof b?b={autoBom:!1}:"object"!=typeof b&&(console.warn("Deprecated: Expected third argument to be a object"),b={autoBom:!b}),b.autoBom&&/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(a.type)?new Blob(["\uFEFF",a],{type:a.type}):a}function c(b,c,d){var e=new XMLHttpRequest;e.open("GET",b),e.responseType="blob",e.onload=function(){a(e.response,c,d)},e.onerror=function(){console.error("could not download file")},e.send()}function d(a){var b=new XMLHttpRequest;b.open("HEAD",a,!1);try{b.send()}catch(a){}return 200<=b.status&&299>=b.status}function e(a){try{a.dispatchEvent(new MouseEvent("click"))}catch(c){var b=document.createEvent("MouseEvents");b.initMouseEvent("click",!0,!0,window,0,0,0,80,20,!1,!1,!1,!1,0,null),a.dispatchEvent(b)}}var f="object"==typeof window&&window.window===window?window:"object"==typeof self&&self.self===self?self:"object"==typeof global&&global.global===global?global:void 0,a=f.saveAs||("object"!=typeof window||window!==f?function(){}:"download"in HTMLAnchorElement.prototype?function(b,g,h){var i=f.URL||f.webkitURL,j=document.createElement("a");g=g||b.name||"download",j.download=g,j.rel="noopener","string"==typeof b?(j.href=b,j.origin===location.origin?e(j):d(j.href)?c(b,g,h):e(j,j.target="_blank")):(j.href=i.createObjectURL(b),setTimeout(function(){i.revokeObjectURL(j.href)},4E4),setTimeout(function(){e(j)},0))}:"msSaveOrOpenBlob"in navigator?function(f,g,h){if(g=g||f.name||"download","string"!=typeof f)navigator.msSaveOrOpenBlob(b(f,h),g);else if(d(f))c(f,g,h);else{var i=document.createElement("a");i.href=f,i.target="_blank",setTimeout(function(){e(i)})}}:function(a,b,d,e){if(e=e||open("","_blank"),e&&(e.document.title=e.document.body.innerText="downloading..."),"string"==typeof a)return c(a,b,d);var g="application/octet-stream"===a.type,h=/constructor/i.test(f.HTMLElement)||f.safari,i=/CriOS\/[\d]+/.test(navigator.userAgent);if((i||g&&h)&&"undefined"!=typeof FileReader){var j=new FileReader;j.onloadend=function(){var a=j.result;a=i?a:a.replace(/^data:[^;]*;/,"data:attachment/file;"),e?e.location.href=a:location=a,e=null},j.readAsDataURL(a)}else{var k=f.URL||f.webkitURL,l=k.createObjectURL(a);e?e.location=l:location.href=l,e=null,setTimeout(function(){k.revokeObjectURL(l)},4E4)}});f.saveAs=a.saveAs=a,"undefined"!=typeof module&&(module.exports=a)});
                '''
    driver.execute_script(file_saver_min_js)

    download_script = f'''
                    console.log('running script')
                    return fetch('%s',
                        {{
                            "method": "GET",
                        }}
                    ).then(resp => {{
                        console.log('response 1 ')
                        return resp.blob();
                    }}).then(blob => {{
                        console.log('response 2 ')
                        saveAs(blob, '%s');
                    }});
                    ''' % (link, output_name)
    driver.execute_script(download_script)
    for _ in range(1000):
        if os.listdir(DOWNLOAD_DIRECTORY):
            break
    wait_until_all_files_downloaded(driver)

    result_filename = DOWNLOAD_DIRECTORY + '/' + output_name
    if not os.path.isfile(result_filename):
        time.sleep(1)
        wait_until_all_files_downloaded(driver)
    return result_filename



def download_file_from_link_that_initiates_download(driver, link):
    clear_download_directory()
    driver.get(link)
    try:
        wait_until_all_files_downloaded(driver)
    except:
        return None
    files = os.listdir(DOWNLOAD_DIRECTORY)
    if files:
        return DOWNLOAD_DIRECTORY + '/' + files[0]
    else:
        return None


def download_pdf(
        driver,
        pdf_link,
        output_filename='temporary.pdf'):
    try:
        clear_download_directory()
        return download_file_from_link_to_path(driver, pdf_link, output_filename)
    except Exception as error:
        return None


def download_file_from_click_of_button(driver, button):
    clear_download_directory()
    button.click()
    wait_until_all_files_downloaded(driver)
    files = os.listdir(DOWNLOAD_DIRECTORY)
    if files:
        return DOWNLOAD_DIRECTORY + '/' + files[0]
    else:
        return None
    # except Exception as error:
    #     return None


def get_files_from_download_directory():
    return [DOWNLOAD_DIRECTORY + '/' + x for x in os.listdir(DOWNLOAD_DIRECTORY)]




