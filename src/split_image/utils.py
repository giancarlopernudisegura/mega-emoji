#!/usr/bin/env python

"""Utility methods"""

import math
import pathlib
from os import getcwd, path
from shutil import rmtree
from typing import Tuple


def get_unit_dimensions(width: int, height: int, grid_size: int) -> Tuple[int, int]:
    """Get the unit dimensions for the final grid of images.

    Args:
        width (int): The width of the original image in pixels
        height (int): The height of the original image in pixels
        grid_size (int): The size of a grid square in pixels

    Returns:
        Tuple[int, int]: The unit dimensions (cols, rows)
    """
    cols = math.ceil(width / grid_size)
    rows = math.ceil(height / grid_size)
    return (cols, rows)


def format_output(output_path: str, filename: str, x: int, y: int) -> str:
    """Get the formatted output name for a sub-image

    Args:
        output_path (str): The path where the sub-image is to be saved
        filename (str): The base name for the sub-image
        x (int): The x-coordinate
        y (int): The y-coordinate

    Returns:
        str: The full path where the final sub-image will be saved
    """
    return path.join(output_path, f"{filename}-{x:02}-{y:02}.png")


def get_path_and_filename(filepath: str) -> Tuple[str, str]:
    """Get the path for saving the images

    Args:
        filepath (str): The path of the original image

    Returns:
        Tuple[str, str]: Path where to save the sub-images
    """
    filename, _ = path.basename(filepath).split(".", maxsplit=1)
    output_path = path.join(getcwd(), filename)
    return (output_path, filename)


def reset_dir(output_path: str):
    """Reset a directory

    If the directory contains any files, they are deleted. If the
    directory does not exist, it is created.

    Args:
        output_path (str): Directory to reset
    """
    if path.exists(output_path):
        rmtree(output_path)
    pathlib.Path(output_path).mkdir()


__all__ = [
    "format_output",
    "get_path_and_filename",
    "get_unit_dimensions",
    "reset_dir",
]
