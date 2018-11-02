#!/usr/bin/env python3
import requests

endpoint = "https://de.wikipedia.org/w/api.php"


def perform_allpages_query(endpoint, payload):
    r = requests.get(endpoint, params=payload)
    results = r.json()["query"]["allpages"]
    return results


def get_links_from_article(page_id, article_name):
    links = {}
    payload = {\
        "action": "query",\
        "list": "allpages",\
        "titles": article_name,\
        "pllimit": 500,\
        "prop": "links",\
        "format": "json"}
    r = requests.get(endpoint, params=payload)
    links = r.json()["query"]["pages"][str(page_id)][links]
    plcontinue = r.json()["continue"]["plcontinue"]


def crawl(endpoint):
    pages = {}
    last_title = ""
    payload = {"action": "query", "list": "allpages", "aplimit": 500, "apfrom": last_title, "format": "json"}
    results = perform_allpages_query(endpoint, payload)

    while len(results) is not 0:
        requested_title = last_title
        # Process results
        for page in results:
            page_id = page["pageid"]
            page_title = page["title"]
            pages[page_id] = page_title
            last_title = page_title

        # Continue, if not requesting same article again
        if last_title != requested_title:
            payload["apfrom"] = last_title
            print("Starting next query from: " + str(last_title))
            results = perform_allpages_query(endpoint, payload)
        else:
            return pages
    return pages


def save_dictionary(dictionary, filename):
    with open(filename, 'w') as f:
        for key in dictionary.keys():
            f.write("%s,%s\n" % (key, dictionary[key]))


print("Collecting wikipedia articles...")

pages = crawl(endpoint)
save_dictionary(pages, "pages.csv")