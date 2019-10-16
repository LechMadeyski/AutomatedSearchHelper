import logging

def configureLogger():
    logsFilename = 'AutomatedSearchHelper.log'
    with open(logsFilename, 'w'):
        pass
    logging.basicConfig(filename=logsFilename, format='%(asctime)s %(levelname)s/%(name)s %(message)s', level=logging.INFO)
    logging.info("Starting new run")

