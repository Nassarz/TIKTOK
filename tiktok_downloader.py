#!/usr/bin/env python3
"""
TikTok Downloader with GUI
Downloads TikTok videos without watermark and photo slideshows with all images.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import requests
from bs4 import BeautifulSoup
import json
import re
import os
import zipfile
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageTk
import threading


class TikTokDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Downloader")
        self.root.geometry("900x700")
        
        # Variables
        self.url_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.media_data = None
        self.image_frames = []
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI components"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # URL Input Section
        url_frame = ttk.LabelFrame(main_frame, text="TikTok URL", padding="10")
        url_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        ttk.Label(url_frame, text="Enter TikTok URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=60)
        url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        download_btn = ttk.Button(url_frame, text="Download", command=self.start_download)
        download_btn.grid(row=1, column=1)
        
        # Status Section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Content Display Section
        self.content_frame = ttk.LabelFrame(main_frame, text="Downloaded Content", padding="10")
        self.content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Scrollable canvas for images
        self.canvas = tk.Canvas(self.content_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
    def start_download(self):
        """Start download in a separate thread"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a TikTok URL")
            return
            
        if not re.match(r'https?://(www\.)?(tiktok\.com|vm\.tiktok\.com)', url):
            messagebox.showerror("Error", "Invalid TikTok URL")
            return
        
        # Clear previous content
        self.clear_content()
        
        # Start download in thread to keep GUI responsive
        thread = threading.Thread(target=self.download_media, args=(url,))
        thread.daemon = True
        thread.start()
        
    def clear_content(self):
        """Clear the content display area"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_frames = []
        self.media_data = None
        
    def download_media(self, url):
        """Download media from TikTok URL"""
        try:
            self.update_status("Fetching TikTok data...")
            
            # Get the actual URL if it's a shortened link
            if 'vm.tiktok.com' in url:
                response = requests.head(url, allow_redirects=True, timeout=10)
                url = response.url
            
            # Fetch the TikTok page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract JSON data from the page
            script_tags = soup.find_all('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
            if not script_tags:
                script_tags = soup.find_all('script', type='application/json')
            
            data = None
            for script in script_tags:
                try:
                    data = json.loads(script.string)
                    break
                except:
                    continue
            
            if not data:
                # Try alternative method - look for SIGI_STATE
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string and 'SIGI_STATE' in script.string:
                        match = re.search(r'SIGI_STATE\s*=\s*({.+?})\s*;', script.string, re.DOTALL)
                        if match:
                            try:
                                data = json.loads(match.group(1))
                                break
                            except:
                                continue
            
            if data:
                self.process_tiktok_data(data, url)
            else:
                # Fallback: Try to use SnaptikAPI method
                self.download_with_snaptik(url)
                
        except requests.exceptions.RequestException as e:
            self.update_status(f"Error: Network error - {str(e)}")
            messagebox.showerror("Error", f"Failed to fetch TikTok data: {str(e)}")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
    def process_tiktok_data(self, data, url):
        """Process extracted TikTok data"""
        try:
            # Try to find video or image data in the JSON structure
            video_url = None
            image_urls = []
            
            # Navigate through the JSON to find media
            if '__DEFAULT_SCOPE__' in data:
                scope_data = data['__DEFAULT_SCOPE__']
                
                # Look for video or image data
                for key, value in scope_data.items():
                    if isinstance(value, dict):
                        # Check for video
                        if 'video' in value:
                            video_data = value['video']
                            if 'downloadAddr' in video_data:
                                video_url = video_data['downloadAddr']
                            elif 'playAddr' in video_data:
                                video_url = video_data['playAddr']
                        
                        # Check for image slideshow
                        if 'imagePost' in value:
                            images = value['imagePost'].get('images', [])
                            for img in images:
                                if 'imageURL' in img:
                                    image_urls.append(img['imageURL']['urlList'][0])
                                elif 'displayImage' in img:
                                    image_urls.append(img['displayImage']['urlList'][0])
            
            # Alternative structure search
            if not video_url and not image_urls:
                self.search_media_in_data(data, video_url, image_urls)
            
            if video_url:
                self.download_video(video_url)
            elif image_urls:
                self.download_images(image_urls)
            else:
                # Try alternative download method
                self.download_with_snaptik(url)
                
        except Exception as e:
            self.update_status(f"Error processing data: {str(e)}")
            # Try fallback method
            self.download_with_snaptik(url)
            
    def search_media_in_data(self, data, video_url, image_urls):
        """Recursively search for media URLs in data"""
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['downloadAddr', 'playAddr'] and isinstance(value, str):
                    return value
                elif key == 'images' and isinstance(value, list):
                    for img in value:
                        if isinstance(img, dict):
                            for img_key in ['imageURL', 'displayImage']:
                                if img_key in img and 'urlList' in img[img_key]:
                                    image_urls.append(img[img_key]['urlList'][0])
                else:
                    result = self.search_media_in_data(value, video_url, image_urls)
                    if result:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = self.search_media_in_data(item, video_url, image_urls)
                if result:
                    return result
        return None
        
    def download_with_snaptik(self, url):
        """Download using SnapTik service as fallback"""
        try:
            self.update_status("Using alternative download method...")
            
            # SnapTik API endpoint
            api_url = "https://snaptik.app/abc2.php"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            }
            
            data = {
                'url': url,
                'lang': 'en'
            }
            
            response = requests.post(api_url, headers=headers, data=data, timeout=15)
            
            if response.status_code == 200:
                # Parse the response to find download links
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for download links
                download_links = soup.find_all('a', {'class': 'download-file'})
                
                if download_links:
                    # Get the no-watermark video link
                    video_url = None
                    for link in download_links:
                        href = link.get('href')
                        if href and 'watermark' not in href.lower():
                            video_url = href
                            break
                    
                    if not video_url and download_links:
                        video_url = download_links[0].get('href')
                    
                    if video_url:
                        self.download_video(video_url)
                        return
                
                # Check for images
                img_tags = soup.find_all('img', {'class': 'image-item'})
                if img_tags:
                    image_urls = [img.get('src') for img in img_tags if img.get('src')]
                    if image_urls:
                        self.download_images(image_urls)
                        return
            
            self.update_status("Error: Could not extract media from TikTok")
            messagebox.showerror("Error", "Failed to extract media. The URL might be invalid or the video is private.")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Download failed: {str(e)}")
            
    def download_video(self, video_url):
        """Download video without watermark"""
        try:
            self.update_status("Downloading video...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
            
            response = requests.get(video_url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            # Ask user where to save
            filename = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")],
                initialfile=f"tiktok_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            )
            
            if filename:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                self.update_status(f"Video saved: {filename}")
                messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {filename}")
                
                # Show confirmation in GUI
                ttk.Label(self.scrollable_frame, text=f"✓ Video saved: {os.path.basename(filename)}", 
                         foreground="green", font=('Arial', 12, 'bold')).pack(pady=20)
            else:
                self.update_status("Download cancelled")
                
        except Exception as e:
            self.update_status(f"Error downloading video: {str(e)}")
            messagebox.showerror("Error", f"Failed to download video: {str(e)}")
            
    def download_images(self, image_urls):
        """Download and display images with individual download buttons"""
        try:
            self.update_status(f"Loading {len(image_urls)} images...")
            self.media_data = {'images': [], 'urls': image_urls}
            
            # Add "Download All as ZIP" button
            button_frame = ttk.Frame(self.scrollable_frame)
            button_frame.pack(pady=10, fill=tk.X)
            
            ttk.Label(button_frame, text=f"Found {len(image_urls)} images", 
                     font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=10)
            
            download_all_btn = ttk.Button(
                button_frame, 
                text="Download All as ZIP",
                command=self.download_all_as_zip
            )
            download_all_btn.pack(side=tk.RIGHT, padx=10)
            
            # Download and display each image
            for idx, img_url in enumerate(image_urls, 1):
                try:
                    self.update_status(f"Loading image {idx}/{len(image_urls)}...")
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': 'https://www.tiktok.com/'
                    }
                    
                    response = requests.get(img_url, headers=headers, timeout=15)
                    response.raise_for_status()
                    
                    # Load image
                    img_data = BytesIO(response.content)
                    img = Image.open(img_data)
                    
                    # Store original image data
                    self.media_data['images'].append({
                        'data': response.content,
                        'index': idx
                    })
                    
                    # Create thumbnail for display
                    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    # Create frame for this image
                    img_frame = ttk.LabelFrame(self.scrollable_frame, text=f"Image {idx}", padding="10")
                    img_frame.pack(pady=10, padx=10, fill=tk.X)
                    
                    # Display image
                    img_label = ttk.Label(img_frame, image=photo)
                    img_label.image = photo  # Keep a reference
                    img_label.pack()
                    
                    # Download button for this image
                    download_btn = ttk.Button(
                        img_frame,
                        text=f"Download Image {idx}",
                        command=lambda i=idx-1: self.download_single_image(i)
                    )
                    download_btn.pack(pady=5)
                    
                    self.image_frames.append(img_frame)
                    
                except Exception as e:
                    print(f"Error loading image {idx}: {str(e)}")
                    continue
            
            self.update_status(f"Loaded {len(self.media_data['images'])} images successfully")
            
        except Exception as e:
            self.update_status(f"Error loading images: {str(e)}")
            messagebox.showerror("Error", f"Failed to load images: {str(e)}")
            
    def download_single_image(self, index):
        """Download a single image"""
        try:
            if not self.media_data or 'images' not in self.media_data:
                return
            
            img_data = self.media_data['images'][index]
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=f"tiktok_image_{img_data['index']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            
            if filename:
                with open(filename, 'wb') as f:
                    f.write(img_data['data'])
                
                messagebox.showinfo("Success", f"Image {img_data['index']} saved to: {filename}")
                self.update_status(f"Image {img_data['index']} saved successfully")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
            
    def download_all_as_zip(self):
        """Download all images as a ZIP file"""
        try:
            if not self.media_data or 'images' not in self.media_data:
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
                initialfile=f"tiktok_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            )
            
            if filename:
                self.update_status("Creating ZIP file...")
                
                with zipfile.ZipFile(filename, 'w') as zipf:
                    for img_data in self.media_data['images']:
                        img_name = f"image_{img_data['index']}.jpg"
                        zipf.writestr(img_name, img_data['data'])
                
                messagebox.showinfo("Success", f"All images saved to ZIP: {filename}")
                self.update_status(f"ZIP file created with {len(self.media_data['images'])} images")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create ZIP: {str(e)}")


def main():
    root = tk.Tk()
    app = TikTokDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
