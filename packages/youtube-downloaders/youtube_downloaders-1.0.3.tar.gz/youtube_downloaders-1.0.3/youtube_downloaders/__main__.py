from youtube_downloaders import youtube as yt
from youtube_downloaders import options
from youtube_downloaders.gui import GUI
from youtube_downloaders.web import Web


def main():
    arg = options.parse()
    if arg.gui_console is True and arg.subparser is None:
        gui = GUI()
        gui.widget()
    if arg.web_console is True and arg.subparser is None:
        web = Web()
        web.run()
    if arg.subparser == "video":
        ytube = yt.youtube_download(arg.urlpath)
        ytube.download_single_video(arg.savepath)
    if arg.subparser == "playlist":
        ytube = yt.youtube_download(arg.urlpath)
        ytube.playlist_download(arg.num, arg.savepath)


if __name__ == "__main__":
    main()
