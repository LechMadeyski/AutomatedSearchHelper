import slate as slate
from pdfminer.pdfinterp import PDFResourceManager

from ArticlesDataDownloader.text_utilities import format_text_and_split_into_sentences


def is_section_title_big_letters(prev, current):
    if prev.strip().isnumeric():
        return (prev.strip().isnumeric() and current.isupper())

    split_current = current.split(' ')
    if len(split_current) > 1 and split_current[0].isnumeric() and split_current[1].isupper():
        return True

    return current.strip() in ['REFERENCES', 'ABSTRACT', 'ACKNOWLEDGMENTS']


def is_section_with_first_big_letter_no_dot(prev, current):
    if '.' not in current and ',' not in current:
        split_current = current.strip().split(' ')

        if prev.strip().isnumeric():
            return split_current and split_current[0] and split_current[0][0].isupper()

        if len(split_current)>1 and split_current[0].strip().isnumeric():
            return split_current[1] and split_current[1][0].isupper()

        return current.strip() in ['References', 'Abstract', 'Acknowledgments']


def is_section_with_first_big_letter_with_dot(prev, current):
    if '.' in prev and ',' not in current:
        split_prev = prev.split('.')
        if split_prev[0].isnumeric() and len(current) > 1:
            return current[0].isupper()

        return current.strip() in ['References', 'Abstract', 'Acknowledgments']


def is_section_with_first_big_letter_and_dot_in_current(prev, current):
    if '.' in current and ',' not in current:
        split_current_with_dot = current.strip().split('.')

        if split_current_with_dot[0].isnumeric() and len(split_current_with_dot) > 1:
            return split_current_with_dot[1] and split_current_with_dot[1][0].isupper()

        return current.strip() in ['References', 'Abstract', 'Acknowledgments']


def is_section_with_big_letters_and_dot_in_current(prev, current):
    if '.' in current and ',' not in current:
        split_current_with_dot = current.strip().split('.')

        if split_current_with_dot[0].isnumeric() and len(split_current_with_dot) > 1:
            return split_current_with_dot[1] and split_current_with_dot[1].isupper()

        return current.strip() in ['REFERENCES', 'ABSTRACT', 'ACKNOWLEDGMENTS']


def is_section_title(prev, current):
    return is_section_title_big_letters(prev, current) \
           or is_section_with_first_big_letter_no_dot(prev, current)\
           or is_section_with_first_big_letter_and_dot_in_current(prev, current)\
           or is_section_with_big_letters_and_dot_in_current(prev, current)\
           or is_section_with_first_big_letter_with_dot(prev, current)


def is_one_of_standard_parts(current):
    standard_parts = ['introduction', 'conclusions', 'related work']
    if current.strip().lower() in standard_parts:
        return True

    if current and current[0].isnumeric():
        split_current = current.strip().lower().split(' ')
        return len(split_current) > 1 and ' '.join(split_current[1:]) in standard_parts
    return False


def detect_start_of_section_method(split_text):
    prev = str()
    for current in split_text:
        if is_one_of_standard_parts(current):
            if is_section_title_big_letters(prev, current):
                return is_section_title_big_letters
            elif is_section_with_first_big_letter_no_dot(prev, current):
                return is_section_with_first_big_letter_no_dot
            elif is_section_with_first_big_letter_and_dot_in_current(prev, current):
                return is_section_with_first_big_letter_and_dot_in_current
            elif is_section_with_big_letters_and_dot_in_current(prev, current):
                return is_section_with_big_letters_and_dot_in_current
            elif is_section_with_first_big_letter_with_dot(prev, current):
                return is_section_with_first_big_letter_with_dot
        prev = current
    return is_section_title



def read_pdf_as_json(filename):
    with open(filename, 'rb') as f:
        extracted_text = slate.PDF(f)
    split_text = []

    for extracted_part in extracted_text:
        split_text += extracted_part.replace('\\n', '\n').split('\n\n')

    is_start_of_section = detect_start_of_section_method(split_text)

    sections = []
    current_section = dict(title='Begining data', text=str())
    prev = str()
    for part in split_text:
        if is_start_of_section(prev, part):
            sections.append(dict(
                title=current_section['title'],
                paragraphs=[dict(sentences=format_text_and_split_into_sentences(current_section['text']))]))
            current_section = dict(title=part.strip(), text=str())
        else:
            if part.endswith('-'):
                current_section['text'] += part[:-1]
            else:
                current_section['text'] += part + ' '
        prev = part

    if current_section['text']:
        sections.append(dict(
            title=current_section['title'],
            paragraphs=[dict(sentences=format_text_and_split_into_sentences(current_section['text']))]))

    no_of_sentences = 0
    for sec in sections:
        for par in sec['paragraphs']:
            no_of_sentences += len([x for x in par['sentences'] if len(x) > 30])
            if no_of_sentences > 30:
                return sections

    raise Exception('Invalid pdf read - text too short')

#
#
# from pdfminer import pdfparser
#
# if __name__ == '__main__':
#     print("extraction start")
#
#     filename = 'test_pdf.pdf'
#     # Import libraries
#     from PIL import Image
#     import pytesseract
#     import sys
#     from pdf2image import convert_from_path
#     import os
#
#     # Path of the pdf
#     PDF_file = os.path.join(os.getcwd(), filename)
#
#     '''
#     Part #1 : Converting PDF to images
#     '''
#     print("FILE PATH IS " + PDF_file)
#
#     # Store all the pages of the PDF in a variable
#     pages = convert_from_path(PDF_file, 500)
#
#     print("conversion done")
#     # Counter to store images of each page of PDF to image
#     image_counter = 1
#
#     # Iterate through all the pages stored above
#     for page in pages:
#         # Declaring filename for each page of PDF as JPG
#         # For each page, filename will be:
#         # PDF page 1 -> page_1.jpg
#         # PDF page 2 -> page_2.jpg
#         # PDF page 3 -> page_3.jpg
#         # ....
#         # PDF page n -> page_n.jpg
#         filename = "page_" + str(image_counter) + ".jpg"
#
#         # Save the image of the page in system
#         page.save(filename, 'JPEG')
#
#         # Increment the counter to update filename
#         image_counter = image_counter + 1
#
#     '''
#     Part #2 - Recognizing text from the images using OCR
#     '''
#     # Variable to get count of total number of pages
#     filelimit = image_counter - 1
#
#     # Creating a text file to write the output
#     outfile = "out_text.txt"
#
#     # Open the file in append mode so that
#     # All contents of all images are added to the same file
#     f = open(outfile, "a", encoding='utf-8')
#
#     # Iterate from 1 to total number of pages
#     for i in range(1, filelimit + 1):
#         # Set filename to recognize text from
#         # Again, these files will be:
#         # page_1.jpg
#         # page_2.jpg
#         # ....
#         # page_n.jpg
#         filename = "page_" + str(i) + ".jpg"
#
#         # Recognize the text as string in image using pytesserct
#         text = str(((pytesseract.image_to_string(Image.open(filename)))))
#
#         # The recognized text is stored in variable text
#         # Any string processing may be applied on text
#         # Here, basic formatting has been done:
#         # In many PDFs, at line ending, if a word can't
#         # be written fully, a 'hyphen' is added.
#         # The rest of the word is written in the next line
#         # Eg: This is a sample text this word here GeeksF-
#         # orGeeks is half on first line, remaining on next.
#         # To remove this, we replace every '-\n' to ''.
#         text = text.replace('-\n', '')
#
#         # Finally, write the processed text to the file.
#         f.write(text)
#
#         # Close the file after writing all the text.
#     f.close()
#
#
#
#     print("result")
