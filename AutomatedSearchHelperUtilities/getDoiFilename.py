import os


def doi_to_filename_base(doi):
    return doi.replace("/", "_").replace(':', '').replace('(', '').replace(')', '').replace('%', '').replace('<', '').replace('>', '')


def getDoiFilename(outputFolder, doi, extension="json"):
    return os.path.join(outputFolder, doi_to_filename_base(doi)+"." + extension)
