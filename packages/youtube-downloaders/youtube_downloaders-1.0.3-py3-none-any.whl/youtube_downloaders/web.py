from flask import Flask, render_template, redirect, request
from youtube_downloaders.os_operations import operations as op
from youtube_downloaders.exception import youtubeException
from youtube_downloaders.youtube import youtube_download as ytd


class Web:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.add_url_rule('/',
                              'home',
                              self.home,
                              methods=['GET',
                                       'POST'
                                       ])
        self.op = op()
        self.folder_location = None
        self.vid_lookup = {}

    def run(self):
        self.app.run(host="127.0.0.1", port=5789, debug=True)

    def download_videos_list(self, url):
        self.ytd = ytd(url)
        return self.ytd.videos_from_url()

    def home(self):
        if request.method == "POST" and "form1" in request.form:
            user_option = request.form.get("type")
            url = request.form.get("url")
            folder_location = request.form.get("folderInput")
            self.folder_location = folder_location
            if user_option is None:
                error = f"Please selection one of the option: Video or Playlist"
                return render_template("error.html", error=error)
            # Check if the directory exist
            if not self.op.is_dir_exist(folder_location):
                error = f"The specified path does not exist : {folder_location}"
                return render_template("error.html", error=error)

            context = {}

            # Check if the video url is valid
            if user_option == "video":
                video = self.download_videos_list(url)
                for vid in video:
                    self.vid_lookup[vid.title] = vid

                context = {
                    "selection": user_option,
                    "videos": video
                }
                return render_template("home.html", context=context)
            elif user_option == 'playlist':
                videos = self.download_videos_list(url)
                for vid in videos:
                    self.vid_lookup[vid.title] = vid

                context = {
                    "selection": user_option,
                    "videos": videos
                }
                return render_template("home.html", context=context)
            else:
                error = f"Application can download  a video or playlist only"
                return render_template("error.html", error=error)

        elif request.method == "POST" and "form2" in request.form:
            to_download = []
            for vid in request.form.keys():
                if vid != "form2" and vid != "selectAll":
                    to_download.append(self.vid_lookup.get(vid))
            self.ytd.download_video_list(to_download, len(to_download), self.folder_location)

        return render_template('home.html')
