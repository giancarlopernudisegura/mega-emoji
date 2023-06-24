#!/usr/bin/env python

"""Split an image into a grid of smaller square images for social
messaging platforms.
"""

import logging
from os import getcwd, path
from shutil import rmtree
from typing import Iterator, Tuple
import pathlib

import click
from PIL import Image


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def split_image(
    image: Image.Image, size: int
) -> Iterator[Tuple[int, int, Image.Image]]:
    width, height = image.size
    # pad image
    width = (width + size - 1) // size * size
    height = (height + size - 1) // size * size
    padded_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    padded_image.paste(image)

    for i, x in enumerate(range(0, width, size)):
        for j, y in enumerate(range(0, height, size)):
            img = padded_image.crop((x, y, x + size, y + size))
            yield (i, j, img)


@click.command(help=__doc__)
@click.option("-s", "--size", default=32, help="Grid size")
@click.option("-v", "--verbose", is_flag=True)
@click.argument("image", type=click.Path(exists=True, dir_okay=False, readable=True))
def cli(size: int, verbose: bool, image: str):
    if verbose:
        logger.setLevel(logging.DEBUG)
    filename, _ = path.basename(image).split(".", maxsplit=1)
    output_path = path.join(getcwd(), filename)
    if path.exists(output_path):
        rmtree(output_path)
    pathlib.Path(output_path).mkdir()
    image = Image.open(image)
    for x, y, sub_image in split_image(image, size):
        file_path = path.join(output_path, f"{filename}-{x:02}-{y:02}.png")
        logger.debug("Saving %s", file_path)
        sub_image.save(file_path)
