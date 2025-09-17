#!/usr/bin/env python3
"""
Test script for the Nx Repository Scanner
Demonstrates functionality with sample data when GitHub API is not available
"""

import sys
import os

# Add the current directory to the path to import our scanner
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nx_repo_scanner import NxRepoScanner

def create_sample_data():
    """Create sample data to demonstrate the scanner functionality"""
    return [
        {
            'repository': {
                'full_name': 'nrwl/nx',
                'html_url': 'https://github.com/nrwl/nx',
                'description': 'Smart, Fast and Extensible Build System',
                'stargazers_count': 15000,
                'language': 'TypeScript',
                'updated_at': '2023-12-01T10:30:00Z'
            },
            'path': 'nx.json',
            'name': 'nx.json'
        },
        {
            'repository': {
                'full_name': 'example/my-nx-workspace',
                'html_url': 'https://github.com/example/my-nx-workspace',
                'description': 'A modern monorepo setup with Nx',
                'stargazers_count': 125,
                'language': 'TypeScript',
                'updated_at': '2023-11-15T14:20:00Z'
            },
            'path': 'package.json',
            'name': 'package.json'
        },
        {
            'repository': {
                'full_name': 'company/frontend-workspace',
                'html_url': 'https://github.com/company/frontend-workspace',
                'description': 'Frontend applications and libraries',
                'stargazers_count': 45,
                'language': 'JavaScript',
                'updated_at': '2023-12-05T09:15:00Z'
            },
            'path': 'workspace.json',
            'name': 'workspace.json'
        }
    ]

def test_scanner():
    """Test the scanner with sample data"""
    print("Testing Nx Repository Scanner")
    print("=" * 50)
    
    scanner = NxRepoScanner()
    sample_data = create_sample_data()
    
    # Test formatting without detailed info
    print("Basic output format:")
    basic_output = scanner.format_results(sample_data, detailed=False)
    print(basic_output)
    
    print("\nDetailed output format:")
    # Mock the get_repo_details method for testing
    original_method = scanner.get_repo_details
    scanner.get_repo_details = lambda repo_name: next(
        (item['repository'] for item in sample_data 
         if item['repository']['full_name'] == repo_name), {}
    )
    
    detailed_output = scanner.format_results(sample_data, detailed=True)
    print(detailed_output)
    
    # Restore original method
    scanner.get_repo_details = original_method

def test_cli_interface():
    """Test the command line interface"""
    print("\nTesting CLI interface:")
    print("=" * 30)
    
    # Show help
    os.system("python3 nx_repo_scanner.py --help")

if __name__ == "__main__":
    test_scanner()
    test_cli_interface()
    
    print("\nTo use with real GitHub data, obtain a GitHub token:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Generate a new token with 'public_repo' scope")
    print("3. Run: python3 nx_repo_scanner.py --token YOUR_TOKEN")