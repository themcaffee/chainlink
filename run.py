from pprint import pprint

from chainlink.main import get_requirements_text, get_issues_from_requirements_text

if __name__ == "__main__":
    requirements_text = get_requirements_text()
    issues = get_issues_from_requirements_text(requirements_text)
    for project in issues:
        pprint(issues[project])
        break
