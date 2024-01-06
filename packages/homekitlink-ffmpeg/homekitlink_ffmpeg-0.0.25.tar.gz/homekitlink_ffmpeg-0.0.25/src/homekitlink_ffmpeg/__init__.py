# homekitlink_ffmpeg/__init__.py
import os
import platform


def get_ffmpeg_binary():
    """Get the path to the appropriate FFmpeg binary."""
    # __file__ is the path to the current file (__init__.py)
    # We loop back to the directory of __init__.py and build the path from there
    package_dir = os.path.abspath(os.path.dirname(__file__))

    arch = platform.machine()
    if arch == 'x86_64':  # x86_64 systems (Intel and some AMD processors)
        binary_name = 'ffmpeg'  # or 'ffmpeg.exe' on Windows
        binary_path = os.path.join(package_dir, 'ffmpeg_binaries', 'x86', binary_name)
    elif arch == 'arm64':  # ARM systems (like Apple M1)
        binary_name = 'ffmpeg'  # or 'ffmpeg.exe' on Windows
        binary_path = os.path.join(package_dir, 'ffmpeg_binaries', 'arm', binary_name)
    else:
        raise ValueError(f"Unsupported architecture: {arch}")

    if not os.path.isfile(binary_path):
        raise FileNotFoundError(f"FFmpeg binary not found for the architecture at {binary_path}")

    return binary_path