from collections import defaultdict
from datetime import datetime

import requests

try:
    from .config import GITHUB_TOKEN
except ImportError:
    GITHUB_TOKEN = None

def get_headers():
    """Get HTTP headers for GitHub API requests."""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    return headers

def get_commit_count(repo_name, username):
    """Get commit count for a specific user in a repository."""
    try:
        # Get commits by the specific user
        commit_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        params = {
            'author': username,
            'per_page': 100
        }
        
        commits = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(commit_url, params=params, headers=get_headers())
            response.raise_for_status()
            
            page_commits = response.json()
            if not page_commits:
                break
                
            commits.extend(page_commits)
            page += 1
            
            # Check if we've reached the last page
            if 'next' not in response.links:
                break
        
        return len(commits)
        
    except Exception as e:
        print(f"Error counting commits for {repo_name}: {e}")
        return 0  # Return 0 if any error occurs

def get_language_stats(username):
    """Fetch repository languages weighted by commit count."""
    try:
        api_url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(api_url, headers=get_headers())
        response.raise_for_status()
        repos = response.json()
        
        if not isinstance(repos, list):
            print("Error: Unable to fetch repository data")
            return {}
            
        # Count repositories by their primary language, weighted by commits
        languages = defaultdict(float)
        total_weighted_count = 0
        
        for repo in repos:
            if isinstance(repo, dict) and repo.get('language'):
                commit_count = get_commit_count(repo['name'], username)
                languages[repo['language']] += commit_count
                total_weighted_count += commit_count
        
        # Calculate weighted percentages
        total_weighted_count = total_weighted_count if total_weighted_count > 0 else 1
        return {lang: round((count/total_weighted_count) * 100, 2) 
                for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)}
        
    except requests.RequestException as e:
        print(f"Error fetching data from GitHub: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

def get_repo_timeline(username):
    """Fetch monthly commit activities since account creation."""
    try:
        # 获取用户信息以确定注册时间
        user_url = f"https://api.github.com/users/{username}"
        response = requests.get(user_url, headers=get_headers())
        response.raise_for_status()
        user_data = response.json()
        created_at = datetime.strptime(user_data['created_at'].split('T')[0], '%Y-%m-%d')
        
        # 获取所有仓库
        repos_url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(repos_url, headers=get_headers())
        response.raise_for_status()
        repos = response.json()
        
        # 按月份统计commits
        monthly_data = defaultdict(list)
        
        for repo in repos:
            if isinstance(repo, dict):
                name = repo.get('name', '')
                language = repo.get('language', 'Unknown')
                
                # 获取该仓库的所有commits
                commits_url = f"https://api.github.com/repos/{username}/{name}/commits"
                params = {'author': username, 'per_page': 100}
                
                try:
                    commits_response = requests.get(commits_url, params=params, headers=get_headers())
                    commits_response.raise_for_status()
                    commits = commits_response.json()
                    
                    # 按月份分组commits
                    for commit in commits:
                        if isinstance(commit, dict) and 'commit' in commit:
                            commit_date = datetime.strptime(
                                commit['commit']['author']['date'].split('T')[0],
                                '%Y-%m-%d'
                            )
                            month_key = commit_date.strftime('%Y-%m')
                            
                            # 将commit信息添加到对应月份
                            found = False
                            for repo_data in monthly_data[month_key]:
                                if repo_data['name'] == name:
                                    repo_data['commits'] += 1
                                    found = True
                                    break
                            
                            if not found:
                                monthly_data[month_key].append({
                                    'name': name,
                                    'commits': 1,
                                    'language': language
                                })
                                
                except Exception as e:
                    print(f"Error fetching commits for {name}: {e}")
                    continue
        
        # 转换为时间线数据格式
        timeline_data = []
        for period in sorted(monthly_data.keys()):
            repos_in_period = monthly_data[period]
            if repos_in_period:  # 只添加有活动的月份
                timeline_data.append({
                    'period': period,
                    'repos': repos_in_period,
                    'total_commits': sum(r['commits'] for r in repos_in_period),
                    'languages': list(set(r['language'] for r in repos_in_period))
                })
        
        return timeline_data
        
    except Exception as e:
        print(f"Error fetching timeline data: {e}")
        return []
