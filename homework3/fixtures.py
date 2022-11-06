import os

import pytest


@pytest.fixture()
def file_path(repo_root):
    """
    Определение пути к файлу, предназначенномиу для загрузки
    """
    return os.path.join(repo_root, "video_6sec.mp4")
