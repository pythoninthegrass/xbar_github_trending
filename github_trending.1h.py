#!/usr/bin/env -S PATH="${HOME}/.asdf/shims:/opt/homebrew/bin:/usr/local/bin:${PATH}" python3
# -*- coding: utf-8 -*-

# <xbar.title>Github Trending</xbar.title>
# <xbar.version>v0.1.0</xbar.version>
# <xbar.author>pythoninthegrass</xbar.author>
# <xbar.author.github>pythoninthegrass</xbar.author.github>
# <xbar.desc>Github Daily Trending Viewer</xbar.desc>
# <xbar.image>https://raw.githubusercontent.com/pythoninthegrass/xbar-plugin-github-trending/Screenshots/01.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/pythoninthegrass/xbar-plugins-github-trending</xbar.abouturl>

import os
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    from requests_cache import CachedSession
    from requests.exceptions import RequestException
except ImportError as e:
    print(f"Failed to import module: {e}")
    print("Please install the required modules by running the following command:")
    print("python -m pip install requests requests-cache bs4")
    # exit(1)

lang = 'python'  # your favorite language (ruby, python, mojo, swift, etc.)
url = f'https://github.com/trending/{lang}?since=daily'
base_url = 'https://github.com/'
links = 10
count = 0
# dark_mode = os.getenv('XBARDarkMode', True)
cache = 'github_trending_cache'


def main():
    session = CachedSession(cache,
                            backend='sqlite',
                            expire_after=3600,
                            use_temp=True,
                            allowable_codes=(200))

    # TODO: capture specific exceptions (e.g., 429)
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        # TODO: replace with sf pro star / star.fill
        print('⭐️\n---')

        soup = BeautifulSoup(html, 'html.parser')
        repo_list_items = soup.find_all('a', class_='Link', attrs={'href': True, 'data-hydro-click': True})

        repos = set()
        for item in repo_list_items:
            repo_name = item['href'][1:]
            if repo_name.endswith('/forks'):
                repo_name = repo_name.replace('/forks', '')
            repo_url = base_url + repo_name

            api_url = f'https://api.github.com/repos/{repo_name}'
            try:
                api_response = requests.get(api_url)
                api_response.raise_for_status()
                repo_data = api_response.json()
                total_stars = repo_data['stargazers_count']
                repos.add((repo_name, total_stars, repo_url))
            except RequestException:
                print('🙅Github Api Limits🙅')
                break

        sorted_repos = sorted(repos, key=lambda x: x[1], reverse=True)
        for repo in sorted_repos[:links]:
            repo_name, total_stars, repo_url = repo
            print(f"{repo_name} ⭐️ Total: {total_stars} | href={repo_url}")

    except RequestException as e:
        print(f"Failed to open URL: {e}")


if __name__ == '__main__':
    main()

    # # import inspect
    # # print(f"Line number: {inspect.currentframe().f_lineno}")
    # # import sys
    # import os
    # path = [path for path in os.environ.get('PATH').split(':')]
    # path = ':'.join(path)
    # print("PATH")
    # print("---")
    # print(path)
