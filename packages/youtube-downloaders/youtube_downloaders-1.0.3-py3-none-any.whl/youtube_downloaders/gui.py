import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from youtube_downloaders.youtube import youtube_download as yd


class GUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Youtube Downloader")
        self.frame = tk.LabelFrame(self.root, text="Download Youtube")
        self.frame.grid(padx=20, sticky="w")

        self.selected_option = None

        self.url_obj = None
        self.provided_url = None

        self.folder_lb = None
        self.folderlocation = None

        self.frame2 = tk.LabelFrame(self.root, text="Videos")
        self.frame2.grid(padx=20, pady=20, sticky="w")

        self.videos = []

    def user_option(self, value):
        self.selected_option = value
        return self.selected_option

    def set_folderlocation(self, location):
        self.folderlocation = location
        return self.folderlocation

    def set_url_obj(self, url_obj):
        self.url_obj = url_obj
        return self.url_obj

    def set_provided_url(self, url):
        self.provided_url = url
        return self.provided_url

    def open_directory(self):
        if self.folder_lb is not None:
            self.folder_lb.destroy()
        folder_location = filedialog.askdirectory(initialdir="./")
        self.set_folderlocation(folder_location)
        self.folder_lb = tk.Label(self.frame, text=folder_location)
        self.folder_lb.grid(row=3, column=2, padx=20)
        return folder_location

    def setup_stage(self):
        self.set_provided_url(self.url_obj.get())
        if (
            self.folderlocation is None
            or self.provided_url is None
            or self.provided_url.strip() == ""
        ):
            messagebox.showerror("Input Error", "Please select location and URL")
            return False
        self.fetch_videos()

    def fetch_videos(self):
        if len(self.videos) > 0:
            for vid in self.videos:
                vid.destroy()
        ytb = yd(self.provided_url)
        lb = tk.Label(self.frame2, text=f"Total videos {ytb.number_of_videos_from_url}")
        lb.grid(row=0, column=0)

        all_select = tk.BooleanVar()
        all_select.set(False)

        video_key_value = {}
        checkbox = [tk.IntVar() for _ in range(ytb.number_of_videos_from_url)]

        def _select_all_videos():
            value = all_select.get()
            if value is True:
                for var in range(len(checkbox)):
                    checkbox[var].set(var + 1)
            else:
                for var in range(len(checkbox)):
                    checkbox[var].set(0)

        def _download_selected_video(row_num):
            to_download = []
            for var in range(len(checkbox)):
                if checkbox[var].get() != 0:
                    key = var + 1
                    to_download.append(video_key_value[key])
            ytb.download_video_list(to_download, len(to_download), self.folderlocation)

        selection = tk.Checkbutton(
            self.frame2,
            text="Select All",
            variable=all_select,
            command=_select_all_videos,
        )
        selection.deselect()
        selection.grid(row=1, column=0, sticky="w")

        row_num = 2
        iter = 1
        for video in ytb.videos_from_url():
            select_var = tk.Checkbutton(
                self.frame2,
                text=video.title,
                variable=checkbox[iter - 1],
                onvalue=iter,
                offvalue=0,
            )
            video_key_value[iter] = video
            select_var.deselect()
            self.videos.append(select_var)
            select_var.grid(row=row_num, column=0, sticky="w")
            row_num += 1
            iter += 1

        download_btn = tk.Button(
            self.frame2,
            text="download",
            width=100,
            bg="#FF681C",
            command=lambda row_num=row_num: _download_selected_video(row_num),
        )
        download_btn.grid(row=row_num, column=0, sticky="w")
        self.videos.append(download_btn)

    def widget(self):
        # Creat widget
        option = tk.StringVar()
        option.set("video")
        option_lb = tk.Label(self.frame, text="Select the option to download")
        option_lb.grid(row=0, column=0)
        radio1 = tk.Radiobutton(
            self.frame,
            text="video",
            variable=option,
            value="video",
            command=lambda: self.user_option(option.get()),
        )
        radio2 = tk.Radiobutton(
            self.frame,
            text="playlist",
            variable=option,
            value="playlist",
            command=lambda: self.user_option(option.get()),
        )
        radio1.grid(row=0, column=1)
        radio2.grid(row=1, column=1)

        url_lb = tk.Label(self.frame, text="Enter the Youtube URL")
        url_lb.grid(row=2, column=0, sticky="w")
        urlinput = tk.Entry(self.frame, width=50)
        self.set_url_obj(urlinput)
        urlinput.grid(row=2, column=1, padx=20)
        location_lb = tk.Label(self.frame, text="Location to save the video/playlist")
        location_lb.grid(row=3, column=0)
        tk.Button_directory = tk.Button(
            self.frame, text="Folder location", command=self.open_directory
        )
        tk.Button_directory.grid(row=3, column=1)

        tk.Button_directory = tk.Button(
            self.frame, text="Fetch Video Information", command=self.setup_stage
        )
        tk.Button_directory.grid(row=4, column=0)

        tk.Button_quit = tk.Button(
            self.root,
            text="Exit Program",
            command=self.root.quit,
            width=20,
            height=2,
            bg="#FA613A",
        )
        tk.Button_quit.grid(row=5, column=1, padx=10, pady=10)
        # Create Widget
        self.root.mainloop()
