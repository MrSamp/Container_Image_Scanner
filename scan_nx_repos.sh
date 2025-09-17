#!/bin/bash

# Nx Repository Scanner Wrapper Script
# Provides an easy interface to scan for repositories using Nx packages

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
LIMIT=50
SEARCH_TYPE="both"
OUTPUT_FILE=""
DETAILED=false
TOKEN=""

# Function to display usage
usage() {
    echo "Nx Repository Scanner"
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --token TOKEN      GitHub personal access token"
    echo "  -l, --limit NUMBER     Maximum number of repositories (default: 50)"
    echo "  -s, --search-type TYPE Search type: nx-json, packages, both (default: both)"
    echo "  -o, --output FILE      Output file path"
    echo "  -d, --detailed         Include detailed repository information"
    echo "  -h, --help             Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --token ghp_xxxx --limit 20 --detailed"
    echo "  $0 --search-type nx-json --output results.txt"
    echo ""
    echo "Get a GitHub token at: https://github.com/settings/tokens"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--token)
            TOKEN="$2"
            shift 2
            ;;
        -l|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -s|--search-type)
            SEARCH_TYPE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -d|--detailed)
            DETAILED=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if required dependencies are installed
if ! python3 -c "import requests" &> /dev/null; then
    echo -e "${YELLOW}Installing required dependencies...${NC}"
    pip3 install -r requirements.txt
fi

# Build the command
COMMAND="python3 nx_repo_scanner.py --limit $LIMIT --search-type $SEARCH_TYPE"

if [ -n "$TOKEN" ]; then
    COMMAND="$COMMAND --token $TOKEN"
fi

if [ "$DETAILED" = true ]; then
    COMMAND="$COMMAND --detailed"
fi

if [ -n "$OUTPUT_FILE" ]; then
    COMMAND="$COMMAND --output $OUTPUT_FILE"
fi

# Run the scanner
echo -e "${GREEN}Starting Nx repository scan...${NC}"
echo -e "${YELLOW}Search type: $SEARCH_TYPE${NC}"
echo -e "${YELLOW}Limit: $LIMIT repositories${NC}"

if [ -z "$TOKEN" ]; then
    echo -e "${YELLOW}Warning: No GitHub token provided. Rate limits may apply.${NC}"
    echo -e "${YELLOW}Get a token at: https://github.com/settings/tokens${NC}"
fi

eval $COMMAND

if [ -n "$OUTPUT_FILE" ]; then
    echo -e "${GREEN}Results saved to: $OUTPUT_FILE${NC}"
fi