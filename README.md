# Container Image Scanner

This repository provides tools for scanning container images and analyzing repositories that use Nx packages.

## Features

- **Container Image Scanning**: Automated Docker image security scanning using Trivy
- **Nx Repository Discovery**: Tool to locate repositories using Nx packages and monorepo tools

## Nx Repository Scanner

The `nx_repo_scanner.py` script helps you discover repositories that use Nx packages and tools.

### Prerequisites

```bash
pip install -r requirements.txt
```

### Usage

#### Using the Shell Script (Recommended)
```bash
# Make the script executable
chmod +x scan_nx_repos.sh

# Basic usage
./scan_nx_repos.sh

# With GitHub token for better rate limits
./scan_nx_repos.sh --token YOUR_GITHUB_TOKEN

# Advanced usage
./scan_nx_repos.sh --token YOUR_TOKEN --limit 20 --detailed --output results.txt
```

#### Direct Python Usage

#### Basic Usage
```bash
python nx_repo_scanner.py
```

#### With GitHub Token (Recommended for higher rate limits)
```bash
python nx_repo_scanner.py --token YOUR_GITHUB_TOKEN
```

#### Search Options
```bash
# Search only for repositories with nx.json files
python nx_repo_scanner.py --search-type nx-json

# Search only for repositories with Nx packages in package.json
python nx_repo_scanner.py --search-type packages

# Search both (default)
python nx_repo_scanner.py --search-type both

# Limit results and get detailed information
python nx_repo_scanner.py --limit 20 --detailed

# Save results to file
python nx_repo_scanner.py --output nx_repos.txt
```

### Command Line Options

- `--token`: GitHub personal access token (increases rate limits)
- `--limit`: Maximum number of repositories to find (default: 50)
- `--detailed`: Include detailed repository information (stars, description, etc.)
- `--search-type`: Type of search (`nx-json`, `packages`, or `both`)
- `--output`: Output file path (default: stdout)

### GitHub Token Setup

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `public_repo` scope
3. Use the token with the `--token` parameter

### Example Output

```
Found 3 repositories using Nx packages:

Repository: example/my-nx-workspace
URL: https://github.com/example/my-nx-workspace
File: nx.json
Description: A modern monorepo setup with Nx
Stars: 125
Language: TypeScript
Last Updated: 2023-12-01T10:30:00Z
--------------------------------------------------
```

## Container Image Scanning

The repository includes GitHub Actions workflows for automated container image scanning:

- **docker-image.yml**: Basic Docker image build and scan
- **trivy_image_scan.yml**: Advanced Trivy security scanning with severity filtering

### Docker Commands

```bash
# Build the image
docker build -t my-mysql-image .

# Run the container
docker run -d -p 3306:3306 --name my-mysql-container my-mysql-image
```

## Configuration

See `nx_scanner_config.yml` for configuration options including:
- Default search parameters
- Nx package patterns to search for
- Output format options

## Files Added

- **nx_repo_scanner.py**: Main Python script for scanning repositories
- **scan_nx_repos.sh**: Shell script wrapper for easy usage
- **test_nx_scanner.py**: Test script with sample data
- **nx_scanner_config.yml**: Configuration file
- **requirements.txt**: Python dependencies
- **.github/workflows/nx_discovery.yml**: GitHub Actions workflow for automated scanning

## Quick Start

1. **Run the scanner with sample data:**
   ```bash
   python3 test_nx_scanner.py
   ```

2. **Scan real repositories (requires GitHub token):**
   ```bash
   ./scan_nx_repos.sh --token YOUR_GITHUB_TOKEN --limit 10
   ```

3. **Get detailed information:**
   ```bash
   ./scan_nx_repos.sh --token YOUR_TOKEN --detailed --output results.txt
   ```

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request