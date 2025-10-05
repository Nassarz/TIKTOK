#!/usr/bin/env python3
"""
Test script for TikTok downloader core functionality (without GUI)
"""

import requests
from bs4 import BeautifulSoup
import json
import re


def test_tiktok_scraper(url):
    """Test the TikTok scraping logic"""
    print(f"Testing TikTok scraper with URL: {url}")
    
    try:
        # Get the actual URL if it's a shortened link
        if 'vm.tiktok.com' in url:
            print("Resolving shortened URL...")
            response = requests.head(url, allow_redirects=True, timeout=10)
            url = response.url
            print(f"Resolved to: {url}")
        
        # Fetch the TikTok page
        print("Fetching TikTok page...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"Response status: {response.status_code}")
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        print("HTML parsed successfully")
        
        # Try to extract JSON data from the page
        script_tags = soup.find_all('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
        if not script_tags:
            script_tags = soup.find_all('script', type='application/json')
        
        print(f"Found {len(script_tags)} JSON script tags")
        
        # Check for title to verify it's a TikTok page
        title = soup.find('title')
        if title:
            print(f"Page title: {title.string[:100]}")
        
        # Look for SIGI_STATE data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'SIGI_STATE' in script.string:
                print("Found SIGI_STATE data in page")
                break
        
        print("\n✓ Core scraping functionality works!")
        print("Note: Actual media extraction depends on TikTok's current page structure")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    modules = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('pillow', 'PIL'),
    ]
    
    all_ok = True
    for package, module in modules:
        try:
            __import__(module)
            print(f"  ✓ {package} ({module})")
        except ImportError:
            print(f"  ✗ {package} ({module}) - NOT INSTALLED")
            all_ok = False
    
    return all_ok


if __name__ == "__main__":
    print("=" * 60)
    print("TikTok Downloader - Core Functionality Test")
    print("=" * 60)
    print()
    
    # Test imports
    if not test_imports():
        print("\n✗ Some required packages are missing!")
        print("Run: pip install -r requirements.txt")
    else:
        print("\n✓ All required packages are installed")
    
    print("\n" + "=" * 60)
    print("Note: Full GUI testing requires tkinter (python3-tk package)")
    print("The GUI application can be run with: python tiktok_downloader.py")
    print("=" * 60)
