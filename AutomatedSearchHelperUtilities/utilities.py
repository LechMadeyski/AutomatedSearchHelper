import os
import shutil
import time


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


def load_function(filename, functionName):
    with open(filename) as f:
        global_var = dict()
        local_var = dict()
        execfile(filename, global_var, local_var)
        functionKey = next(k for k in local_var.keys() if k == functionName and callable(local_var[k]))
        if functionKey is not None:
            return local_var[functionKey]

def load_variable(filename, variableName):
    with open(filename) as f:
        global_var = dict()
        local_var = dict()
        execfile(filename, global_var, local_var)
        functionKey = next(k for k in local_var.keys() if k == variableName)
        if functionKey is not None:
            return local_var[functionKey]

def createDirectoryIfNotExists(directoryPath):
  if not os.path.exists(directoryPath):
      os.makedirs(directoryPath)


def createDirectoryIfNotExistsOrClean(directoryPath):
    if os.path.exists(directoryPath):
        shutil.rmtree(directoryPath)
        while os.path.exists(directoryPath):
            time.sleep(0.01)
            pass
    os.makedirs(directoryPath)
    while not os.path.exists(directoryPath):
        time.sleep(0.01)
        pass

def getDoiFilename(outputFolder, doi, extension = "json"):
    return outputFolder + "/" + doi.replace("/", "_")+"." + extension