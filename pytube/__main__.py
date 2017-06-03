#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import argparse
import tkinter as tk
import re

from . import YouTube
from .utils import FullPaths, convert_mp3


def main():
    parser = argparse.ArgumentParser(description='YouTube video downloader')
    parser.add_argument('--paste_from_clipboard', default=True,
                        help='If should fetch URLs from clipboard. Assumes Chrome extension installed.')
    parser.add_argument("--path", "-p", action=FullPaths, default=os.getcwd(),
                        dest="path", help=("The path to save the video to."))
    args = parser.parse_args()
    if args.paste_from_clipboard:
        root = tk.Tk()
        root.withdraw()

        # Unpack JSON
        urls = [website['url'] for website in eval(root.clipboard_get())]
        batch_download(urls, args.path)

    # else:
    #     try:
    #         yt = YouTube(args.url)
    #         videos = []
    #         for i, video in enumerate(yt.get_videos()):
    #             ext = video.extension
    #             res = video.resolution
    #             videos.append((ext, res))
    #     except PytubeError:
    #         print("Incorrect video URL.")
    #         sys.exit(1)
    #
    #     if args.show_available:
    #         print_available_vids(videos)
    #         sys.exit(0)
    #
    #     if args.filename:
    #         yt.set_filename(args.filename)
    #
    #     if args.ext or args.res:
    #         if not all([args.ext, args.res]):
    #             print("Make sure you give either of the below specified "
    #                   "format/resolution combination.")
    #             print_available_vids(videos)
    #             sys.exit(1)
    #
    #     if args.ext and args.res:
    #         # There's only ope video that matches both so get it
    #         vid = yt.get(args.ext, args.res)
    #         # Check if there's a video returned
    #         if not vid:
    #             print("There's no video with the specified format/resolution "
    #                   "combination.")
    #             pprint(videos)
    #             sys.exit(1)
    #
    #     elif args.ext:
    #         # There are several videos with the same extension
    #         videos = yt.filter(extension=args.ext)
    #         # Check if we have a video
    #         if not videos:
    #             print("There are no videos in the specified format.")
    #             sys.exit(1)
    #         # Select the highest resolution one
    #         vid = max(videos)
    #     elif args.res:
    #         # There might be several videos in the same resolution
    #         videos = yt.filter(resolution=args.res)
    #         # Check if we have a video
    #         if not videos:
    #             print("There are no videos in the specified in the specified "
    #                   "resolution.")
    #             sys.exit(1)
    #         # Select the highest resolution one
    #         vid = max(videos)
    #     else:
    #         # If nothing is specified get the highest resolution one
    #         print_available_vids(videos)
    #         while True:
    #             try:
    #                 choice = int(input("Enter choice: "))
    #                 vid = yt.get(*videos[choice])
    #                 break
    #             except (ValueError, IndexError):
    #                 print("Requires an integer in range 0-{}".format(len(videos) - 1))
    #             except KeyboardInterrupt:
    #                 sys.exit(2)
    #
    #     try:
    #         vid.download(path=args.path, on_progress=print_status)
    #     except KeyboardInterrupt:
    #         print("Download interrupted.")
    #         sys.exit(1)


def print_available_vids(videos):
    formatString = "{:<2} {:<15} {:<15}"
    print(formatString.format("", "Resolution", "Extension"))
    print("-"*28)
    print("\n".join([formatString.format(index, *formatTuple) for index, formatTuple in enumerate(videos)]))


def batch_download(urls, download_path, convert_to_mp3=True, extension='mp4', quality='lowest'):
    """Download multiple YouTube videos and converts to mp3"""
    resolution_sorting = {'lowest': 0, 'highest': -1}
    for url in urls:
        yt = YouTube(url)
        print(yt.filename)
        yt.set_filename(yt.filename.strip())
        yt.set_filename(re.sub('\\W+', '-', yt.filename.strip()))
        resolution = sorted([video.resolution
                             for video in yt.filter(extension=extension)
                             ])[resolution_sorting[quality]]
        video = yt.get(extension=extension, resolution=resolution)
        print('Downloading {}...'.format(yt.filename))
        video.download(download_path, force_overwrite=True)
        if convert_to_mp3:
            video_path = download_path + '/' + yt.filename
            convert_mp3(video_path)


if __name__ == '__main__':
    main()
