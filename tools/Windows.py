"""
title: Windows
description: Windows system tool collection
version: 0.1.0
author: Hui LIU
license: MIT
requirements:
required_open_webui_version: 0.8.12
"""

import os
import shutil
from pathlib import Path
from datetime import datetime


class Tools:
    def __init__(self):
        pass

    # Includes functions to save desktop images, save screensaver images, etc.

    def archive_desktop_images(
        self,
    ) -> str:
        """
        Save desktop images
        """

        user = os.getenv("USERPROFILE")
        source_path = rf"{user}\AppData\Roaming\Microsoft\Windows\Themes"
        target_path = rf"{user}\Downloads\screen-assets"

        def file_filter(file):
            return file.suffix.lower() not in {
                ".ini",
            }

        def file_rename(file):
            time = file.stat().st_mtime
            name = datetime.fromtimestamp(time).strftime("%Y%m%d")
            return f"{name}.jpg"

        return self._archive_images(
            source_path,
            target_path,
            file_rename,
            file_filter,
        )

    def archive_screen_images(
        self,
    ) -> str:
        """
        Save login-screen images
        """

        user = os.getenv("USERPROFILE")
        source_path = (
            rf"{user}\AppData\Local\Packages"
            r"\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy"
            r"\LocalState\Assets"
        )
        target_path = rf"{user}\Downloads\screen-assets"

        def file_rename(file):
            return f"{file.name}.jpg"

        return self._archive_images(
            source_path,
            target_path,
            file_rename,
        )

    def _archive_images(
        self,
        source_path,
        target_path,
        file_rename,
        file_filter=None,
    ):
        """
        Common logic for saving images
        """
        try:
            source = Path(source_path)
            target = Path(target_path)
            target.mkdir(parents=True, exist_ok=True)

            for file in source.rglob("*"):
                if not file.is_file():
                    continue
                if file_filter and not file_filter(file):
                    continue

                dest = target / file_rename(file)
                shutil.copy2(file, dest)

            return f"Saving completed, saved at {target_path}"
        except Exception as e:
            print(e)

            return str(e)
