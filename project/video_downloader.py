import yt_dlp
import os
from pathlib import Path

class BackgroundVideoDownloader:
    def __init__(self, output_dir="background", cookies_file=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.cookies_file = cookies_file

    def download_video(self, url: str, filename: str = None):
        """ Download a single video """

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(self.output_dir / (filename or '%(title)s.%(ext)s')),
            'quiet': False,
            'no_warnings': False,
        }

        if self.cookies_file:
            ydl_opts['cookiefile'] = self.cookies_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading: {url}")
                ydl.download([url])
                print(f"Downloaded Successfully: {url}")
        except Exception as e:
            print(f"Error Downloading {url}: {e}")

    def download_playlist(self, playlist_url: str, max_videos: int = 30):
        """ Download Multiple videos from a playlist """

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': str(self.output_dir / '%(playlist_index)s_%(title)s.%(ext)s'),
            'quiet': False,
            'playlistend': max_videos,
            'ignoreerrors': True,
        }

        if self.cookies_file:
            ydl_opts['cookiefile'] = self.cookies_file

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading playlist: {playlist_url}")
                ydl.download([playlist_url])
                print(f"Playlist downloaded {playlist_url}")
        except Exception as e:
            print(f"Error: Downloading Playlist: {playlist_url}")

    def download_from_list(self, video_urls: list):
        """ Download multiple videos from a list of URLs """
        for i, url in enumerate(video_urls, 1):
            print(f"\n[{i}]/{len(video_urls)}")
            self.download_video(url, f"background_{i:02d}.mp4")

if __name__ == "__main__":
    downloader = BackgroundVideoDownloader(output_dir="backgrounds", cookies_file=r"~/cookies.txt")

    video_list = ["https://youtu.be/OTfqQL-Tkaw?si=6oi0aXnmZeeOE1Cs",
                  "https://youtu.be/MPf716qQCjU?si=wRuy-BtG6G2C9z8I",
                  "https://youtu.be/Q6fkNkVymOA?si=up5IwK7jSwzz11uj",
                  "https://youtu.be/7yl7Wc1dtWc?si=QcNEkBz7hGvaq7Ju",
                  "https://youtu.be/XBIaqOm0RKQ?si=KBHMAL_8kGSpa6nw",
                  "https://youtu.be/tCBOhczn6Ok?si=iL-PqfQnKs0Wr9lJ"
                ]
    downloader.download_from_list(video_list)