import os
import requests
import streamlit as st
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GitHubOrgFetcher:
    def __init__(self, org_name: str):
        self.org_name = org_name
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.headers = self._setup_headers()

    def _setup_headers(self) -> Dict[str, str]:
        """Set up headers for GitHub API requests"""
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
        return headers

    def fetch_org_repos(self) -> List[Dict]:
        """Fetch all repositories from the organization with their details"""
        all_repos = []
        page = 1

        while True:
            url = f'https://api.github.com/orgs/{self.org_name}/repos'
            params = {
                'type': 'all',
                'sort': 'updated',
                'direction': 'desc',
                'per_page': 100,
                'page': page
            }

            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                repos = response.json()
                if not repos:
                    break

                # Extract relevant information from each repository
                for repo in repos:
                    repo_info = {
                        'name': repo.get('name'),
                        'description': repo.get('description'),
                        'homepage': repo.get('homepage'),
                        'topics': repo.get('topics', []),
                        'html_url': repo.get('html_url'),
                        'created_at': repo.get('created_at'),
                        'updated_at': repo.get('updated_at'),
                        'visibility': repo.get('visibility'),
                        'default_branch': repo.get('default_branch'),
                        'language': repo.get('language')
                    }
                    all_repos.append(repo_info)

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching repositories: {e}")
                if response.status_code == 401:
                    print("Authentication failed. Please check your GitHub token.")
                elif response.status_code == 403:
                    print("API rate limit exceeded or insufficient permissions.")
                break

        return all_repos

def main():
    # Initialize the fetcher with your organization name
    org_name = 'alphatechlogics'  # Replace with your organization name
    fetcher = GitHubOrgFetcher(org_name)

    # Fetch repositories
    repos = fetcher.fetch_org_repos()

    # Print repository information
    print(f"\nFound {len(repos)} repositories in {org_name}:\n")
    
    for repo in repos:
        print(f"Repository: {repo['name']}")
        print(f"Description: {repo['description']}")
        print(f"Homepage: {repo['homepage']}")
        print(f"Topics: {', '.join(repo['topics'])}")
        print(f"Language: {repo['language']}")
        print(f"Visibility: {repo['visibility']}")
        print(f"URL: {repo['html_url']}")
        print("-" * 80)

if __name__ == "__main__":
    main()
