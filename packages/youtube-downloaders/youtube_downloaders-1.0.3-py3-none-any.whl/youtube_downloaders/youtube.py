import concurrent.futures
from pytube import Playlist, YouTube
import re
from youtube_downloaders.os_operations import operations as op
from youtube_downloaders.exception import youtubeException


class youtube_download:
    def __init__(self, url):
        self.url = url
        self.op = op()
        if self._check_url_playlist(self.url):
            self.playlist = Playlist(self.url)
        else:
            self.video = YouTube(self.url)

    @staticmethod
    def _check_url_playlist(url):
        match = re.search(r"playlist", url)
        return True if match else False

    def download_videos(self, vid, path):
        if self.op.is_dir_exist(path):
            print(f"Video to be downloaded: {vid.title}")
            vid.streams.get_highest_resolution().download(output_path=path)
            print(f"Video download completed : {vid.title}")
            return vid.title
        raise youtubeException(f"The specified path does not exist : {path}")

    def download_single_video(self, path):
        self.download_videos(self.video, path)

    def videos_from_url(self):
        if self._check_url_playlist(self.url):
            return list(self.playlist.videos)
        else:
            video = []
            video.append(self.video)
            return video

    @property
    def number_of_videos_from_url(self):
        if self._check_url_playlist(self.url):
            return self.playlist_length
        else:
            return 1

    @property
    def playlist_length(self):
        return len(self.playlist.video_urls)

    @staticmethod
    def _chunking(entire_list, num_of_elem_in_chunks):
        chunked_array = []
        for i in range(0, len(entire_list), num_of_elem_in_chunks):
            chunked_array.append(entire_list[i : i + num_of_elem_in_chunks])
        return chunked_array

    def playlist_download(self, parallel_number, path):
        print(f"Total {self.playlist_length} videos are present in the playlist")
        self.download_video_list(list(self.playlist.videos), parallel_number, path)

    def download_video_list(self, vido_list, parallel_number, path):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            chucked_video_array = self._chunking(vido_list, parallel_number)
            for vid_array in chucked_video_array:
                results = {}

                for video in vid_array:
                    results[
                        executor.submit(self.download_videos, video, path)
                    ] = video.title

                for result in concurrent.futures.as_completed(results.keys()):
                    try:
                        success = result.result()
                        print(f"Video COMPLETED - {success} successfully.")
                    except Exception as e:
                        print(f"Video FAILED - {results[result]} \n {e}.")

    def __str__(self) -> str:
        return f"Youtube download URL : {self.url}"
