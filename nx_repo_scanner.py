#!/usr/bin/env python3
"""
Nx Repository Scanner
Locates repositories that use Nx packages and tools.
"""

import requests
import json
import argparse
import sys
from typing import List, Dict, Any
from urllib.parse import quote


class NxRepoScanner:
    """Scanner to find repositories using Nx packages"""
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "nx-repo-scanner"
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
    
    def search_repos_with_nx_json(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Search for repositories containing nx.json files"""
        if not self.github_token:
            print("Note: Code search requires authentication. Falling back to repository search.")
            return self._search_repositories_fallback(limit)
        
        query = "filename:nx.json"
        return self._search_code(query, limit)
    
    def search_repos_with_nx_packages(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Search for repositories with Nx packages in package.json"""
        if not self.github_token:
            print("Note: Code search requires authentication. Falling back to repository search.")
            return self._search_repositories_fallback(limit)
        
        queries = [
            '"@nrwl/workspace"',
            '"@nx/workspace"', 
            '"nx"',
            '"@nrwl/cli"',
            '"@nx/cli"'
        ]
        
        all_repos = []
        for query in queries:
            search_query = f"{query} filename:package.json"
            repos = self._search_code(search_query, limit // len(queries))
            all_repos.extend(repos)
        
        # Remove duplicates based on repository full_name
        seen = set()
        unique_repos = []
        for repo in all_repos:
            repo_name = repo.get('repository', {}).get('full_name')
            if repo_name and repo_name not in seen:
                seen.add(repo_name)
                unique_repos.append(repo)
        
        return unique_repos[:limit]
    
    def _search_repositories_fallback(self, limit: int) -> List[Dict[str, Any]]:
        """Fallback repository search when code search is not available"""
        search_terms = ["nx workspace", "nx monorepo", "nrwl", "@nx/workspace"]
        all_repos = []
        
        for term in search_terms:
            repos = self._search_repositories(term, limit // len(search_terms))
            # Convert repository format to match code search format
            for repo in repos:
                all_repos.append({
                    'repository': repo,
                    'path': 'package.json (inferred)',
                    'name': 'package.json'
                })
        
        # Remove duplicates
        seen = set()
        unique_repos = []
        for repo_item in all_repos:
            repo_name = repo_item.get('repository', {}).get('full_name')
            if repo_name and repo_name not in seen:
                seen.add(repo_name)
                unique_repos.append(repo_item)
        
        return unique_repos[:limit]
    
    def _search_repositories(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search GitHub repositories"""
        encoded_query = quote(query)
        url = f"{self.base_url}/search/repositories?q={encoded_query}&per_page={min(limit, 100)}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return data.get('items', [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching repositories: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}")
            return []
    
    def _search_code(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search GitHub code using the search API"""
        encoded_query = quote(query)
        url = f"{self.base_url}/search/code?q={encoded_query}&per_page={min(limit, 100)}"
        
        try:
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 403:
                print("GitHub API requires authentication for code search.")
                print("Please provide a GitHub token using --token parameter.")
                print("You can generate one at: https://github.com/settings/tokens")
                return []
            
            response.raise_for_status()
            
            data = response.json()
            return data.get('items', [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching GitHub: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}")
            return []
    
    def get_repo_details(self, repo_full_name: str) -> Dict[str, Any]:
        """Get detailed information about a repository"""
        url = f"{self.base_url}/repos/{repo_full_name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting repo details for {repo_full_name}: {e}")
            return {}
    
    def format_results(self, results: List[Dict[str, Any]], detailed: bool = False) -> str:
        """Format search results for display"""
        if not results:
            return "No repositories found using Nx packages."
        
        output = f"Found {len(results)} repositories using Nx packages:\n\n"
        
        for item in results:
            repo = item.get('repository', {})
            repo_name = repo.get('full_name', 'Unknown')
            repo_url = repo.get('html_url', '')
            file_path = item.get('path', '')
            
            output += f"Repository: {repo_name}\n"
            output += f"URL: {repo_url}\n"
            output += f"File: {file_path}\n"
            
            if detailed:
                repo_details = self.get_repo_details(repo_name)
                if repo_details:
                    output += f"Description: {repo_details.get('description', 'N/A')}\n"
                    output += f"Stars: {repo_details.get('stargazers_count', 0)}\n"
                    output += f"Language: {repo_details.get('language', 'N/A')}\n"
                    output += f"Last Updated: {repo_details.get('updated_at', 'N/A')}\n"
            
            output += "-" * 50 + "\n"
        
        return output


def main():
    parser = argparse.ArgumentParser(description="Scan for repositories using Nx packages")
    parser.add_argument("--token", help="GitHub personal access token")
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of repositories to find")
    parser.add_argument("--detailed", action="store_true", help="Include detailed repository information")
    parser.add_argument("--search-type", choices=["nx-json", "packages", "both"], default="both",
                       help="Type of search to perform")
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    scanner = NxRepoScanner(args.token)
    all_results = []
    
    if args.search_type in ["nx-json", "both"]:
        print("Searching for repositories with nx.json files...")
        nx_json_results = scanner.search_repos_with_nx_json(args.limit)
        all_results.extend(nx_json_results)
    
    if args.search_type in ["packages", "both"]:
        print("Searching for repositories with Nx packages...")
        package_results = scanner.search_repos_with_nx_packages(args.limit)
        all_results.extend(package_results)
    
    # Remove duplicates if searching both
    if args.search_type == "both":
        seen = set()
        unique_results = []
        for result in all_results:
            repo_name = result.get('repository', {}).get('full_name')
            if repo_name and repo_name not in seen:
                seen.add(repo_name)
                unique_results.append(result)
        all_results = unique_results[:args.limit]
    
    output = scanner.format_results(all_results, args.detailed)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Results written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()