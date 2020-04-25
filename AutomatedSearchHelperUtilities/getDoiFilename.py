
def getDoiFilename(outputFolder, doi, extension = "json"):
    return outputFolder + "/" + doi.replace("/", "_")+"." + extension

def doi_to_filename_base(doi):
    return doi.replace("/", "_")
