import logging
import requests

def getLinkFromDoi(doi):
    r = dict()
    try:
        url = "https://doi.org/api/handles/" + doi
        logging.debug('getting url using following link <' + url + '>')
        r = requests.get(url)

        if r.json()["responseCode"] == 1:
            return str(r.json()["values"][0]["data"]["value"])
    except Exception as e:
        pass
    logging.getLogger("getLinkFromDoi").error("Could \
        not find a link for following doi: <" + doi + ">")
    return str()
