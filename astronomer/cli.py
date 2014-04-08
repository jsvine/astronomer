import sys
import argparse
import getpass
import logging
import requests
from core import Repo, Stargazer
from writers import write_json, write_tsv, write_csv

logging.basicConfig(format="%(name)s | %(message)s")
logger = logging.getLogger("astronomer")

def repo_from_slash(repo_str):
    split = repo_str.split("/")
    if len(split) != 2:
        raise Exception("Repo argument should be in the format :owner/:repo.")
    return Repo(*split)

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("repo",
        type=repo_from_slash,
        help=":owner/:repo")

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
        log_response(response)
        return response
    return requester

def get_writer(fmt):
    return {
        "json": write_json,
        "tsv": write_tsv,
        "csv": write_csv
    }[fmt]

def main():
    args = get_args()
    logger.setLevel(logging.WARNING if args.quiet else logging.INFO) 
    token = args.token or getpass.getpass("Personal API Access Token: ")
    requester = make_requester(token)
    repo = args.repo
    repo.fetch_info(requester)
    repo.fetch_stargazers(requester)
    if not args.minimal:
        repo.fetch_stargazer_details(requester)
    writer = get_writer(args.format)
    writer(repo.stargazers, args.outfile)

if __name__ == "__main__":
    main()
