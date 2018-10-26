#!/usr/bin/env python3
import requests

endpoint = "https://de.wikipedia.org/w/api.php"


def perform_allpages_query(endpoint, payload):
    r = requests.get(endpoint, params=payload)
    results = r.json()["query"]["allpages"]
    return results


def crawl(endpoint):
    pages = {}
    payload = {"action": "query", "list": "allpages", "aplimit": 500, "format": "json"}
    last_title = ""
    results = perform_allpages_query(endpoint, payload)

    while len(results) is not 0:
        for page in results:
            page_id = page["pageid"]
            page_title = page["title"]
            pages[page_id] = page_title
            last_title = page_title
        payload["apfrom"] = last_title
        print("Starting next query from: " + str(last_title))
        results = perform_allpages_query(endpoint, payload)
    return pages


def save_dictionary(dictionary, filename):
    with open(filename, 'w') as f:
        for key in dictionary.keys():
            f.write("%s,%s\n" % (key, dictionary[key]))


print("Collecting wikipedia articles...")

pages = crawl(endpoint)
save_dictionary(pages, "pages.csv")