from bs4 import BeautifulSoup
import requests
import re

website1 = requests.get('https://github.com/Julie17XI')
soup1 = BeautifulSoup(website1.content, 'html.parser')
website2 = requests.get('https://github.com/Julie17XI?page=1&tab=repositories')
soup2 = BeautifulSoup(website2.content, 'html.parser')
user = soup1.find('strong').string.strip()
repo_nums = soup1.find('span', class_='Counter').string.strip()
last_yr_contribution_text = soup1.find('h2', class_='f4 text-normal mb-2').string.strip()
last_yr_contribution = re.findall("\d+", last_yr_contribution_text)[0]
print(user)
print(repo_nums)
print(last_yr_contribution)
print('------------------------------')
repos = soup2.find_all('li', itemprop='owns')
for repo in repos:
    repo_name = repo.find('a', itemprop='name codeRepository')
    repo_lang = repo.find('span', itemprop='programmingLanguage')
    repo_description = repo.find('p', itemprop='description')
    if repo_name:
        print(repo_name.string.strip())
    if repo_lang:
        print(repo_lang.string.strip())
    if repo_description:
        print(repo_description.string.strip())
    print('------------------------------')
