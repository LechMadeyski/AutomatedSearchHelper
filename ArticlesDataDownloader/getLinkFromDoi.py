import logging
import requests

def getLinkFromDoi(doi):
    url = "https://doi.org/api/handles/" + doi
    r = requests.get(url)
    if r.json()["responseCode"] == 1:
        return r.json()["values"][0]["data"]["value"]
    else:
        logging.getLogger("getLinkFromDoi").error("Could \
            not find a link for following doi: "+ doi + " returned data is "+ str(r.json()))
        return None
