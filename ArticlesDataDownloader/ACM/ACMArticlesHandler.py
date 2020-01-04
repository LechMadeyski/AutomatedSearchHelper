
import selenium
import os
import logging
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from .extract_text_from_pdf import read_pdf_as_json
class ACMArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ACMArticlesHandler")

    def getArticle(self, url):
        self.__logger.debug("ACM::getArticle start " + url)
        try:
            self.__logger.debug("Called get for  " + url)

            self.driver.get(url)

            self.__logger.info("Get called")

            element = WebDriverWait(self.driver, 10).until(
                lambda x: x.find_elements_by_xpath("//a[@title='PDF']"))

            self.__logger.info("Wait end")

            python_button = self.driver.find_elements_by_xpath("//a[@title='PDF']")[0]

            link = str(python_button.get_property('href'))

            self.__logger.info("Got link to pdf : " + link)

            file_saver_min_js = '''
(function(a,b){if("function"==typeof define&&define.amd)define([],b);else if("undefined"!=typeof exports)b();else{b(),a.FileSaver={exports:{}}.exports}})(this,function(){"use strict";function b(a,b){return"undefined"==typeof b?b={autoBom:!1}:"object"!=typeof b&&(console.warn("Deprecated: Expected third argument to be a object"),b={autoBom:!b}),b.autoBom&&/^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(a.type)?new Blob(["\uFEFF",a],{type:a.type}):a}function c(b,c,d){var e=new XMLHttpRequest;e.open("GET",b),e.responseType="blob",e.onload=function(){a(e.response,c,d)},e.onerror=function(){console.error("could not download file")},e.send()}function d(a){var b=new XMLHttpRequest;b.open("HEAD",a,!1);try{b.send()}catch(a){}return 200<=b.status&&299>=b.status}function e(a){try{a.dispatchEvent(new MouseEvent("click"))}catch(c){var b=document.createEvent("MouseEvents");b.initMouseEvent("click",!0,!0,window,0,0,0,80,20,!1,!1,!1,!1,0,null),a.dispatchEvent(b)}}var f="object"==typeof window&&window.window===window?window:"object"==typeof self&&self.self===self?self:"object"==typeof global&&global.global===global?global:void 0,a=f.saveAs||("object"!=typeof window||window!==f?function(){}:"download"in HTMLAnchorElement.prototype?function(b,g,h){var i=f.URL||f.webkitURL,j=document.createElement("a");g=g||b.name||"download",j.download=g,j.rel="noopener","string"==typeof b?(j.href=b,j.origin===location.origin?e(j):d(j.href)?c(b,g,h):e(j,j.target="_blank")):(j.href=i.createObjectURL(b),setTimeout(function(){i.revokeObjectURL(j.href)},4E4),setTimeout(function(){e(j)},0))}:"msSaveOrOpenBlob"in navigator?function(f,g,h){if(g=g||f.name||"download","string"!=typeof f)navigator.msSaveOrOpenBlob(b(f,h),g);else if(d(f))c(f,g,h);else{var i=document.createElement("a");i.href=f,i.target="_blank",setTimeout(function(){e(i)})}}:function(a,b,d,e){if(e=e||open("","_blank"),e&&(e.document.title=e.document.body.innerText="downloading..."),"string"==typeof a)return c(a,b,d);var g="application/octet-stream"===a.type,h=/constructor/i.test(f.HTMLElement)||f.safari,i=/CriOS\/[\d]+/.test(navigator.userAgent);if((i||g&&h)&&"undefined"!=typeof FileReader){var j=new FileReader;j.onloadend=function(){var a=j.result;a=i?a:a.replace(/^data:[^;]*;/,"data:attachment/file;"),e?e.location.href=a:location=a,e=null},j.readAsDataURL(a)}else{var k=f.URL||f.webkitURL,l=k.createObjectURL(a);e?e.location=l:location.href=l,e=null,setTimeout(function(){k.revokeObjectURL(l)},4E4)}});f.saveAs=a.saveAs=a,"undefined"!=typeof module&&(module.exports=a)});
            '''

            self.driver.execute_script(file_saver_min_js)

            self.__logger.info("Script executed")


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
                    saveAs(blob, 'temporary.pdf');
                }});
                ''' % link
            self.driver.execute_script(download_script)
            self.__logger.info("Driver script executed")

            time.sleep(10)

            result = read_pdf_as_json('temporary.pdf')
            os.remove('temporary.pdf')
            return result
        except Exception as error:
            self.__logger.error("ERROR TYPE: " + str(type(error)))
            self.__logger.error(error)
            self.__logger.error("some error occured, moving on")
            return None

    def linkPart(self):
        return "dl.acm.org"

    def name(self):
        return "ACM"

