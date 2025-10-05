# TikTok Downloader - Quick Start Guide

## Installation (2 steps)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python tiktok_downloader.py
   ```

## How to Use (3 steps)

1. **Copy a TikTok URL**
   - Open TikTok and find a video or slideshow
   - Copy the URL (e.g., `https://www.tiktok.com/@user/video/123...`)

2. **Paste and Fetch**
   - Paste the URL in the application
   - Click "Fetch Media"

3. **Download**
   - **For Videos:** Click "Download Video" (no watermark!)
   - **For Slideshows:** Download individual images or use "Download All as ZIP"

## Features at a Glance

| Feature | Description |
|---------|-------------|
| 🎥 Videos | Download without watermark, original quality |
| 📸 Slideshows | All images with previews and thumbnails |
| 💾 Downloads | Individual or batch (ZIP) downloads |
| 🖼️ Preview | See images before downloading |
| ✅ Status | Real-time updates and error messages |
| 🌐 Scraping | Works without TikTok API |

## Example URLs

The app supports all TikTok URL formats:
```
https://www.tiktok.com/@username/video/1234567890
https://vm.tiktok.com/XXXXXXX/
https://vt.tiktok.com/XXXXXXX/
```

## Troubleshooting

**Problem:** GUI won't start  
**Solution:** Install tkinter: `sudo apt-get install python3-tk` (Linux)

**Problem:** Downloads fail  
**Solution:** Check internet connection and verify URL is valid

**Problem:** No images in slideshow  
**Solution:** Ensure URL is a slideshow (not video) and try re-fetching

## Need More Help?

- Read [USAGE.md](USAGE.md) for detailed guide
- Check [README.md](README.md) for overview
- Run [example_usage.py](example_usage.py) for tests

## Requirements

- Python 3.7+
- Internet connection
- Valid TikTok URLs

That's it! Enjoy downloading TikTok media! 🎉
