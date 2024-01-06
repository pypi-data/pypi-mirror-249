import argparse
import sys
from youtube_downloaders import VERSION


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Download", description="Download Youtube CLI"
    )
    parser.add_argument("-v", "--version", action="version", version=VERSION)
    subparser = parser.add_subparsers(dest="subparser")
    parser_video = subparser.add_parser("video", help="video to download")
    parser_video.add_argument(
        "-url",
        "--urlpath",
        required=True,
        type=str,
        help="URL of the single video to download",
    )
    parser_video.add_argument(
        "-save",
        "--savepath",
        required=True,
        type=str,
        help="location on OS to save the single video",
    )
    parser_playlist = subparser.add_parser("playlist", help="playlist to download")
    parser_playlist.add_argument(
        "-url",
        "--urlpath",
        required=True,
        type=str,
        help="URL of the playlist to download",
    )
    parser_playlist.add_argument(
        "-num",
        required=False,
        type=int,
        default=1,
        help="number of parallel videos to be downloaded",
    )
    parser_playlist.add_argument(
        "-save",
        "--savepath",
        required=True,
        type=str,
        help="location on OS to save the playlist",
    )
    parser.add_argument(
        "-gui",
        "--gui_console",
        required=False,
        action="store_true",
        help="download videos using Graphical Interface",
    )
    parser.add_argument(
        "-web",
        "--web_console",
        required=False,
        action="store_true",
        help="download videos using Web Console",
    )
    return parser


def parse():
    parser = create_parser()
    known, unknown = parser.parse_known_args()
    if hasattr(known, "gui_console"):
        return parser.parse_args()
    if hasattr(known, "web_console"):
        return parser.parse_args()
    if not hasattr(known, "subparser") or known.subparser is None:
        print("Please specified right parameters")
        parser.print_help()
        sys.exit()
    if len(unknown) != 0:
        print(f"BAD Specified parameter : {unknown}")
        parser.print_help()
        sys.exit()
    return known
