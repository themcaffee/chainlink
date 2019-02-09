import datetime

import requests
from redis import Redis
from rq import Queue


# Connection to the redis server for python-rq
queue = Queue(connection=Redis())


def parse_requirements(file_text):
    """
    Parse a python requirements.txt string into a list of package names
    :param file_text: requirements.txt text
    :return: List of package names
    """
    lines = file_text.split("\n")
    packages = []
    for line in lines:
        if len(line) == 0:
            continue
        packages.append(line.split("=="))
    return packages


def get_github_from_pypi(package, version):
    """
    Make a request to pypi to get the github repo for the given package and version
    :param package: PyPI package
    :param version: Package version
    :return: Owner and github repo of package
    """
    res = requests.get("https://pypi.python.org/pypi/{}/{}/json".format(package, version))
    if res.status_code != 200:
        print(res.text)
        raise Exception("Got error requesting from pypii")

    # Parse out the package home page
    res_json = res.json()
    home_page = res_json['info']['home_page']

    if "github.com" not in home_page:
        # If not a github repo just return what was given
        return home_page
    else:
        # Parse out the owner and package of github repo
        home_page = home_page.replace("https://github.com/", "")
        home_page = home_page.replace("http://github.com", "")
        split_b = home_page.split("/")
        github = {
            "owner": split_b[0],
            "package": split_b[1]
        }
        return github


def mp_get_github_from_pypi(req_text):
    """
    Use python-rq to create parallel jobs to get the list of github repos
    from the given requirement text.
    :param req_text: requirements.txt text
    :return: List of github repos
    """
    reqs = parse_requirements(req_text)

    # Queue up all of the jobs
    jobs = []
    for req in reqs:
        jobs.append(queue.enqueue(get_github_from_pypi, req[0], req[1]))

    # Wait until all the jobs are finished
    start_time = datetime.datetime.now()
    finished = False
    while not finished:
        all_done = True
        for job in jobs:
            if not job.result:
                all_done = False
                break
        if all_done:
            finished = True
        else:
            proc_time = datetime.datetime.now() - start_time
            if proc_time.seconds >= 2 * 60:
                raise Exception("Timed out getting results from pypi workers")
            finished = False

    # Get the results from the jobs
    github_repos = []
    for job in jobs:
        result = job.result
        if type(result) is not dict:
            continue
        github_repos.append(result)
    return github_repos

