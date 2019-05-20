def getDoiFilename(outputFolder, doi, extension = "json"):
    return outputFolder + "/" + doi.replace("/", "_")+"." + extension