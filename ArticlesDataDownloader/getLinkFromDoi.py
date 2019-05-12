
import requests

def getLinkFromDoi(doi):
	url = "https://doi.org/api/handles/" + doi
	r = requests.get(url)
	return r.json()["values"][0]["data"]["value"]
