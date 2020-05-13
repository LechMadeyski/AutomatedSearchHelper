import slate as slate

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
    return sections
