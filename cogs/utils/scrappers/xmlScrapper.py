from collections import defaultdict
import re


class xmlScrapper(object):

    def __init__(self, keys: [], xml: str):
        self.keys = keys
        self.xml = xml
        self.result = defaultdict(list)

    def get_values(self):

        spliced = re.split("[<>\]=\"]", self.xml)
        for i, item in enumerate(spliced):
            if item in self.keys:
                self.result[item].append(spliced[i + 1].replace("\n", ''))

        return self.result

    def set_keys(self, new_keys: []):
        self.keys = new_keys

    def set_xml(self, new_xml):
        self.xml = new_xml

    def get_dict(self):
        return self.result
