import json
import os
from argparse import Namespace
from pathlib import Path

from caelestia.utils.wallpaper import get_colours_for_wall, get_wallpaper, set_random, set_wallpaper


class Command:
    args: Namespace

    def __init__(self, args: Namespace) -> None:
        self.args = args

    def run(self) -> None:
        if self.args.print:
            print(json.dumps(get_colours_for_wall(self.args.print, self.args.no_smart)))
        elif getattr(self.args, "boot", False):
            wall = get_wallpaper()
            if wall:
                wall_path = Path(wall)
                is_video = wall_path.suffix.lower() in [".mp4", ".webm", ".mkv", ".avi"]
                if is_video:
                    import subprocess
                    subprocess.run(["pkill", "-f", "mpvpaper"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    log_file = open(os.path.expanduser("~/.local/state/caelestia/mpvpaper.log"), "w")
                    mpv_opts = "loop-file=inf no-audio --panscan=1.0 --hwdec=no --cache=no --demuxer-max-bytes=50M --vd-lavc-fast=yes"
                    subprocess.Popen(["mpvpaper", "-p", "-o", mpv_opts, "*", str(wall_path)], start_new_session=True, stderr=log_file, stdout=log_file)
        elif self.args.file:
            set_wallpaper(self.args.file, self.args.no_smart)
        elif self.args.random:
            set_random(self.args)
        else:
            print(get_wallpaper() or "No wallpaper set")
