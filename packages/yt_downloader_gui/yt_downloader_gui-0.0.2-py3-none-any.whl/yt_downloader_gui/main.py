"""General module."""
from yt_downloader_gui.youtube_downloader import YouTubeDownloader

def main():
    """Create app and start."""
    app = YouTubeDownloader()
    app.mainloop()

if __name__ == "__main__":
    main()