import logging
import os

from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader

def main():
    logsFilename = 'AutomatedSearchHelper.log'
    with open(logsFilename, 'w'):
        pass
    logging.basicConfig(filename=logsFilename, format='%(asctime)s %(levelname)s/%(message)s', level=logging.INFO)
    logging.info("Starting new run")

    outputFolder = 'outputArticles'

    if not os.path.exists(outputFolder):
        logging.info("Creating folder for output articles " + outputFolder)
        os.makedirs(outputFolder)

    downloader = ArticlesDataDownloader(outputFolder+"/")
    downloader.getDownloadArticles(
        [
          # "10.1109/icstw.2018.00026",
          # "10.1002/stvr.1675",
          # "10.1109/icstw.2018.00021",
          "10.1016/j.cosrev.2017.06.001",
          # "10.1145/3183519.3183521", #ACM
          # "10.1007/978-3-319-99927-2_9",
          # "10.1016/j.infsof.2016.07.002",
          # "10.1002/stvr.1630",
          # "10.1109/icstw.2018.00024",
          # "10.1109/icstw.2018.00025",
          # "10.1109/icstw.2018.00027",
          # "10.1109/icst.2018.00032",
          # "10.1145/3180155.3180183",
          # "10.1109/tse.2017.2684805",
          # "10.1109/C-M.1978.218136",
          # "10.1109/tse.2013.44",
        ])

if __name__ == '__main__':
    main()