import csv
import logging

def extract_doi_from_csv(csv_filename):
    logger = logging.getLogger("extract_doi_from_csv")
    with open(csv_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        doiIndex = None
        doiList = list()
        for row in csv_reader:
            if line_count == 0:
                for i in range(len(row)):
                    if "DOI" in str(row[i]):
                        logger.info("Doi has column name : " + row[i] + " and index " + str(i))
                        doiIndex = i
                        break
                if doiIndex == None:
                    logger.error("No doi in csv")
                    return list()
                line_count += 1
            else:
                if row[doiIndex] != str():
                    doiList.append(row[doiIndex])
                else:
                    logger.warning('Could not find doi for row: ' + str(row))
                line_count += 1

        logger.info(f'Processed {len(doiList)} dois.')
        return doiList