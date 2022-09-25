from bs4 import BeautifulSoup
import requests
import re
import json

def user_info(username):

    url1 = 'https://github.com/' + username
    url2 = 'https://github.com/' + username + '?page=1&tab=repositories'
    website1 = requests.get(url1)
    website2 = requests.get(url2)
    soup1 = BeautifulSoup(website1.content, 'html.parser')
    soup2 = BeautifulSoup(website2.content, 'html.parser')

    user = soup1.find('strong').string.strip()
    repo_nums = soup1.find('span', class_='Counter').string.strip()
    last_yr_contribution_text = soup1.find('h2', class_='f4 text-normal mb-2').string.strip()
    last_yr_contribution = re.findall("\d+", last_yr_contribution_text)[0]

    repos = soup2.find_all('li', itemprop='owns')
    repos_info = []
    for repo in repos:
        repo_info = {}
        repo_name = repo.find('a', itemprop='name codeRepository')
        repo_lang = repo.find('span', itemprop='programmingLanguage')
        repo_description = repo.find('p', itemprop='description')
        if repo_name:
            repo_info["repo_name"] = repo_name.string.strip()
        if repo_lang:
            repo_info["repo_lang"] = repo_lang.string.strip()
        if repo_description:
            repo_info["repo_description"] = repo_description.string.strip()
        repos_info.append(repo_info)

    info = {
            "user": user,
            "repo_nums": repo_nums,
            "last_yr_contribution": last_yr_contribution,
            "repos_info": repos_info
            }

    return json.dumps(info)
