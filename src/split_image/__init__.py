#!/usr/bin/env python

"""Split an image into a grid of smaller square images for social
messaging platforms.
"""

import logging
from os import path
from typing import Iterator, Tuple

import click
from PIL import Image

from . import utils

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def split_image(
    image: Image.Image, size: int
) -> Iterator[Tuple[int, int, Image.Image]]:
    """Split the image into multiple square sub-images, padding as
    necessary
    """
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
@click.option("--estimate", is_flag=True)
@click.argument("image", type=click.Path(exists=True, dir_okay=False, readable=True))
def cli(size: int, verbose: bool, estimate: bool, image: str):
    """Takes in command-line input to create a grid of images from an
    input image
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
    output_path, filename = utils.get_path_and_filename(image)

    image = Image.open(image)
    rows, cols = utils.get_unit_dimensions(*image.size, size)

    if estimate:
        if verbose:
            logger.debug(
                "Image with grid size will create a grid of unit dimensions %s",
                (rows, cols),
            )
        else:
            logger.setLevel(logging.INFO)
            logger.info((rows, cols))
    else:
        utils.reset_dir(output_path)
        for x, y, sub_image in split_image(image, size):
            filepath = utils.format_output(output_path, filename, x, y)
            logger.debug("Saving %s", filepath)
            sub_image.save(filepath)
        with open(path.join(output_path, "emoji.txt"), "wt", encoding="utf-8") as f:
            for c in range(cols):
                for r in range(rows):
                    f.write(f":{filename}-{c:02}-{r:02}:")
                f.write("\n")
