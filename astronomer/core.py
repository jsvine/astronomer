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
        nixed = set(("url", "type", "site_admin"))
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
    def __init__(self, repo_id, repo_type="repo"):
        self.repo_id = repo_id
        self.repo_type = repo_type

    def fetch_info(self, requester):
        url = "{0}/{1}s/{2}".format(API_BASE,
            self.repo_type, self.repo_id)
        response = requester(url)
        self.info = response.json()
        self.stargazers_count = self.info["stargazers_count"]
        return self
    
    def fetch_stargazers(self, requester):
        url = "{0}/{1}s/{2}/stargazers".format(API_BASE,
            self.repo_type, self.repo_id)
        self.stargazers = map(Stargazer, gather_responses(requester, url))
        return self 

    def fetch_stargazer_details(self, requester):
        for s in self.stargazers: s.get_details(requester)
        return 
