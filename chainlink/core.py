import argparse
from pprint import pprint

import requests


def parse_requirements(file_text):
    lines = file_text.split("\n")
    packages = []
    for line in lines:
        if len(line) == 0:
            continue
        packages.append(line.split("=="))
    return packages


def get_requirements_text():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    file_name = args.file
    data = None
    with open(file_name) as f:
        data = f.read()
    if not data:
        raise Exception("Could not read data from file")
    return data


def get_github_from_pypi(package, version):
    res = requests.get("https://pypi.python.org/pypi/{}/{}/json".format(package, version))
    if res.status_code != 200:
        print(res.text)
        raise Exception("Got error requesting from pypii")
    res_json = res.json()
    home_page = res_json['info']['home_page']
    if "github.com" not in home_page:
        return None
    else:
        home_page = home_page.replace("https://github.com/", "")
        home_page = home_page.replace("http://github.com", "")
        split_b = home_page.split("/")
        github = {
            "owner": split_b[0],
            "package": split_b[1]
        }
        return github


def get_all_github_repos(packages):
    github_repos = []
    for package in packages:
        github = get_github_from_pypi(package[0], package[1])
        if not github:
            continue
        github_repos.append(github)
    return github_repos


def get_github_issues(owner, project):
    res = requests.get("https://api.github.com/repos/{}/{}/issues".format(owner, project))
    res_json = res.json()
    return res_json


def get_all_github_issues(github_repos):
    issues = []
    for repo in github_repos:
        issue = get_github_issues(repo["owner"], repo["package"])
        issues.append(issue)
    return issues


def get_issues_from_requirements_text(req_text):
    repos_issues = {}
    reqs = parse_requirements(req_text)
    for req in reqs:
        github = get_github_from_pypi(req[0], req[1])
        if not github:
            continue
        repos_issues[github["package"]] = github
    for repo_name in repos_issues:
        repo = repos_issues[repo_name]
        issues = get_github_issues(repo["owner"], repo["package"])
        repos_issues[repo_name]["issues"] = issues
    return repos_issues

