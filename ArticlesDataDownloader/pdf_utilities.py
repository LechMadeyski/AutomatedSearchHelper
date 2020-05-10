import logging
import os

from PyPDF2 import PdfFileWriter, PdfFileReader


def extract_given_pages_from_pdf(pdf_filename, start_page, end_page):
    logger = logging.getLogger('extract_given_pages_from_pdf')

    logger.info('Trying to extract pages ' + str(start_page) + '-' + str(end_page) + ' from ' + pdf_filename)
    if start_page > end_page:
        logger.warning('Given invalid range for extraction of ' + pdf_filename + " {" + str(start_page) + "-" + str(end_page) + "}")
        return str()
    inputpdf = PdfFileReader(open(pdf_filename, "rb"))

    if end_page > inputpdf.numPages:
        logger.warning('Range exceeds pdf size of ' + pdf_filename + " (" + str(inputpdf.numPages) + ") end page:" + str(end_page))
        return str()
    output = PdfFileWriter()
    for i in range(start_page, end_page+1):
        output.addPage(inputpdf.getPage(i))
    output_name = pdf_filename.replace('.pdf', '_extracted.pdf')
    logger.info('Writing results to  ' + output_name)
    with open(output_name, "wb") as outputStream:
        output.write(outputStream)
    os.remove(pdf_filename)
    return output_name

