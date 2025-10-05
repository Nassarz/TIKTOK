"""
TikTok Media Downloader with GUI
Downloads TikTok videos (without watermark) and photo slideshows
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import re
import os
import zipfile
from io import BytesIO
from PIL import Image, ImageTk
from threading import Thread
from urllib.parse import urlparse, parse_qs
import time


class TikTokDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Media Downloader")
        self.root.geometry("800x600")
        
        # Variables
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.media_data = None
        self.image_widgets = []
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the GUI layout"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # URL input section
        ttk.Label(main_frame, text="TikTok URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        download_btn = ttk.Button(main_frame, text="Fetch Media", command=self.fetch_media)
        download_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Status label
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Scrollable frame for media display
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def clear_media_display(self):
        """Clear previous media display"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_widgets = []
    
    def fetch_media(self):
        """Fetch media in a separate thread"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a TikTok URL")
            return
        
        # Run in thread to avoid freezing UI
        thread = Thread(target=self._fetch_media_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _fetch_media_thread(self, url):
        """Fetch media from TikTok URL"""
        try:
            self.update_status("Fetching media data...")
            self.clear_media_display()
            
            # Extract video ID from URL
            video_id = self.extract_video_id(url)
            if not video_id:
                self.update_status("Error: Invalid TikTok URL")
                messagebox.showerror("Error", "Invalid TikTok URL")
                return
            
            # Fetch media data using web scraping
            media_data = self.scrape_tiktok_data(url)
            
            if not media_data:
                self.update_status("Error: Could not fetch media data")
                messagebox.showerror("Error", "Could not fetch media data. Please check the URL.")
                return
            
            self.media_data = media_data
            
            # Display based on media type
            if media_data['type'] == 'video':
                self.display_video_info(media_data)
            elif media_data['type'] == 'slideshow':
                self.display_slideshow(media_data)
            
            self.update_status("Media fetched successfully!")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_video_id(self, url):
        """Extract video ID from TikTok URL"""
        # Handle different URL formats
        patterns = [
            r'tiktok\.com/@[\w.-]+/video/(\d+)',
            r'tiktok\.com/.*?/video/(\d+)',
            r'vm\.tiktok\.com/([\w]+)',
            r'vt\.tiktok\.com/([\w]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def scrape_tiktok_data(self, url):
        """Scrape TikTok data using web scraping"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.tiktok.com/',
        }
        
        try:
            # Follow redirects for short URLs
            response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            response.raise_for_status()
            
            html_content = response.text
            
            # Extract JSON data from HTML
            # TikTok embeds data in a script tag with id="__UNIVERSAL_DATA_FOR_REHYDRATION__"
            json_pattern = r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>'
            match = re.search(json_pattern, html_content)
            
            if match:
                json_data = json.loads(match.group(1))
                return self.parse_tiktok_json(json_data)
            
            # Alternative: Try SIGI_STATE pattern
            sigi_pattern = r'<script id="SIGI_STATE" type="application/json">(.*?)</script>'
            match = re.search(sigi_pattern, html_content)
            
            if match:
                json_data = json.loads(match.group(1))
                return self.parse_sigi_state(json_data)
            
            # If no JSON found, try using a TikTok downloader API as fallback
            return self.use_api_fallback(url)
            
        except Exception as e:
            print(f"Error scraping TikTok: {e}")
            return None
    
    def parse_tiktok_json(self, json_data):
        """Parse TikTok JSON data"""
        try:
            # Navigate through the JSON structure
            default_scope = json_data.get('__DEFAULT_SCOPE__', {})
            video_detail = default_scope.get('webapp.video-detail', {})
            item_info = video_detail.get('itemInfo', {})
            item_struct = item_info.get('itemStruct', {})
            
            video_info = item_struct.get('video', {})
            image_post = item_struct.get('imagePost', {})
            
            # Check if it's a slideshow (has images)
            if image_post and image_post.get('images'):
                images = []
                for img in image_post['images']:
                    # Get highest quality image URL
                    img_urls = img.get('imageURL', {})
                    url_list = img_urls.get('urlList', [])
                    if url_list:
                        images.append(url_list[0])
                
                return {
                    'type': 'slideshow',
                    'images': images,
                    'title': item_struct.get('desc', 'TikTok Slideshow')
                }
            
            # It's a video
            elif video_info:
                # Get download URL (without watermark)
                download_url = video_info.get('downloadAddr', '')
                play_url = video_info.get('playAddr', '')
                
                return {
                    'type': 'video',
                    'download_url': download_url or play_url,
                    'title': item_struct.get('desc', 'TikTok Video')
                }
            
        except Exception as e:
            print(f"Error parsing JSON: {e}")
        
        return None
    
    def parse_sigi_state(self, json_data):
        """Parse SIGI_STATE JSON data"""
        try:
            # Try to find video detail in ItemModule
            item_module = json_data.get('ItemModule', {})
            
            for key, item in item_module.items():
                video_info = item.get('video', {})
                image_post = item.get('imagePost', {})
                
                # Check if slideshow
                if image_post and image_post.get('images'):
                    images = []
                    for img in image_post['images']:
                        img_urls = img.get('imageURL', {})
                        url_list = img_urls.get('urlList', [])
                        if url_list:
                            images.append(url_list[0])
                    
                    return {
                        'type': 'slideshow',
                        'images': images,
                        'title': item.get('desc', 'TikTok Slideshow')
                    }
                
                # Video
                elif video_info:
                    download_url = video_info.get('downloadAddr', '')
                    play_url = video_info.get('playAddr', '')
                    
                    return {
                        'type': 'video',
                        'download_url': download_url or play_url,
                        'title': item.get('desc', 'TikTok Video')
                    }
            
        except Exception as e:
            print(f"Error parsing SIGI_STATE: {e}")
        
        return None
    
    def use_api_fallback(self, url):
        """Use a third-party API as fallback"""
        # Using a free TikTok downloader API
        api_urls = [
            f"https://api.tiklydown.eu.org/api/download?url={url}",
            f"https://tikwm.com/api/?url={url}",
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        for api_url in api_urls:
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Parse response based on API
                    if 'video' in data and 'noWatermark' in data['video']:
                        # tikwm.com format
                        return {
                            'type': 'video',
                            'download_url': data['video']['noWatermark'],
                            'title': data.get('title', 'TikTok Video')
                        }
                    elif 'images' in data:
                        # Slideshow format
                        return {
                            'type': 'slideshow',
                            'images': data['images'],
                            'title': data.get('title', 'TikTok Slideshow')
                        }
                    elif 'video' in data and 'url' in data['video']:
                        # Alternative video format
                        return {
                            'type': 'video',
                            'download_url': data['video']['url'],
                            'title': data.get('title', 'TikTok Video')
                        }
            except Exception as e:
                print(f"API fallback error: {e}")
                continue
        
        return None
    
    def display_video_info(self, media_data):
        """Display video download option"""
        info_frame = ttk.Frame(self.scrollable_frame, padding="10")
        info_frame.pack(fill="x", pady=10)
        
        ttk.Label(info_frame, text="Video (No Watermark)", font=("Arial", 12, "bold")).pack(anchor="w")
        ttk.Label(info_frame, text=media_data['title'], wraplength=700).pack(anchor="w", pady=5)
        
        download_btn = ttk.Button(
            info_frame,
            text="Download Video",
            command=lambda: self.download_video(media_data['download_url'], media_data['title'])
        )
        download_btn.pack(pady=10)
    
    def display_slideshow(self, media_data):
        """Display slideshow images with individual download buttons"""
        header_frame = ttk.Frame(self.scrollable_frame, padding="10")
        header_frame.pack(fill="x")
        
        ttk.Label(header_frame, text="Photo Slideshow", font=("Arial", 12, "bold")).pack(anchor="w")
        ttk.Label(header_frame, text=media_data['title'], wraplength=700).pack(anchor="w", pady=5)
        ttk.Label(header_frame, text=f"Total Images: {len(media_data['images'])}", font=("Arial", 10)).pack(anchor="w")
        
        # Download All button
        download_all_btn = ttk.Button(
            header_frame,
            text="Download All as ZIP",
            command=lambda: self.download_all_as_zip(media_data['images'], media_data['title'])
        )
        download_all_btn.pack(pady=10)
        
        # Display images
        for idx, image_url in enumerate(media_data['images']):
            self.display_image_with_button(image_url, idx + 1)
    
    def display_image_with_button(self, image_url, index):
        """Display a single image with download button"""
        image_frame = ttk.Frame(self.scrollable_frame, padding="10", relief="solid", borderwidth=1)
        image_frame.pack(fill="x", pady=5)
        
        ttk.Label(image_frame, text=f"Image {index}", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Try to load and display thumbnail
        try:
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            
            # Resize for display
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            
            img_label = ttk.Label(image_frame, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(pady=5)
            
        except Exception as e:
            ttk.Label(image_frame, text=f"Preview not available: {str(e)}").pack(pady=5)
        
        # Download button for this image
        download_btn = ttk.Button(
            image_frame,
            text=f"Download Image {index}",
            command=lambda url=image_url, idx=index: self.download_image(url, idx)
        )
        download_btn.pack(pady=5)
    
    def download_video(self, url, title):
        """Download video file"""
        try:
            self.update_status("Downloading video...")
            
            # Ask for save location
            filename = self.sanitize_filename(title) + ".mp4"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
                initialfile=filename
            )
            
            if not filepath:
                self.update_status("Download cancelled")
                return
            
            # Download the video
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
            
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filepath, 'wb') as f:
                if total_size == 0:
                    f.write(response.content)
                else:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = (downloaded / total_size) * 100
                            self.update_status(f"Downloading: {progress:.1f}%")
            
            self.update_status(f"Video saved to {filepath}")
            messagebox.showinfo("Success", f"Video downloaded successfully!\n{filepath}")
            
        except Exception as e:
            self.update_status(f"Error downloading video: {str(e)}")
            messagebox.showerror("Error", f"Failed to download video: {str(e)}")
    
    def download_image(self, url, index):
        """Download a single image"""
        try:
            self.update_status(f"Downloading image {index}...")
            
            filename = f"tiktok_image_{index}.jpg"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
                initialfile=filename
            )
            
            if not filepath:
                self.update_status("Download cancelled")
                return
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            self.update_status(f"Image {index} saved to {filepath}")
            messagebox.showinfo("Success", f"Image {index} downloaded successfully!")
            
        except Exception as e:
            self.update_status(f"Error downloading image: {str(e)}")
            messagebox.showerror("Error", f"Failed to download image: {str(e)}")
    
    def download_all_as_zip(self, image_urls, title):
        """Download all images as a ZIP file"""
        try:
            self.update_status("Preparing ZIP file...")
            
            filename = self.sanitize_filename(title) + "_images.zip"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
                initialfile=filename
            )
            
            if not filepath:
                self.update_status("Download cancelled")
                return
            
            # Create ZIP file
            with zipfile.ZipFile(filepath, 'w') as zipf:
                for idx, img_url in enumerate(image_urls, 1):
                    self.update_status(f"Downloading image {idx}/{len(image_urls)}...")
                    
                    try:
                        response = requests.get(img_url, timeout=30)
                        response.raise_for_status()
                        
                        # Add to ZIP
                        img_filename = f"image_{idx}.jpg"
                        zipf.writestr(img_filename, response.content)
                        
                    except Exception as e:
                        print(f"Error downloading image {idx}: {e}")
                        continue
            
            self.update_status(f"All images saved to {filepath}")
            messagebox.showinfo("Success", f"All images downloaded as ZIP!\n{filepath}")
            
        except Exception as e:
            self.update_status(f"Error creating ZIP: {str(e)}")
            messagebox.showerror("Error", f"Failed to create ZIP: {str(e)}")
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Limit length
        filename = filename[:100]
        # Remove leading/trailing spaces
        filename = filename.strip()
        return filename if filename else "tiktok_media"


def main():
    root = tk.Tk()
    app = TikTokDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
