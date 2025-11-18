#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐳 Enhanced Docker Images Manager - Super Cool Edition! 🚀
Version: 3.0 - Ultra Beautiful
Author: Converted from Grok AI Assistant's bash script
Features: Save/Load all or specific images, list images/tars, delete tars, beautiful UI, emojis, error handling
Compatible: Windows + Linux
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from datetime import datetime

# Fix encoding issues on Windows
if platform.system() == 'Windows':
    # Set console to UTF-8
    if sys.version_info >= (3, 7):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass
    
    # Enable ANSI colors on Windows 10+
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass

# 🎨 Color codes for beautiful output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NC = '\033[0m'
    
    # Bright colors
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_CYAN = '\033[1;96m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_MAGENTA = '\033[1;95m'

# Get script directory and setup backup directory
SCRIPT_DIR = Path(__file__).parent.absolute()
BACKUP_DIR = SCRIPT_DIR / 'backups'

# Create backup directory if it doesn't exist
try:
    BACKUP_DIR.mkdir(exist_ok=True)
except Exception as e:
    print(f"⚠️ Error creating backup directory: {e}")
    BACKUP_DIR = SCRIPT_DIR

def safe_print(text):
    """Safe print that handles encoding issues"""
    try:
        print(text)
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Try without emojis
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text)
    except Exception as e:
        print(str(e).encode('ascii', 'ignore').decode('ascii'))

def print_line(char='═', length=60, color=Colors.CYAN):
    """Print a decorative line"""
    safe_print(f"{color}{char * length}{Colors.NC}")

def print_box(text, color=Colors.BRIGHT_CYAN):
    """Print text in a box"""
    length = len(text) + 4
    safe_print(f"{color}╔{'═' * length}╗{Colors.NC}")
    safe_print(f"{color}║  {text}  ║{Colors.NC}")
    safe_print(f"{color}╚{'═' * length}╝{Colors.NC}")

def display_header():
    """Display beautiful script header"""
    safe_print("")
    print_line('═', 60, Colors.BRIGHT_CYAN)
    safe_print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}{'':^60}{Colors.NC}")
    safe_print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}{'🐳 DOCKER IMAGES MANAGER 🐳':^60}{Colors.NC}")
    safe_print(f"{Colors.BRIGHT_BLUE}{Colors.BOLD}{'✨ Super Cool Edition ✨':^60}{Colors.NC}")
    safe_print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}{'':^60}{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_CYAN)
    safe_print(f"{Colors.YELLOW}{'Version: 3.0 | Author: AI Assistant':^60}{Colors.NC}")
    safe_print(f"{Colors.CYAN}{'📁 Backup Directory: ' + str(BACKUP_DIR.name):^60}{Colors.NC}")
    print_line('─', 60, Colors.CYAN)
    safe_print("")

def run_docker_command(cmd, capture=True):
    """Run docker command with proper error handling"""
    try:
        kwargs = {
            'capture_output': capture,
            'text': True,
            'check': True,
            'encoding': 'utf-8',
            'errors': 'replace'
        }
        
        # Add CREATE_NO_WINDOW flag for Windows (Python 3.7+)
        if platform.system() == 'Windows' and sys.version_info >= (3, 7):
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        
        result = subprocess.run(cmd, **kwargs)
        return result
    except subprocess.CalledProcessError as e:
        raise e
    except Exception as e:
        safe_print(f"{Colors.RED}❌ Error running command: {e}{Colors.NC}")
        raise e

def check_docker():
    """Check if Docker is installed and running"""
    safe_print(f"{Colors.BRIGHT_BLUE}🔍 Checking Docker status...{Colors.NC}")
    safe_print("")
    
    # Check if docker command exists
    try:
        run_docker_command(['docker', '--version'])
        safe_print(f"{Colors.BRIGHT_GREEN}   ✅ Docker is installed{Colors.NC}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        safe_print(f"{Colors.BRIGHT_RED}   ❌ Docker is NOT installed!{Colors.NC}")
        safe_print(f"{Colors.YELLOW}   💡 Download from: https://www.docker.com/products/docker-desktop{Colors.NC}")
        input(f"\n{Colors.CYAN}Press Enter to exit...{Colors.NC}")
        sys.exit(1)
    
    # Check if docker daemon is running
    try:
        run_docker_command(['docker', 'info'])
        safe_print(f"{Colors.BRIGHT_GREEN}   ✅ Docker daemon is running{Colors.NC}")
        safe_print("")
    except subprocess.CalledProcessError:
        safe_print(f"{Colors.BRIGHT_RED}   ❌ Docker daemon is NOT running!{Colors.NC}")
        safe_print(f"{Colors.YELLOW}   💡 Please start Docker Desktop and try again{Colors.NC}")
        input(f"\n{Colors.CYAN}Press Enter to exit...{Colors.NC}")
        sys.exit(1)

def get_docker_images():
    """Get list of docker images"""
    try:
        result = run_docker_command(
            ['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}|{{.ID}}|{{.Size}}']
        )
        images = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) == 3:
                    repo_tag, img_id, size = parts
                    if repo_tag != '<none>:<none>':
                        images.append({
                            'repo_tag': repo_tag,
                            'id': img_id,
                            'size': size
                        })
        return images
    except subprocess.CalledProcessError:
        return []
    except Exception as e:
        safe_print(f"{Colors.RED}❌ Error getting images: {e}{Colors.NC}")
        return []

def list_docker_images():
    """List current Docker images"""
    print_line('─', 60, Colors.CYAN)
    safe_print(f"{Colors.BRIGHT_BLUE}📦 Current Docker Images{Colors.NC}")
    print_line('─', 60, Colors.CYAN)
    
    images = get_docker_images()
    
    if not images:
        safe_print(f"{Colors.YELLOW}⚠️  No Docker images found{Colors.NC}")
        safe_print("")
        return
    
    safe_print(f"{Colors.BRIGHT_GREEN}✨ Found {len(images)} image(s):{Colors.NC}")
    safe_print("")
    
    for i, img in enumerate(images, 1):
        safe_print(f"{Colors.BRIGHT_CYAN}  {i:2d}) {Colors.WHITE}{img['repo_tag']}{Colors.NC}")
        safe_print(f"{Colors.CYAN}      🆔 ID: {img['id']}  |  📊 Size: {img['size']}{Colors.NC}")
        if i < len(images):
            safe_print(f"{Colors.CYAN}      {'─' * 50}{Colors.NC}")
    
    safe_print("")

def list_tar_files():
    """List tar files in backup directory"""
    print_line('─', 60, Colors.CYAN)
    safe_print(f"{Colors.BRIGHT_BLUE}📚 Saved TAR Files{Colors.NC}")
    print_line('─', 60, Colors.CYAN)
    
    tar_files = list(BACKUP_DIR.glob('*.tar'))
    
    if not tar_files:
        safe_print(f"{Colors.YELLOW}⚠️  No TAR files found in backup directory{Colors.NC}")
        safe_print("")
        return []
    
    safe_print(f"{Colors.BRIGHT_GREEN}✨ Found {len(tar_files)} TAR file(s):{Colors.NC}")
    safe_print("")
    
    for i, file in enumerate(tar_files, 1):
        size_mb = file.stat().st_size / (1024 * 1024)
        safe_print(f"{Colors.BRIGHT_CYAN}  {i:2d}) {Colors.WHITE}{file.name}{Colors.NC}")
        safe_print(f"{Colors.CYAN}      💾 Size: {size_mb:.2f} MB{Colors.NC}")
        if i < len(tar_files):
            safe_print(f"{Colors.CYAN}      {'─' * 50}{Colors.NC}")
    
    safe_print("")
    return tar_files

def parse_selections(selections, max_num):
    """Parse user selections (supports comma-separated and ranges like 1,3-5)"""
    selected = set()
    parts = selections.replace(' ', '').split(',')
    
    for part in parts:
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                selected.update(range(start, end + 1))
            except ValueError:
                continue
        else:
            try:
                selected.add(int(part))
            except ValueError:
                continue
    
    return sorted([i for i in selected if 1 <= i <= max_num])

def save_images():
    """Save Docker images to tar files"""
    print_line('═', 60, Colors.BRIGHT_GREEN)
    safe_print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}💾 SAVE DOCKER IMAGES{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_GREEN)
    safe_print("")
    
    safe_print(f"{Colors.CYAN}Choose an option:{Colors.NC}")
    safe_print(f"{Colors.WHITE}  [A] Save ALL images{Colors.NC}")
    safe_print(f"{Colors.WHITE}  [S] Save SPECIFIC images{Colors.NC}")
    safe_print("")
    
    save_choice = input(f"{Colors.BRIGHT_CYAN}👉 Your choice (A/S): {Colors.NC}").strip().lower()
    
    images = get_docker_images()
    if not images:
        safe_print(f"\n{Colors.YELLOW}⚠️  No Docker images found. Nothing to save!{Colors.NC}")
        safe_print("")
        return
    
    selected_images = []
    
    if save_choice == 's':
        safe_print("")
        list_docker_images()
        safe_print(f"{Colors.CYAN}Enter image numbers (e.g., 1,3-5 or 1,2,4):{Colors.NC}")
        selections = input(f"{Colors.BRIGHT_CYAN}👉 Select: {Colors.NC}").strip()
        selected_indices = parse_selections(selections, len(images))
        selected_images = [images[i-1] for i in selected_indices]
    else:
        selected_images = images
    
    if not selected_images:
        safe_print(f"\n{Colors.YELLOW}⚠️  No images selected. Operation cancelled!{Colors.NC}")
        safe_print("")
        return
    
    print_line('─', 60, Colors.GREEN)
    safe_print(f"{Colors.BRIGHT_GREEN}🚀 Saving {len(selected_images)} image(s)...{Colors.NC}")
    print_line('─', 60, Colors.GREEN)
    safe_print("")
    
    success_count = 0
    for i, img in enumerate(selected_images, 1):
        safe_name = img['repo_tag'].replace('/', '_').replace(':', '_')
        filename = BACKUP_DIR / f"{safe_name}.tar"
        
        safe_print(f"{Colors.CYAN}📦 [{i}/{len(selected_images)}] {img['repo_tag']}{Colors.NC}")
        safe_print(f"{Colors.CYAN}   → {filename.name}{Colors.NC}")
        
        try:
            run_docker_command(['docker', 'save', '-o', str(filename), img['repo_tag']], capture=False)
            safe_print(f"{Colors.BRIGHT_GREEN}   ✅ Saved successfully!{Colors.NC}")
            success_count += 1
        except subprocess.CalledProcessError:
            safe_print(f"{Colors.BRIGHT_RED}   ❌ Failed to save!{Colors.NC}")
        except Exception as e:
            safe_print(f"{Colors.BRIGHT_RED}   ❌ Error: {e}{Colors.NC}")
        
        if i < len(selected_images):
            safe_print("")
    
    print_line('═', 60, Colors.BRIGHT_GREEN)
    safe_print(f"{Colors.BRIGHT_GREEN}✨ Completed! {success_count}/{len(selected_images)} images saved successfully{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_GREEN)
    safe_print("")

def load_images():
    """Load tar files as Docker images"""
    print_line('═', 60, Colors.BRIGHT_BLUE)
    safe_print(f"{Colors.BRIGHT_BLUE}{Colors.BOLD}📥 LOAD DOCKER IMAGES{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_BLUE)
    safe_print("")
    
    safe_print(f"{Colors.CYAN}Choose an option:{Colors.NC}")
    safe_print(f"{Colors.WHITE}  [A] Load ALL tar files{Colors.NC}")
    safe_print(f"{Colors.WHITE}  [S] Load SPECIFIC tar files{Colors.NC}")
    safe_print("")
    
    load_choice = input(f"{Colors.BRIGHT_CYAN}👉 Your choice (A/S): {Colors.NC}").strip().lower()
    
    tar_files = list(BACKUP_DIR.glob('*.tar'))
    if not tar_files:
        safe_print(f"\n{Colors.YELLOW}⚠️  No TAR files found in {BACKUP_DIR}{Colors.NC}")
        safe_print("")
        return
    
    selected_files = []
    
    if load_choice == 's':
        safe_print("")
        list_tar_files()
        safe_print(f"{Colors.CYAN}Enter file numbers (e.g., 1,3-5 or 1,2,4):{Colors.NC}")
        selections = input(f"{Colors.BRIGHT_CYAN}👉 Select: {Colors.NC}").strip()
        selected_indices = parse_selections(selections, len(tar_files))
        selected_files = [tar_files[i-1] for i in selected_indices]
    else:
        selected_files = tar_files
    
    if not selected_files:
        safe_print(f"\n{Colors.YELLOW}⚠️  No files selected. Operation cancelled!{Colors.NC}")
        safe_print("")
        return
    
    print_line('─', 60, Colors.BLUE)
    safe_print(f"{Colors.BRIGHT_BLUE}🚀 Loading {len(selected_files)} file(s)...{Colors.NC}")
    print_line('─', 60, Colors.BLUE)
    safe_print("")
    
    success_count = 0
    for i, file in enumerate(selected_files, 1):
        safe_print(f"{Colors.CYAN}📦 [{i}/{len(selected_files)}] {file.name}{Colors.NC}")
        
        try:
            run_docker_command(['docker', 'load', '-i', str(file)], capture=False)
            safe_print(f"{Colors.BRIGHT_GREEN}   ✅ Loaded successfully!{Colors.NC}")
            success_count += 1
        except subprocess.CalledProcessError:
            safe_print(f"{Colors.BRIGHT_RED}   ❌ Failed to load!{Colors.NC}")
        except Exception as e:
            safe_print(f"{Colors.BRIGHT_RED}   ❌ Error: {e}{Colors.NC}")
        
        if i < len(selected_files):
            safe_print("")
    
    print_line('═', 60, Colors.BRIGHT_BLUE)
    safe_print(f"{Colors.BRIGHT_BLUE}✨ Completed! {success_count}/{len(selected_files)} files loaded successfully{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_BLUE)
    safe_print("")

def delete_tar_files():
    """Delete specific tar files"""
    print_line('═', 60, Colors.BRIGHT_RED)
    safe_print(f"{Colors.BRIGHT_RED}{Colors.BOLD}🗑️  DELETE TAR FILES{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_RED)
    safe_print("")
    
    tar_files = list_tar_files()
    
    if not tar_files:
        return
    
    safe_print(f"{Colors.CYAN}Enter file numbers to delete (e.g., 1,3-5 or 1,2,4):{Colors.NC}")
    selections = input(f"{Colors.BRIGHT_CYAN}👉 Select: {Colors.NC}").strip()
    selected_indices = parse_selections(selections, len(tar_files))
    selected_files = [tar_files[i-1] for i in selected_indices]
    
    if not selected_files:
        safe_print(f"\n{Colors.YELLOW}⚠️  No files selected. Operation cancelled!{Colors.NC}")
        safe_print("")
        return
    
    print_line('─', 60, Colors.YELLOW)
    safe_print(f"{Colors.BRIGHT_YELLOW}⚠️  WARNING: You are about to delete {len(selected_files)} file(s)!{Colors.NC}")
    safe_print(f"{Colors.YELLOW}⚠️  This action is PERMANENT and cannot be undone!{Colors.NC}")
    print_line('─', 60, Colors.YELLOW)
    safe_print("")
    
    safe_print(f"{Colors.WHITE}Files to be deleted:{Colors.NC}")
    for file in selected_files:
        safe_print(f"{Colors.RED}  🗑️  {file.name}{Colors.NC}")
    safe_print("")
    
    confirm = input(f"{Colors.BRIGHT_RED}❓ Are you sure? Type 'YES' to confirm: {Colors.NC}").strip()
    
    if confirm.upper() != 'YES':
        safe_print(f"\n{Colors.YELLOW}✋ Deletion cancelled. Files are safe!{Colors.NC}")
        safe_print("")
        return
    
    safe_print("")
    success_count = 0
    for file in selected_files:
        safe_print(f"{Colors.CYAN}🗑️  Deleting {file.name}...{Colors.NC}")
        try:
            file.unlink()
            safe_print(f"{Colors.GREEN}   ✅ Deleted successfully{Colors.NC}")
            success_count += 1
        except OSError as e:
            safe_print(f"{Colors.RED}   ❌ Failed: {e}{Colors.NC}")
    
    print_line('═', 60, Colors.GREEN)
    safe_print(f"{Colors.BRIGHT_GREEN}✨ Completed! {success_count}/{len(selected_files)} files deleted{Colors.NC}")
    print_line('═', 60, Colors.GREEN)
    safe_print("")

def show_help():
    """Show help information"""
    safe_print("")
    print_line('═', 60, Colors.BRIGHT_MAGENTA)
    safe_print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}{'📚 HELP & ABOUT':^60}{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_MAGENTA)
    safe_print("")
    
    safe_print(f"{Colors.BRIGHT_CYAN}🎯 Purpose:{Colors.NC}")
    safe_print(f"{Colors.WHITE}   This tool helps you manage Docker images by saving and loading")
    safe_print(f"{Colors.WHITE}   them as TAR files for backup, transfer, or archival purposes.{Colors.NC}")
    safe_print("")
    
    safe_print(f"{Colors.BRIGHT_CYAN}✨ Features:{Colors.NC}")
    features = [
        "💾 Save Docker images to TAR files (all or specific)",
        "📥 Load TAR files back as Docker images",
        "📦 List current Docker images with details",
        "📚 List saved TAR files with sizes",
        "🗑️  Delete TAR files safely",
        "🎨 Beautiful colorful output",
        "🪟 Windows + 🐧 Linux compatible",
        "😊 User-friendly interface with emojis"
    ]
    for feature in features:
        safe_print(f"{Colors.WHITE}   • {feature}{Colors.NC}")
    safe_print("")
    
    safe_print(f"{Colors.BRIGHT_CYAN}💡 Tips:{Colors.NC}")
    safe_print(f"{Colors.WHITE}   • Use comma-separated numbers: 1,3,5{Colors.NC}")
    safe_print(f"{Colors.WHITE}   • Use ranges for convenience: 1-5 or 1,3-5,7{Colors.NC}")
    safe_print(f"{Colors.WHITE}   • TAR files are saved in the 'backups' folder{Colors.NC}")
    safe_print(f"{Colors.WHITE}   • Large images may take time to save/load{Colors.NC}")
    safe_print("")
    
    safe_print(f"{Colors.BRIGHT_CYAN}⚙️  Requirements:{Colors.NC}")
    safe_print(f"{Colors.WHITE}   • Docker Desktop installed and running{Colors.NC}")
    safe_print(f"{Colors.WHITE}   • Python 3.6 or higher{Colors.NC}")
    safe_print(f"{Colors.WHITE}   • Sufficient disk space for TAR files{Colors.NC}")
    safe_print("")
    
    print_line('─', 60, Colors.MAGENTA)
    safe_print(f"{Colors.BRIGHT_MAGENTA}💖 Made with love by AI Assistant 🤖{Colors.NC}")
    safe_print(f"{Colors.MAGENTA}Version 3.0 - Ultra Beautiful Edition ✨{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_MAGENTA)
    safe_print("")

def show_menu():
    """Display main menu"""
    print_line('═', 60, Colors.BRIGHT_CYAN)
    safe_print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}{'📋 MAIN MENU':^60}{Colors.NC}")
    print_line('═', 60, Colors.BRIGHT_CYAN)
    safe_print("")
    
    menu_items = [
        (f"{Colors.BRIGHT_GREEN}1{Colors.NC}", "💾 Save Docker images to TAR files"),
        (f"{Colors.BRIGHT_BLUE}2{Colors.NC}", "📥 Load TAR files as Docker images"),
        (f"{Colors.BRIGHT_CYAN}3{Colors.NC}", "📦 List current Docker images"),
        (f"{Colors.BRIGHT_CYAN}4{Colors.NC}", "📚 List saved TAR files"),
        (f"{Colors.BRIGHT_RED}5{Colors.NC}", "🗑️  Delete TAR files"),
        (f"{Colors.BRIGHT_MAGENTA}6{Colors.NC}", "📚 Help & About"),
        (f"{Colors.BRIGHT_RED}7{Colors.NC}", "🚪 Exit")
    ]
    
    for num, desc in menu_items:
        safe_print(f"  {num}) {Colors.WHITE}{desc}{Colors.NC}")
    
    safe_print("")
    print_line('─', 60, Colors.CYAN)

def main():
    """Main function - Runs in infinite loop until user exits"""
    display_header()
    check_docker()
    
    while True:
        try:
            show_menu()
            
            choice = input(f"{Colors.BRIGHT_CYAN}👉 Your choice: {Colors.NC}").strip()
            safe_print("")
            
            if choice == '1':
                save_images()
            elif choice == '2':
                load_images()
            elif choice == '3':
                list_docker_images()
            elif choice == '4':
                list_tar_files()
            elif choice == '5':
                delete_tar_files()
            elif choice == '6':
                show_help()
            elif choice == '7':
                print_line('═', 60, Colors.BRIGHT_YELLOW)
                safe_print(f"{Colors.BRIGHT_YELLOW}👋 Goodbye! Have a great day! ✨{Colors.NC}")
                print_line('═', 60, Colors.BRIGHT_YELLOW)
                safe_print("")
                sys.exit(0)
            else:
                safe_print(f"{Colors.BRIGHT_RED}❌ Invalid choice! Please select 1-7{Colors.NC}")
                safe_print("")
                continue
            
            print_line('═', 60, Colors.BRIGHT_GREEN)
            safe_print(f"{Colors.BRIGHT_GREEN}✅ Operation completed successfully!{Colors.NC}")
            safe_print(f"{Colors.CYAN}💡 Ready for next operation...{Colors.NC}")
            print_line('═', 60, Colors.BRIGHT_GREEN)
            safe_print("")
            
            # Ask if user wants to continue
            continue_choice = input(f"{Colors.BRIGHT_CYAN}🔄 Press Enter to continue or type 'exit' to quit: {Colors.NC}").strip().lower()
            if continue_choice == 'exit':
                print_line('═', 60, Colors.BRIGHT_YELLOW)
                safe_print(f"{Colors.BRIGHT_YELLOW}👋 Goodbye! Have a great day! ✨{Colors.NC}")
                print_line('═', 60, Colors.BRIGHT_YELLOW)
                safe_print("")
                break
            safe_print("")
        
        except KeyboardInterrupt:
            safe_print(f"\n\n{Colors.BRIGHT_YELLOW}⚠️  Operation interrupted by user{Colors.NC}")
            retry = input(f"{Colors.CYAN}🔄 Return to main menu? (Y/N): {Colors.NC}").strip().lower()
            if retry != 'y':
                safe_print(f"{Colors.YELLOW}👋 Goodbye!{Colors.NC}")
                safe_print("")
                break
            safe_print("")
        
        except Exception as e:
            safe_print(f"\n{Colors.BRIGHT_RED}{'═' * 60}{Colors.NC}")
            safe_print(f"{Colors.BRIGHT_RED}❌ UNEXPECTED ERROR{Colors.NC}")
            safe_print(f"{Colors.BRIGHT_RED}{'═' * 60}{Colors.NC}")
            safe_print(f"{Colors.RED}{str(e)}{Colors.NC}")
            safe_print(f"{Colors.BRIGHT_RED}{'═' * 60}{Colors.NC}")
            safe_print("")
            retry = input(f"{Colors.CYAN}🔄 Return to main menu? (Y/N): {Colors.NC}").strip().lower()
            if retry != 'y':
                break
            safe_print("")

if __name__ == '__main__':
    main()