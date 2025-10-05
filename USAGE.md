# TikTok Downloader - Usage Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python tiktok_downloader.py
   ```

3. **Download TikTok content:**
   - Paste a TikTok URL
   - Click "Download"
   - Save the media

## Supported URL Formats

The application supports various TikTok URL formats:

- `https://www.tiktok.com/@username/video/1234567890123456789`
- `https://tiktok.com/@username/video/1234567890123456789`
- `https://vm.tiktok.com/XXXXXXXXX/` (shortened URLs)
- `https://m.tiktok.com/@username/video/1234567890123456789` (mobile URLs)

## Features

### 1. Video Downloads

**What it does:**
- Extracts video without TikTok watermark
- Downloads original quality video
- Saves as MP4 format

**How to use:**
1. Paste video URL
2. Click "Download"
3. Choose save location
4. Video downloads automatically

**Example:**
```
URL: https://www.tiktok.com/@creator/video/7123456789012345678
Result: tiktok_video_20240101_120000.mp4 (no watermark)
```

### 2. Photo Slideshow Downloads

**What it does:**
- Fetches all images from slideshow posts
- Displays thumbnails in GUI
- Allows individual or batch download

**How to use:**
1. Paste slideshow URL
2. Click "Download"
3. Images appear in GUI
4. Download options:
   - Click button under each image to save individually
   - Click "Download All as ZIP" for batch download

**Example:**
```
URL: https://www.tiktok.com/@creator/video/7123456789012345678 (slideshow)
Result:
- Image preview gallery in GUI
- Individual download: image_1.jpg, image_2.jpg, etc.
- ZIP download: tiktok_images_20240101_120000.zip (contains all images)
```

## GUI Components

### URL Input Section
```
┌──────────────────────────────────────┐
│ Enter TikTok URL:                    │
│ [text field]              [Download] │
└──────────────────────────────────────┘
```
- **Text field:** Paste TikTok URL here
- **Download button:** Start the download process

### Status Section
```
┌──────────────────────────────────────┐
│ Status: Ready                        │
└──────────────────────────────────────┘
```
Shows current operation:
- "Ready" - Waiting for input
- "Fetching TikTok data..." - Scraping webpage
- "Downloading video..." - Getting video file
- "Loading images..." - Fetching slideshow images
- "Video saved: [filename]" - Success!
- "Error: [message]" - Problem occurred

### Content Display Section
```
┌──────────────────────────────────────┐
│ [Scrollable content area]            │
│                                      │
│ For videos: Success message          │
│ For images: Gallery with buttons     │
└──────────────────────────────────────┘
```

## Error Handling

The application handles various errors gracefully:

### Network Errors
```
Error: Network error - Connection timeout
```
**Solution:** Check internet connection and try again

### Invalid URLs
```
Error: Invalid TikTok URL
```
**Solution:** Ensure URL is from tiktok.com

### Private/Restricted Content
```
Error: Failed to extract media. The URL might be invalid or the video is private.
```
**Solution:** Content may be private or deleted

### Download Failures
```
Error: Failed to download video: [reason]
```
**Solution:** Check URL and try again

## Tips & Best Practices

### For Best Results:
1. **Use direct URLs:** Copy URL from browser address bar
2. **Wait for loading:** Large slideshows take time to load all images
3. **Check status:** Monitor status section for progress
4. **Save promptly:** Save files when prompted to avoid losing downloads

### Troubleshooting:

**Problem:** GUI doesn't open
```bash
# On Linux, install tkinter:
sudo apt-get install python3-tk

# On macOS, tkinter is usually included
# On Windows, tkinter comes with Python
```

**Problem:** Can't download video
- Check if video is public
- Try a different URL
- Verify internet connection

**Problem:** Images not loading
- Wait for all images to load (check status)
- Slideshow might have many images
- Check internet connection

## Advanced Usage

### Running Tests
```bash
# Test core functionality without GUI
python test_core.py

# View demo and features
python demo.py

# See GUI mockup
python GUI_MOCKUP.py
```

### Saving to Specific Locations
The application uses file dialogs, so you can:
- Choose custom save locations
- Rename files before saving
- Organize downloads in folders

### Batch Processing
For multiple slideshows:
1. Download first slideshow
2. Use "Download All as ZIP"
3. Clear and download next
4. Repeat as needed

## Technical Details

### Web Scraping Method
```python
1. Fetch TikTok page HTML
2. Extract embedded JSON data:
   - __UNIVERSAL_DATA_FOR_REHYDRATION__
   - SIGI_STATE
3. Parse media URLs from JSON
4. Download with proper headers
```

### Data Extraction Points
- Video: `downloadAddr` or `playAddr` fields
- Images: `imagePost.images[].imageURL.urlList[]`

### Fallback Mechanisms
1. Primary: Direct JSON extraction
2. Secondary: Alternative JSON structures
3. Tertiary: External service integration

## File Structure

```
TIKTOK/
├── tiktok_downloader.py    # Main GUI application
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── .gitignore             # Git ignore patterns
├── test_core.py           # Core functionality tests
├── demo.py                # Feature demonstration
├── GUI_MOCKUP.py          # Visual GUI representation
└── USAGE.md              # This file
```

## Dependencies

### Required Packages
```
requests>=2.31.0      # HTTP requests
beautifulsoup4>=4.12.0  # HTML parsing
pillow>=10.0.0         # Image processing
```

### System Requirements
```
Python: 3.7+
GUI: tkinter (python3-tk)
OS: Windows, macOS, Linux
Internet: Required for downloads
```

## Limitations

1. **Requires internet:** Cannot work offline
2. **Public content only:** Private videos not accessible
3. **TikTok changes:** May break if TikTok updates their site structure
4. **Rate limiting:** Frequent requests may be throttled
5. **Regional restrictions:** Some content may be geo-blocked

## Legal & Ethical Considerations

⚠️ **Important:**
- This tool is for **educational purposes** only
- Respect content creators' rights
- Follow TikTok's Terms of Service
- Only download content you have permission to use
- Don't redistribute downloaded content without permission

## Support

For issues or questions:
1. Check this usage guide
2. Review README.md
3. Run test scripts to diagnose issues
4. Check GitHub repository for updates

## Version Information

- **Version:** 1.0
- **Python:** 3.7+
- **License:** Educational/Open Source
- **Last Updated:** 2024

## Changelog

### Version 1.0 (Initial Release)
- ✓ GUI with tkinter
- ✓ Video downloads (no watermark)
- ✓ Photo slideshow support
- ✓ Individual image download
- ✓ ZIP batch download
- ✓ Error handling
- ✓ Status updates
- ✓ Web scraping implementation
