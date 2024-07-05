import subprocess
import os


class TimelapseGenerator:
    def __init__(
            self,
            ffmpeg_bin: str,
            fps: int,
            image_format: str,
            crf: int,
            input_directory: str,
            output_path: str,
            width: int,
            height: int
    ):
        self.ffmpeg_bin = ffmpeg_bin
        self.fps = fps
        self.image_format = image_format
        self.crf = crf
        self.input_directory = input_directory
        self.output_path = output_path
        self.width = width if width % 2 == 0 else width + 1
        self.height = height if height % 2 == 0 else height + 1

    def get_args(self):
        return (
            self.ffmpeg_bin,
            "-framerate", f"{self.fps}",
            "-pattern_type", "glob",
            "-i", f"{os.path.join(self.input_directory, f"*{self.image_format}")}",
            "-s:v", f"{self.width}x{self.height}",
            "-c:v", f"libx264",
            "-crf", f"{self.crf}",
            f"{self.output_path}"
        )

    def generate(self):
        args = self.get_args()

        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()


