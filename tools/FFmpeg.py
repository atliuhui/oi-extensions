"""
title: FFmpeg
description: 音视频文件转换工具集合
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

    # 通过FFmpeg帮忙转为音视频文件的格式

    def convert_audio(
        self,
        input_file_path: str = Field(
            ..., description="（被转换的）输入文件路径，例如：C:\\input.mp4。"
        ),
    ) -> str:
        """
        将输入转为音频mp3
        """

        output_file_path = f"{input_file_path}.mp3"  # （转换后的）输出文件路径。
        if os.path.exists(output_file_path):
            return f"'{output_file_path}' already exists."

        try:
            ffmpeg.input(input_file_path).output(output_file_path).global_args(
                "-n"
            ).run()

            return f"转换已经完成，保存的路径是{output_file_path}"
        except Exception as e:
            print(e)

            return str(e)

    def replace_audio(
        self,
        input_video_path: str = Field(
            ..., description="（被替换的）视频文件路径，例如：C:\\input.mp4。"
        ),
        input_audio_path: str = Field(
            ..., description="（要转换的）音频文件路径，例如：C:\\input.mp3。"
        ),
    ) -> str:
        """
        使用音频替换视频的音轨
        """

        output_file_path = f"{input_video_path}.mp4"  # （替换后的）输出文件路径。
        if os.path.exists(output_file_path):
            return f"'{output_file_path}' already exists."

        try:
            v = ffmpeg.input(input_video_path)
            a = ffmpeg.input(input_audio_path)

            ffmpeg.output(
                v.video,  # 视频流取自第 1 个输入（0:v）
                a.audio,  # 音频流取自第 2 个输入（1:a）
                output_file_path,
                vcodec="copy",  # 视频不重编码
                acodec="aac",  # 在 MP4 容器里 AAC 兼容性最稳
                shortest=None,  # 让输出以较短者结束，避免音频长于视频时产生尾部黑屏/静音拖尾
            ).global_args("-n").run()

            return f"替换已经完成，保存的路径是{output_file_path}"
        except Exception as e:
            print(e)

            return str(e)
