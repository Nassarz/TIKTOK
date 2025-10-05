#!/usr/bin/env python3
"""
Example usage of the TikTok Downloader

This script demonstrates how to use the TikTok downloader programmatically
without the GUI, for testing purposes.
"""

import sys
import os
sys.path.insert(0, '/home/runner/work/TIKTOK/TIKTOK')

# Set display for headless operation
os.environ['DISPLAY'] = ':99'

# Start a virtual display if not already running
import subprocess
try:
    subprocess.run(['pgrep', 'Xvfb'], check=True, capture_output=True)
except subprocess.CalledProcessError:
    # Xvfb not running, start it
    xvfb = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '800x600x24'],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    import time
    time.sleep(2)

from tiktok_downloader import TikTokDownloader
import tkinter as tk

def test_url_parsing():
    """Test URL parsing functionality"""
    print("Testing TikTok URL Parsing")
    print("-" * 50)
    
    root = tk.Tk()
    root.withdraw()  # Hide the window
    downloader = TikTokDownloader(root)
    
    # Test various URL formats
    test_urls = [
        "https://www.tiktok.com/@charlidamelio/video/7000000000000000000",
        "https://www.tiktok.com/@user/video/1234567890",
        "https://vm.tiktok.com/ZS8JKLmno/",
        "https://vt.tiktok.com/ZS9ABCdef/",
    ]
    
    print("\nTesting Video ID Extraction:")
    for url in test_urls:
        video_id = downloader.extract_video_id(url)
        print(f"  URL: {url}")
        print(f"  Video ID: {video_id}\n")
    
    root.destroy()
    print("-" * 50)


def test_filename_sanitization():
    """Test filename sanitization"""
    print("\nTesting Filename Sanitization")
    print("-" * 50)
    
    root = tk.Tk()
    root.withdraw()  # Hide the window
    downloader = TikTokDownloader(root)
    
    test_filenames = [
        "Normal video title",
        "Video with / invalid \\ chars : * ? \" < > |",
        "   Spaces everywhere   ",
        "Very long title " * 20,
        "",
    ]
    
    for filename in test_filenames:
        sanitized = downloader.sanitize_filename(filename)
        print(f"Original:  '{filename[:50]}'")
        print(f"Sanitized: '{sanitized}'\n")
    
    root.destroy()
    print("-" * 50)


def test_parsing_methods():
    """Test that parsing methods are available"""
    print("\nTesting Parsing Methods Availability")
    print("-" * 50)
    
    root = tk.Tk()
    root.withdraw()  # Hide the window
    downloader = TikTokDownloader(root)
    
    methods = [
        'extract_video_id',
        'scrape_tiktok_data',
        'parse_tiktok_json',
        'parse_sigi_state',
        'use_api_fallback',
        'download_video',
        'download_image',
        'download_all_as_zip',
    ]
    
    print("\nAvailable methods:")
    for method_name in methods:
        has_method = hasattr(downloader, method_name)
        status = "✓" if has_method else "✗"
        print(f"  {status} {method_name}")
    
    root.destroy()
    print("\n" + "-" * 50)


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("TikTok Downloader - Example Usage & Tests")
    print("=" * 50 + "\n")
    
    test_url_parsing()
    test_filename_sanitization()
    test_parsing_methods()
    
    print("\n" + "=" * 50)
    print("To run the GUI application:")
    print("  python tiktok_downloader.py")
    print("=" * 50 + "\n")
