from bs4 import BeautifulSoup
import bs4
import requests
import re

GITHUB_URL = 'https://github.com/'
GITHUB_REPO_SUFFIX = '?page=1&tab=repositories'

# real-time web scraping for github user information
# url1 = GITHUB_URL + username
# url2 = GITHUB_URL + username + GITHUB_REPO_SUFFIX
# use url1 to get username, public repository number, and one year contribution number
# user url2 to get a list of public repositories, including repo name, repo language and repo description

def get_body_content(username):
    """
    Scrape real-time user data from GitHub with given username.

    :param username: string, the GitHub username our app user enters in search box

    :return: dict, the data about the user and his/her list of public repositories

    This is for one username at a time. E.g. {"user_info": {"username": "Jane", "repo_number": "2",
    "one_yr_contribution_number": "21"}, "repos_info": [{"repo_name": "repo1", "repo_lang": "Python,
    "repo_description": "some description"}, {"repo_name": "repo2", "repo_lang": "C++,
    "repo_description": "some other description"}]}
    """
    user_info = get_user_basics(username)
    repos_info = get_repo_list(username)
    info = {
        "user_info": user_info,
        "repos_info": repos_info
        }
    return info

def get_soup(url):
    """
    Pull data out of HTML.

    :param url: string, the url that needs to be parsed

    :return: bs4.BeautifulSoup object, it contains all HTML elements from this url
    """
    website = requests.get(url)  # Careful url may not exist
    soup = BeautifulSoup(website.content, 'html.parser')
    return soup

def get_user_basics(username):
    """
    Scrape user's basic info from github user home page. E.g. 'https://github.com/Jane'.

    :param username: string, the GitHub username our app user enters in search box

    :return: dict, username, the number of the user's public repositories, and the number
    of the user's contribution in last year
    """
    url = GITHUB_URL + username
    soup = get_soup(url)

    user_name = soup.find('strong').string.strip()
    repo_number = soup.find('span', class_='Counter').string.strip()
    one_yr_contribution_number_text = soup.find('h2', class_='f4 text-normal mb-2').string.strip()
    one_yr_contribution_number = re.findall("\d+", one_yr_contribution_number_text)[0]

    user_basics = {
        "user_name": user_name,
        "repo_number": repo_number,
        "one_yr_contribution_number": one_yr_contribution_number
    }
    return user_basics

def get_repo_list(username):
    """
    Scrape the list of public repositories of a user from github user repository page.
    E.g. 'https://github.com/Jane/?page=1&tab=repositories'

    :param username: string, the GitHub username our app user enters in search box

    :return: dict, contains username, the number of the user's public repositories, and the
    number of the user's contribution in last year
    """
    url = GITHUB_URL + username + GITHUB_REPO_SUFFIX
    soup = get_soup(url)
    repos = soup.find_all('li', itemprop='owns')
    repos_info = []
    for repo in repos:
        repo_info = get_repo_info(repo)
        repos_info.append(repo_info)
    return repos_info

def get_repo_info(repo):
    """
    Find the repository name, the language that the repository uses, and the description
    of the repository, and save them to a map.

    :param repo: bs4.BeautifulSoup object, the section that contains the data mentioned
    above

    :return: dict, contains the data of each repositories of the user
    """
    repo_info = {}
    repo_name = repo.find('a', itemprop='name codeRepository')
    repo_lang = repo.find('span', itemprop='programmingLanguage')
    repo_description_with_emoji = repo.find('p', itemprop='description')
    repo_description = get_repo_description(repo_description_with_emoji)
    set_repo_attr(repo_info, "repo_name", repo_name)
    set_repo_attr(repo_info, "repo_lang", repo_lang)
    set_repo_attr_for_text(repo_info, "repo_description", repo_description)
    return repo_info

def set_repo_attr(repo_info, key, attr):
    """
    Store the given attribute in the form of string to a dict. If such attribute is
    not found in the HTML tag, store an empty string for that attribute in dict.

    :param repo_info: dict, contains data about one public repository of a GitHub user
    :param key: str, key in dict and represents one attribute of the repository
    :param attr: bs4.element.Tag, the HTML tag that contains data for one repo

    :return: None, no need to return anything
    """
    if attr:
        repo_info[key] = attr.string.strip()
    else:
        repo_info[key] = ""

def set_repo_attr_for_text(repo_info, key, attr):
    """
    Store the given attribute in the form of string to a dict. If such attribute is
    not found in the HTML tag, store an empty string for that attribute in dict.

    :param repo_info: dict, contains data about one public repository of a GitHub user
    :param key: str, key in dict and represents one attribute of the repository
    :param attr: str, data for one attribute of the repo

    :return: None, no need to return anything
    """
    if attr:
        repo_info[key] = attr.strip()
    else:
        repo_info[key] = ""

def get_repo_description(raw_repo_description):
    """
    Eliminate anything from the related tag except for the pure text of repo description.

    :param raw_repo_description: bs4.element.Tag, the tag that includes repo description

    :return: string, the pure text of repo description
    """
    if raw_repo_description:
        text = []
        for x in raw_repo_description:
            if isinstance(x, bs4.element.NavigableString):
                text.append(x.strip())
        repo_description = " ".join(text)
        return repo_description
