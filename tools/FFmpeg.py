"""
title: FFmpeg
description: Audio and video file conversion tool collection
version: 0.1.0
author: Hui LIU
license: MIT
requirements: ffmpeg-python
required_open_webui_version: 0.8.12
"""

import os
import ffmpeg
from pydantic import Field


class Tools:
    def __init__(self):
        pass

    # Convert audio and video file formats using FFmpeg

    def convert_audio(
        self,
        input_file_path: str = Field(
            ...,
            description=(r"Input file path to be converted. e.g., C:\input.mp4."),
        ),
    ) -> str:
        """
        Convert input file to audio mp3
        """

        # Output file path after conversion.
        output_file_path = f"{input_file_path}.mp3"
        if os.path.exists(output_file_path):
            return f"'{output_file_path}' already exists."

        try:
            ffmpeg.input(input_file_path).output(output_file_path).global_args(
                "-n"
            ).run()

            return f"Conversion completed, saved at {output_file_path}"
        except Exception as e:
            print(e)

            return str(e)

    def convert_audios(
        self,
        input_file_paths: list[str] = Field(
            ...,
            description=(
                r"Input file paths to be converted, "
                r"A list of file paths. "
                r'(e.g., ["C:\input1.mp4", "C:\input2.mp4"]).'
            ),
        ),
    ) -> str:
        """
        Convert multiple input files to audio mp3
        """

        results = [self.convert_audio(path) for path in input_file_paths]
        return "\n".join(results)

    def replace_audio(
        self,
        input_video_path: str = Field(
            ...,
            description=(r"Video file path to be replaced, e.g., C:\input.mp4."),
        ),
        input_audio_path: str = Field(
            ..., description=(r"Audio file path to be used, e.g., C:\input.mp3.")
        ),
    ) -> str:
        """
        Replace video's audio track with the provided audio
        """

        # Output file path after replacement.
        output_file_path = f"{input_video_path}.mp4"
        if os.path.exists(output_file_path):
            return f"'{output_file_path}' already exists."

        try:
            v = ffmpeg.input(input_video_path)
            a = ffmpeg.input(input_audio_path)

            ffmpeg.output(
                # Video stream from the first input (0:v)
                v.video,
                # Audio stream from the second input (1:a)
                a.audio,
                output_file_path,
                # Do not re-encode video
                vcodec="copy",
                # AAC has the best compatibility in MP4 container
                # Let output end with the shorter one to avoid black
                # screen/silence when audio is longer than video
                acodec="aac",
                shortest=None,
            ).global_args("-n").run()

            return f"Replacement completed, saved at {output_file_path}"
        except Exception as e:
            print(e)

            return str(e)
