# Playlist URL: https://www.youtube.com/watch?v=nDyZb09cdyg&list=PL6XRrncXkMaW5p7muaR2s2IqjouQh4jqS

from datetime import datetime
from pytube import YouTube


def main():
    """
    This function downloads a video from a url given in a file.
    """
    with open('url.txt', 'r', encoding="utf-8") as f:
        # read the url
        url = f.read()

        now = datetime.now()

        print(
            f"Video download started at: {now.strftime('%d/%m/%Y %H:%M:%S')} from the url: {url}"
        )
        # Downloading a video
        yt = YouTube(url)
        yt.streams.filter(
            progressive=True, 
            file_extension='mp4'
        ).order_by(
            'resolution'
        ).desc().first().download()

        print(
            f"Video download finished at: {now.strftime('%d/%m/%Y %H:%M:%S')} from the url: {url}"
        )


if __name__ == '__main__':
    main()
