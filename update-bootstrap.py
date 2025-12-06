#!/usr/bin/env python3
"""
Bootstrap Version Updater

Updates Bootstrap CSS and JS files to the version specified in .bootstrap-version.
Downloads from CDN and updates:
  - styles/bootstrap-full.css
  - scripts/bootstrap-full.js
"""

import os
import sys
import urllib.request
from pathlib import Path

def print_status(status, message):
    """Print colored status messages"""
    colors = {
        'info': '\033[94m',
        'success': '\033[92m',
        'warning': '\033[93m',
        'error': '\033[91m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(status, '')}{message}{colors['reset']}")

def get_version():
    """Read Bootstrap version from .bootstrap-version file"""
    version_file = Path('.bootstrap-version')
    if not version_file.exists():
        print_status('error', 'Error: .bootstrap-version file not found')
        sys.exit(1)

    version = version_file.read_text().strip()
    if not version:
        print_status('error', 'Error: .bootstrap-version file is empty')
        sys.exit(1)

    return version

def download_file(url, filepath):
    """Download file from URL"""
    try:
        print_status('info', f'  Downloading: {url}')
        urllib.request.urlretrieve(url, filepath)
        size = os.path.getsize(filepath) / 1024  # KB
        print_status('success', f'  ✓ Downloaded ({size:.1f} KB)')
        return True
    except Exception as e:
        print_status('error', f'  ✗ Failed: {e}')
        return False

def update_readme(version):
    """Update Bootstrap version in README.adoc"""
    import re
    readme_path = Path('README.adoc')
    if not readme_path.exists():
        print_status('warning', 'Warning: README.adoc not found, skipping version update')
        return

    content = readme_path.read_text()
    updated = re.sub(
        r':bootstrap-version: [\d.]+',
        f':bootstrap-version: {version}',
        content
    )

    if updated != content:
        readme_path.write_text(updated)
        print_status('success', f'  ✓ README.adoc updated with version {version}')
    else:
        print_status('info', f'  ℹ README.adoc already has version {version}')

def main():
    """Main function"""
    print_status('info', '=' * 50)
    print_status('info', 'Bootstrap Update Script')
    print_status('info', '=' * 50)

    version = get_version()
    print_status('info', f'Target Bootstrap Version: {version}\n')

    # Download CSS
    print_status('info', 'Downloading Bootstrap CSS...')
    css_url = f'https://cdn.jsdelivr.net/npm/bootstrap@{version}/dist/css/bootstrap.min.css'
    if not download_file(css_url, 'styles/bootstrap-full.css'):
        sys.exit(1)

    print()

    # Download JS
    print_status('info', 'Downloading Bootstrap JS...')
    js_url = f'https://cdn.jsdelivr.net/npm/bootstrap@{version}/dist/js/bootstrap.bundle.min.js'
    if not download_file(js_url, 'scripts/bootstrap-full.js'):
        sys.exit(1)

    print()

    # Update README
    print_status('info', 'Updating README.adoc...')
    update_readme(version)

    print()
    print_status('info', '=' * 50)
    print_status('success', '✓ Bootstrap updated successfully!')
    print_status('info', '=' * 50)
    print_status('warning', '\nNext steps:')
    print_status('warning', '  1. Review changes with: git diff')
    print_status('warning', '  2. Test the build')
    print_status('warning', '  3. Commit the changes')

if __name__ == '__main__':
    main()
