# import slate as slate

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



# def read_pdf_as_json_pdf_analysis(filename):
#     with open(filename, 'rb') as f:
#         extracted_text = slate.PDF(f)
#     split_text = []

#     for extracted_part in extracted_text:
#         split_text += extracted_part.replace('\\n', '\n').split('\n\n')

#     is_start_of_section = detect_start_of_section_method(split_text)

#     sections = []
#     current_section = dict(title='Begining data', text=str())
#     prev = str()
#     for part in split_text:
#         if is_start_of_section(prev, part):
#             sections.append(dict(
#                 title=current_section['title'],
#                 paragraphs=[dict(sentences=format_text_and_split_into_sentences(current_section['text']))]))
#             current_section = dict(title=part.strip(), text=str())
#         else:
#             if part.endswith('-'):
#                 current_section['text'] += part[:-1]
#             else:
#                 current_section['text'] += part + ' '
#         prev = part

#     if current_section['text']:
#         sections.append(dict(
#             title=current_section['title'],
#             paragraphs=[dict(sentences=format_text_and_split_into_sentences(current_section['text']))]))

#     no_of_sentences = 0
#     for sec in sections:
#         for par in sec['paragraphs']:
#             no_of_sentences += len([x for x in par['sentences'] if len(x) > 30])
#             if no_of_sentences > 30:
#                 return sections

#     raise Exception('Invalid pdf read - text too short')


from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
import logging


STANDARD_CHAPTERS = ['introduction', 'conclusions', 'related work']

def is_one_of_standard_parts_ocr(line):
    split_line = line.lower().split(' ')
    if len(split_line) > 1 and ' '.join(split_line[1:]).strip() in STANDARD_CHAPTERS:
        return True
    else:
        return line.strip().lower() in STANDARD_CHAPTERS

def is_numeric_index(part):
    part_replaced = part.replace('.', '')
    return part_replaced.strip() and part_replaced.isnumeric()


def is_numeric_and_big_letters(line):
    split_line = line.split(' ')
    return len(split_line) > 1 and is_numeric_index(split_line[0]) and split_line[1].isupper()

def is_upper_camel_case(part):
    return len(part) > 1 and part[0].isupper() and part[1:].islower()


def is_numeric_and_camel_case(line):
    split_line = line.split(' ')
    return len(split_line) > 1 and is_numeric_index(split_line[0]) and is_upper_camel_case(split_line[1])


def is_one_of_non_chapter_parts(line):
    return line.lower().strip() in ['references', 'abstract', 'acknowledgments']

def is_roman_index(part):
    stripped_part = part.replace('.', '').strip()
    if stripped_part:
        for l in stripped_part:
            if l not in ["X", "V", "I"]:
                return False
        return True
    else:
        return False

def is_roman_and_big_letters(line):
    split_line = line.split(' ')
    return len(split_line) > 1 and is_roman_index(split_line[0]) and split_line[1].isupper()


def is_roman_and_camel_case(line):
    split_line = line.split(' ')
    return len(split_line) > 1 and is_roman_index(split_line[0]) and is_upper_camel_case(split_line[1])

def is_just_big_letters(line):
    return line.isupper()


def detect_chapter_line_format_analyzer(text_lines):
    logger = logging.getLogger('detect_chapter_line_format_analyzer')
    for line_prev, line_curent, line_next in zip(text_lines, text_lines[1:], text_lines[2:]):
        if is_one_of_standard_parts_ocr(line_curent):
            def wrap_analyzer(analyzer):
                prev_analyzer = lambda t: True
                next_analyzer = lambda t: True

                if line_prev == str():
                    prev_analyzer = lambda t: t == str()
                # if line_next == str():
                #     next_analyzer = lambda t: t == str()

                def result_detector(line_prev, line_current, line_next):
                    return prev_analyzer(line_prev) \
                           and next_analyzer(line_next)\
                           and (is_one_of_non_chapter_parts(line_current) or analyzer(line_current))
                return result_detector
            logger.info('Got standard part: <' + line_curent + '>')
            if is_numeric_and_big_letters(line_curent):
                return wrap_analyzer(is_numeric_and_big_letters)
            elif is_numeric_and_camel_case(line_curent):
                return wrap_analyzer(is_numeric_and_camel_case)
            elif is_roman_and_big_letters(line_curent):
                return wrap_analyzer(is_roman_and_big_letters)
            elif is_roman_and_camel_case(line_curent):
                return wrap_analyzer(is_roman_and_camel_case)
            elif is_just_big_letters(line_curent):
                return wrap_analyzer(is_just_big_letters)
            logger.info('No match with analyzer')

    logger.info('No standard part found, returning default')

    return lambda line_prev, line_current, line_next: False


def read_pdf_as_json_ocr(filename):
    logger = logging.getLogger('read_pdf_as_json_ocr')
    logger.info('Start ocr reading for ' + filename)

    pixel_density = 300

    pages = convert_from_path(filename, pixel_density, thread_count=12, paths_only=True, fmt='jpg', output_folder=os.path.dirname(filename))
    logger.info('Conversion done - got pages : ' + str(len(pages)))
    logger.info('Pixel density is = ' + str(pixel_density))

    if len(pages) > 60:
        logger.warning("There are more then 60 pages in the article, article cannot be read")
        raise Exception('Invalid pdf read - too many pages')

    full_text_lines = []


    images_text_file_content = str()
    for index, page in enumerate(pages):
        # logger.info('Reading page ' + str(index+1) + '/' + str(len(pages)))
        # page_file = os.path.join(os.path.dirname(filename), 'page' + str(index) + '.jpg')
        # page.save(page_file, 'JPEG')
        images_text_file_content += page +'\n'


    images_text_file = os.path.join(os.path.dirname(filename), 'images.txt')

    with open(images_text_file, 'w') as f:
        f.write(images_text_file_content)

    logger.info('Pages saved to file start ocr')
    full_text_lines += str((pytesseract.image_to_string(images_text_file, lang='eng'))).split('\n')
    logger.info('Finished ocr starting text analysis')

    if len(full_text_lines) < 3:
        logger.info('No text could be read or it has less then 3 lines')
        raise Exception('Invalid pdf read - text too short')

    # ## Debug option
    # with open('output_full_lines.json', 'w', encoding='utf-8') as f:
    #     import json
    #     f.write(json.dumps(full_text_lines))


    is_chapter_name = detect_chapter_line_format_analyzer(full_text_lines)

    sections = []
    current_section = dict(title='Begining data', text=full_text_lines[0])
    for line_prev, line_current, line_next in zip(full_text_lines, full_text_lines[1:], full_text_lines[2:]):
        if is_chapter_name(line_prev, line_current, line_next):
            sections.append(dict(
                title=current_section['title'],
                paragraphs=[dict(sentences=format_text_and_split_into_sentences(current_section['text']))]))
            current_section = dict(title=line_current.strip(), text=line_current + '\n')
            logger.info('Start analyzing next section: <' + current_section['title'] + '>')
        else:
            if line_current.endswith('-'):
                current_section['text'] += line_current[:-1]
            else:
                current_section['text'] += line_current + ' '

    current_section['text'] += full_text_lines[-1]
    sections.append(dict(
        title=current_section['title'],
        paragraphs=[dict(sentences=format_text_and_split_into_sentences(current_section['text']))]))

    return sections


def read_pdf_as_json(filename):
    return read_pdf_as_json_ocr(filename)