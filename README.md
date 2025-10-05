# TikTok Downloader

A Python application with a GUI to download TikTok media without watermarks.

## Features

- **Video Downloads**: Download TikTok videos without watermark
- **Photo Slideshows**: Download all images from TikTok photo slideshows
- **GUI Interface**: User-friendly graphical interface built with Tkinter
- **Individual Downloads**: Download each image separately with dedicated buttons
- **Batch Download**: Download all images as a ZIP file with one click
- **Error Handling**: Comprehensive error handling with status updates
- **Web Scraping**: Uses web scraping techniques (no official API required)

## Requirements

- Python 3.7 or higher
- See `requirements.txt` for Python package dependencies

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Nassarz/TIKTOK.git
cd TIKTOK
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python tiktok_downloader.py
```

2. Enter a TikTok URL in the input field

3. Click the "Download" button

4. For videos:
   - Choose where to save the video file
   - Video will be downloaded without watermark

5. For photo slideshows:
   - All images will be displayed in the GUI
   - Click individual "Download Image" buttons to save specific images
   - Or click "Download All as ZIP" to save all images at once

## How It Works

The application uses web scraping to:
1. Fetch the TikTok page content
2. Extract JSON data embedded in the page
3. Locate media URLs (video or images)
4. Download media without watermarks

For videos, it extracts the original video URL without TikTok watermark.
For photo slideshows, it fetches all individual image URLs and displays them in the GUI.

## Features in Detail

### Video Downloads
- Automatically detects video content
- Downloads without TikTok watermark
- Saves as MP4 format

### Photo Slideshow Downloads
- Displays all images in the GUI
- Individual download buttons for each image
- Batch download option (ZIP file)
- Preview images before downloading

### Error Handling
- Network error handling
- Invalid URL detection
- Private/unavailable content notifications
- Status updates throughout the process

## Limitations

- Requires active internet connection
- May not work with private or restricted content
- Depends on TikTok's HTML structure (may break if TikTok changes their website)

## Disclaimer

This tool is for educational purposes only. Please respect content creators' rights and TikTok's Terms of Service. Only download content you have permission to download.

## License

This project is open source and available for educational purposes.
