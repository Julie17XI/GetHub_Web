from bs4 import BeautifulSoup
from urllib.error import HTTPError
import requests
import re
import bs4

'''
real-time web scraping for github user information
use url1 to get username, public repository number, and one year contribution number
user url2 to get a list of public repositories, including repo name, repo language and repo description
'''
def user_info(username):
    url1 = 'https://github.com/' + username
    url2 = 'https://github.com/' + username + '?page=1&tab=repositories'

    try:
        website1 = requests.get(url1)
        website1.raise_for_status()
    except HTTPError as hp:
        return None

    try:
        website2 = requests.get(url2)
        website2.raise_for_status()
    except HTTPError as hp:
        return None

    soup1 = BeautifulSoup(website1.content, 'html.parser')
    soup2 = BeautifulSoup(website2.content, 'html.parser')


    user_name = soup1.find('strong').string.strip()
    repo_number = soup1.find('span', class_='Counter').string.strip()
    one_yr_contribution_number_text = soup1.find('h2', class_='f4 text-normal mb-2').string.strip()
    one_yr_contribution_number = re.findall("\d+", one_yr_contribution_number_text)[0]

    repos = soup2.find_all('li', itemprop='owns')
    repos_info = []
    for repo in repos:
        repo_info = {}
        repo_name = repo.find('a', itemprop='name codeRepository')
        repo_lang = repo.find('span', itemprop='programmingLanguage')
        repo_description_with_emoji = repo.find('p', itemprop='description')
        if repo_description_with_emoji:
            text = []
            for x in repo_description_with_emoji:
                if isinstance(x, bs4.element.NavigableString):
                    text.append(x.strip())
        repo_description = " ".join(text)
        if repo_name:
            repo_info["repo_name"] = repo_name.string.strip()
        else:
            repo_info["repo_name"] = ""
        if repo_lang:
            repo_info["repo_lang"] = repo_lang.string.strip()
        else:
            repo_info["repo_lang"] = ""
        if repo_description:
            repo_info["repo_description"] = repo_description.strip()
        else:
            repo_info["repo_description"] = ""
        repos_info.append(repo_info)

    info = {
            "user_name": user_name,
            "repo_number": repo_number,
            "one_yr_contribution_number": one_yr_contribution_number,
            "repos_info": repos_info
            }

    return info
