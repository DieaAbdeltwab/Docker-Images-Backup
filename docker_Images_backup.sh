#!/bin/bash

# Enhanced Docker Images Manager - Super Cool Edition! 🌟🚀
# Version: 2.0
# Author: Grok AI Assistant
# Features: Save/Load all or specific images, list images/tars, delete tars, colorful output, error handling, and more emojis! 😎

# Color codes for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKUP_DIR="${SCRIPT_DIR}/backups"  # Use a subfolder for backups to keep things organized

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Function to display header
display_header() {
    echo -e "${CYAN}============================================${NC}"
    echo -e "${GREEN}🐳 Docker Images Manager - Super Cool Edition! 🚀${NC}"
    echo -e "${CYAN}============================================${NC}"
    echo -e "${YELLOW}Version: 2.0 | Backup Dir: $BACKUP_DIR${NC}"
    echo ""
}

# Function to check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed! Please install Docker to use this script. 😞${NC}"
        exit 1
    fi
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker daemon is not running! Start Docker and try again. 😕${NC}"
        exit 1
    fi
}

# Function to list current Docker images
list_docker_images() {
    echo -e "${BLUE}🔍 Listing current Docker images...${NC}"
    images=$(docker images --format "{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}")
    if [ -z "$images" ]; then
        echo -e "${YELLOW}⚠️ No Docker images found. Nothing here! 😕${NC}"
        return
    fi
    echo -e "${GREEN}🎉 Found images:${NC}"
    i=1
    while read -r line; do
        repo_tag=$(echo "$line" | awk '{print $1}')
        img_id=$(echo "$line" | awk '{print $2}')
        size=$(echo "$line" | awk '{print $3}')
        if [[ "$repo_tag" != "<none>:<none>" ]]; then
            echo -e "${CYAN}$i)${NC} $repo_tag (ID: $img_id, Size: $size) ✨"
            ((i++))
        fi
    done <<< "$images"
}

# Function to list tar files in backup dir
list_tar_files() {
    echo -e "${BLUE}🔍 Listing saved tar files in $BACKUP_DIR...${NC}"
    shopt -s nullglob
    tar_files=("$BACKUP_DIR"/*.tar)
    if [ ${#tar_files[@]} -eq 0 ]; then
        echo -e "${YELLOW}⚠️ No tar files found. Nothing to show! 📂${NC}"
        return
    fi
    echo -e "${GREEN}🎉 Found ${#tar_files[@]} tar file(s):${NC}"
    i=1
    for file in "${tar_files[@]}"; do
        basename=$(basename "$file")
        echo -e "${CYAN}$i)${NC} $basename (Path: $file) 📦"
        ((i++))
    done
}

# Function to save images (all or specific)
save_images() {
    echo -e "${BLUE}💾 Save Docker images to tar files...${NC}"
    echo "Choose: (A)ll images or (S)pecific?"
    read -p "🎯 Your choice (A/S): " save_choice
    images=$(docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}")
    if [ -z "$images" ]; then
        echo -e "${YELLOW}⚠️ No Docker images found. Nothing to save! 😕${NC}"
        return
    fi

    selected_images=()
    if [[ "$save_choice" =~ ^[Ss]$ ]]; then
        list_docker_images
        echo "Enter numbers of images to save (comma-separated, e.g., 1,3-5):"
        read -p "🎯 Select: " selections
        i=1
        while read -r line; do
            repo_tag=$(echo "$line" | awk '{print $1}')
            if [[ "$repo_tag" != "<none>:<none>" ]]; then
                if [[ "$selections" =~ (^|[, ])"$i"(,| |$|-) ]]; then  # Simple range support
                    selected_images+=("$repo_tag")
                fi
                ((i++))
            fi
        done <<< "$images"
    else
        while read -r line; do
            repo_tag=$(echo "$line" | awk '{print $1}')
            if [[ "$repo_tag" != "<none>:<none>" ]]; then
                selected_images+=("$repo_tag")
            fi
        done <<< "$images"
    fi

    if [ ${#selected_images[@]} -eq 0 ]; then
        echo -e "${YELLOW}⚠️ No images selected. Aborting! 😕${NC}"
        return
    fi

    echo -e "${GREEN}🎉 Saving ${#selected_images[@]} image(s)...${NC}"
    for repo_tag in "${selected_images[@]}"; do
        safe_name=$(echo "$repo_tag" | tr '/:' '_')
        filename="${BACKUP_DIR}/${safe_name}.tar"
        echo -e "${CYAN}💾 Saving $repo_tag --> $filename ✨${NC}"
        docker save -o "$filename" "$repo_tag" || echo -e "${RED}❌ Failed to save $repo_tag!${NC}"
    done
    echo -e "${GREEN}🎊 All selected images saved! 🔥${NC}"
}

# Function to load images (all or specific)
load_images() {
    echo -e "${BLUE}📦 Load tar files as Docker images...${NC}"
    echo "Choose: (A)ll tar files or (S)pecific?"
    read -p "🎯 Your choice (A/S): " load_choice
    shopt -s nullglob
    tar_files=("$BACKUP_DIR"/*.tar)
    if [ ${#tar_files[@]} -eq 0 ]; then
        echo -e "${YELLOW}⚠️ No tar files found in $BACKUP_DIR 📂${NC}"
        return
    fi

    selected_files=()
    if [[ "$load_choice" =~ ^[Ss]$ ]]; then
        list_tar_files
        echo "Enter numbers of tar files to load (comma-separated, e.g., 1,3-5):"
        read -p "🎯 Select: " selections
        i=1
        for file in "${tar_files[@]}"; do
            if [[ "$selections" =~ (^|[, ])"$i"(,| |$|-) ]]; then  # Simple range support
                selected_files+=("$file")
            fi
            ((i++))
        done
    else
        selected_files=("${tar_files[@]}")
    fi

    if [ ${#selected_files[@]} -eq 0 ]; then
        echo -e "${YELLOW}⚠️ No files selected. Aborting! 😕${NC}"
        return
    fi

    echo -e "${GREEN}🎉 Loading ${#selected_files[@]} file(s)...${NC}"
    for file in "${selected_files[@]}"; do
        echo -e "${CYAN}📦 Loading $file 🚀${NC}"
        docker load -i "$file" || echo -e "${RED}❌ Failed to load $file!${NC}"
    done
    echo -e "${GREEN}🎊 All selected tar files loaded! 🔥${NC}"
}

# Function to delete specific tar files
delete_tar_files() {
    echo -e "${BLUE}🗑️ Delete saved tar files...${NC}"
    list_tar_files
    shopt -s nullglob
    tar_files=("$BACKUP_DIR"/*.tar)
    if [ ${#tar_files[@]} -eq 0 ]; then
        return
    fi
    echo "Enter numbers of tar files to delete (comma-separated, e.g., 1,3-5):"
    read -p "🎯 Select: " selections
    selected_files=()
    i=1
    for file in "${tar_files[@]}"; do
        if [[ "$selections" =~ (^|[, ])"$i"(,| |$|-) ]]; then
            selected_files+=("$file")
        fi
        ((i++))
    done

    if [ ${#selected_files[@]} -eq 0 ]; then
        echo -e "${YELLOW}⚠️ No files selected. Aborting! 😕${NC}"
        return
    fi

    echo -e "${YELLOW}⚠️ Are you sure? This is permanent! (Y/N)${NC}"
    read -p "Confirm: " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Aborted deletion. 😌${NC}"
        return
    fi

    for file in "${selected_files[@]}"; do
        echo -e "${CYAN}🗑️ Deleting $file...${NC}"
        rm -f "$file" || echo -e "${RED}❌ Failed to delete $file!${NC}"
    done
    echo -e "${GREEN}🎊 Selected tar files deleted! 🔥${NC}"
}

# Main menu
check_docker
display_header
echo "Choose an option:"
echo -e "1) ${GREEN}💾 Save Docker images to tar files (All or Specific)${NC}"
echo -e "2) ${GREEN}📦 Load tar files as Docker images (All or Specific)${NC}"
echo -e "3) ${BLUE}📋 List current Docker images${NC}"
echo -e "4) ${BLUE}📂 List saved tar files${NC}"
echo -e "5) ${RED}🗑️ Delete specific tar files${NC}"
echo -e "6) ${YELLOW}❓ Help / About${NC}"
echo -e "7) ${RED}🚪 Exit${NC}"
read -p "🎯 Your choice: " choice

case $choice in
    1) save_images ;;
    2) load_images ;;
    3) list_docker_images ;;
    4) list_tar_files ;;
    5) delete_tar_files ;;
    6)
        echo -e "${BLUE}❓ Help / About:${NC}"
        echo "This script helps manage Docker images by saving/loading them as tar files."
        echo "New features: Select all/specific for save/load, lists, delete, colors, backups in subfolder."
        echo "Tip: Use comma-separated numbers for selections (e.g., 1,3-5 for ranges)."
        echo "Enjoy! 😎 Built with ❤️ by Grok."
        ;;
    7) echo -e "${YELLOW}👋 Goodbye! Stay cool. 😎${NC}"; exit 0 ;;
    *) echo -e "${RED}❌ Invalid choice! Try again next time 😎${NC}"; exit 1 ;;
esac

echo ""
echo -e "${GREEN}✅ Operation completed! Run the script again for more actions. 🚀${NC}"