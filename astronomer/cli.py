import sys
import argparse
import getpass
import logging
import requests
from core import Repo, Stargazer, API_BASE
from writers import write_json, write_tsv, write_csv

logging.basicConfig(format="%(name)s | %(message)s")
logger = logging.getLogger("astronomer")

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("repo",
        help=":owner/:repo")

    parser.add_argument("--gist", "-g",
        action="store_true",
        help="Repo is a gist. Not yet supported by GitHub API.")

    parser.add_argument("--format", "-f",
        default="tsv",
        choices=["tsv", "csv", "json"],
        help="Format. Choices: tsv, csv, json. Default: tsv.")

    parser.add_argument("--minimal",
        action="store_true",
        help="Only get the users' names and ids, not their details.")

    parser.add_argument("--token", "-t",
        help="""Personal API Token, for authenticating requests.
        If you do not supply this as an argument,
        you will be prompted to enter it.""")

    parser.add_argument("--outfile", "-o",
        type=argparse.FileType('w'),
        default=sys.stdout,
        help="File to write output. Default: stdout.")

    parser.add_argument("--quiet",
        help="Silence logging.",
        action="store_true")

    args = parser.parse_args()
    return args

def log_url(url):
    logger.info("GET {0}".format(url))

def log_response(response):
    logger.info(u"\t\u261e Status: {0}".format(response.status_code))
    logger.info(u"\t\u261e Rate limit: {0}/{1} remaining.".format(
        response.headers["X-RateLimit-Remaining"],
        response.headers["X-RateLimit-Limit"],
    ))

def make_requester(token):
    def requester(url):
        log_url(url)
        response = requests.get(url, auth=(token, "x-oauth-basic"))
        if response.status_code != 200:
            raise Exception("HTTP Status: {}".format(response.status_code))
        log_response(response)
        return response
    return requester

def get_writer(fmt):
    return {
        "json": write_json,
        "tsv": write_tsv,
        "csv": write_csv
    }[fmt]

def check_rate_limit(repo, requester, args):
    rate_limit_response = requester(API_BASE + "/rate_limit")
    rate_limit = rate_limit_response.json()["resources"]["core"]
    reqs_remaining = rate_limit["remaining"]
    reqs_needed = (repo.stargazers_count / 20) \
        + (bool(repo.stargazers_count % 20) * 1) \
        + ((not args.minimal) * repo.stargazers_count)
    if reqs_needed > reqs_remaining:
        logger.fatal("Getting all these stargazers would require {0} requests, but you have only {1} remaining. Exiting.".format(reqs_needed, reqs_remaining))
        exit()

def get_repo_type(args):
    repo_type = "gist" if args.gist else "repo"
    if repo_type == "gist":
        logger.fatal("The GitHub API cannot yet retreive stargazers for gists. Exiting.")
        exit()
    else:
        return repo_type
    
def main():
    args = get_args()

    # Set up logging
    logger.setLevel(logging.WARNING if args.quiet else logging.INFO) 

    # Set up authentication
    token = args.token or getpass.getpass("Personal API Access Token: ")
    requester = make_requester(token)

    # Initialize repo, and check the rate limit
    repo = Repo(args.repo, get_repo_type(args))
    repo.fetch_info(requester)
    check_rate_limit(repo, requester, args)

    # Get the stargazers
    repo.fetch_stargazers(requester)
    if not args.minimal: repo.fetch_stargazer_details(requester)

    # Write the results
    writer = get_writer(args.format)
    writer(repo.stargazers, args.outfile)

if __name__ == "__main__":
    main()
