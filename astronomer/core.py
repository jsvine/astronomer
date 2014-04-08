import re

API_BASE = "https://api.github.com"

class Stargazer(object):
    def __init__(self, info):
        self.info = info

    def get_details(self, requester):
        url = self.info["url"]
        response = requester(url)
        self.info = dict(self.info.items() + response.json().items())
        return self

    def to_json(self):
        nixed = set(("url", "type", "site_admin", "gravatar_id"))
        urls = set(filter(lambda x: "_url" in x, self.info.keys()))
        keys = set(self.info.keys()) - (nixed | urls)
        encode = lambda x: x.encode("utf-8") if type(x) == unicode else x 
        return {key:encode(self.info[key])
            for key in keys}

def gather_responses(requester, url, so_far=[]):
    response = requester(url)
    if not len(response.json()): return so_far
    link_pattern = re.compile(r'<([^<>]+)>; rel="([^"]+)"')
    links = re.findall(link_pattern, response.headers["link"])
    next_link = filter(lambda x: x[1] == "next", links)[0][0]
    return gather_responses(requester, next_link, so_far + response.json())

class Repo(object):
    def __init__(self, owner, name):
        self.api_base = API_BASE
        self.owner = owner
        self.name = name

    def fetch_info(self, requester):
        url = "{api_base}/repos/{owner}/{name}".format(**self.__dict__)
        response = requester(url)
        self.info = response.json()
        return self
    
    def fetch_stargazers(self, requester):
        url = "{api_base}/repos/{owner}/{name}/stargazers".format(**self.__dict__)
        self.stargazers = map(Stargazer, gather_responses(requester, url))
        return self 

    def fetch_stargazer_details(self, requester):
        for s in self.stargazers: s.get_details(requester)
        return 
