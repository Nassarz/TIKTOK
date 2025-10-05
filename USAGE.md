# TikTok Downloader - Usage Guide

## Quick Start

### Installation
1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
python tiktok_downloader.py
```

## Features Overview

### 1. Video Downloads (No Watermark)
- Downloads TikTok videos without watermarks
- Extracts the original high-quality video
- Preserves video quality

**How to use:**
1. Copy a TikTok video URL
2. Paste into the URL field
3. Click "Fetch Media"
4. Click "Download Video"
5. Choose where to save the file

### 2. Photo Slideshow Downloads
- Detects photo slideshows automatically
- Displays all images with thumbnails
- Individual download buttons for each image
- Batch download option

**How to use:**
1. Copy a TikTok slideshow URL
2. Paste into the URL field
3. Click "Fetch Media"
4. View all images with previews
5. Options:
   - Download individual images
   - Download all as ZIP file

### 3. Status Updates
- Real-time status messages
- Error handling with clear messages
- Download progress tracking

## Supported URL Formats

The downloader supports various TikTok URL formats:

```
https://www.tiktok.com/@username/video/1234567890
https://vm.tiktok.com/XXXXXXX/
https://vt.tiktok.com/XXXXXXX/
```

## Web Scraping Approach

The application uses multiple methods to extract media:

1. **Direct HTML Scraping**
   - Fetches TikTok page HTML
   - Extracts embedded JSON data
   - Parses `__UNIVERSAL_DATA_FOR_REHYDRATION__`
   - Parses `SIGI_STATE` data

2. **API Fallback**
   - Uses third-party APIs if direct scraping fails
   - Ensures high success rate

## Error Handling

The application handles various error scenarios:

- **Invalid URL**: Shows warning message
- **Network Error**: Displays connection error
- **Missing Data**: Falls back to alternative methods
- **Download Failure**: Shows detailed error message

## Technical Details

### Video Processing
- Extracts video ID from various URL formats
- Fetches `downloadAddr` field (no watermark)
- Falls back to `playAddr` if needed
- Supports redirects for shortened URLs

### Slideshow Processing
- Extracts all image URLs from `imagePost` data
- Downloads highest quality images
- Creates ZIP archive with sequential naming
- Displays thumbnails (300x300) in GUI

### Filename Sanitization
- Removes invalid characters: `< > : " / \ | ? *`
- Trims whitespace
- Limits length to 100 characters
- Uses fallback name if empty

## Code Examples

### Using the Downloader Class Programmatically

```python
import tkinter as tk
from tiktok_downloader import TikTokDownloader

# Create GUI
root = tk.Tk()
app = TikTokDownloader(root)

# Set URL programmatically
app.url_var.set("https://www.tiktok.com/@user/video/123...")

# Start GUI
root.mainloop()
```

### Testing URL Extraction

```python
from tiktok_downloader import TikTokDownloader
import tkinter as tk

root = tk.Tk()
downloader = TikTokDownloader(root)

url = "https://www.tiktok.com/@user/video/1234567890"
video_id = downloader.extract_video_id(url)
print(f"Video ID: {video_id}")
```

## Troubleshooting

### GUI Won't Start
- Ensure tkinter is installed: `python -m tkinter`
- On Linux: `sudo apt-get install python3-tk`

### Downloads Fail
- Check internet connection
- Verify URL is valid and accessible
- Try a different TikTok URL
- Check if TikTok changed their page structure

### No Images in Slideshow
- Ensure the URL is actually a slideshow (not a video)
- Check network connectivity
- Try refreshing/re-fetching

### Slow Downloads
- Large files take time
- Check internet speed
- Multiple images download sequentially

## Privacy & Legal

**Important Notes:**
- This tool is for educational purposes
- Respect content creators' rights
- Only download content you have permission to use
- Follow TikTok's Terms of Service
- Do not use for copyright infringement

## Development

### Project Structure
```
TIKTOK/
├── tiktok_downloader.py   # Main application
├── requirements.txt        # Dependencies
├── README.md              # Project overview
├── USAGE.md              # This file
└── example_usage.py       # Example code
```

### Dependencies
- **requests**: HTTP requests and downloads
- **Pillow**: Image processing and thumbnails
- **tkinter**: GUI framework (included with Python)

### Testing
Run the example usage script:
```bash
python example_usage.py
```

## Future Enhancements

Potential improvements:
- [ ] Concurrent image downloads
- [ ] Better progress bars
- [ ] Video preview
- [ ] Download history
- [ ] Settings/preferences
- [ ] Multiple URL batch processing
- [ ] Custom save locations

## Support

For issues or questions:
1. Check this guide
2. Review README.md
3. Examine example_usage.py
4. Check GitHub issues

## Version History

**v1.0.0** - Initial Release
- Video downloads without watermark
- Photo slideshow support
- GUI with tkinter
- Web scraping implementation
- ZIP download for slideshows
- Error handling and status updates
