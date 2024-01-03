import requests
import json

class Filters:
    def __init__(self):
        self.LIMIT = 5
        self.CROSSREF = "http://api.crossref.org/works"
        self.params = {
            "query.affiliation" : None,
            "query.bibliographic" : None, 
            "query.publisher-name" : None, 
            "query.author" : None,
            "query.publisher-location" : None, 
            "query.event-location" : None, 
            "query.event-name" : None,
            "rows" : self.LIMIT
        }
    
    def set_affiliation(self, input):
        self.params["query.affiliation"] = input
    def set_bibliographic(self, input):
        self.params["query.bibliographic"] = input
    def set_publisher_name(self, input):
        self.params["query.publisher-name"] = input
    def set_author(self, input):
        self.params["query.author"] = input
    def set_publisher_location(self, input):
        self.params["query.publisher-location"] = input
    def set_event_location(self, input):
        self.params["query.event-location"] = input
    def set_event_name(self, input):
        self.params["query.event-name"] = input
    def set_rows(self, input):
        self.params["rows"] = int(input)

    def reset(self):
        self.params = {
            "query.affiliation" : None,
            "query.bibliographic" : None, 
            "query.publisher-name" : None, 
            "query.author" : None,
            "query.publisher-location" : None, 
            "query.event-location" : None, 
            "query.event-name" : None,
            "rows" : self.LIMIT
        }

    def get_data(self):
        r = requests.get(self.CROSSREF, params=self.params)
        r.encoding = 'UTF-8'
        self.reset()
        return json.loads(r.text).get("message").get("items")
    
    def get_details(self, doi):
        url = "https://api.crossref.org/works"
        r = requests.get('{}/{}'.format(url, doi))
        return json.loads(str(r.text)).get('message')