import random
from abc import ABC
from math import floor, ceil

from PIL import Image, ImageFile


class SingleSourceImageBuilder(ABC):

    def __init__(self, source: str, pieces_count: int, output: str, **kwargs):
        self.source = source
        self.output = output
        self.pieces_count = pieces_count
        self.args = kwargs

    def build(self):
        image = Image.open(self.source)
        slices, image_width, image_height = self.slice_image(image)
        self.randomize(slices)
        self.generate_output(slices, image_width, image_height)

    def slice_image(self, image):
        raise NotImplemented

    def generate_output(self, slices, image_width, image_height):
        raise NotImplemented

    def randomize(self, slices):
        random.shuffle(slices)


class HorizontalSingleSourceImageBuilder(SingleSourceImageBuilder):

    def slice_image(self, image: ImageFile):
        image_width, image_height = image.size
        piece_height: int = self.get_piece_height(image_height)
        slices = []

        for p in range(0, self.pieces_count):
            height_start = p * piece_height
            height_end = (p + 1) * piece_height

            image_slice = image.crop((0, height_start, image_width, height_end))
            slices.append(image_slice)

        return slices, image_width, image_height

    def get_piece_height(self, image_height) -> int:
        return floor(image_height / self.pieces_count)

    def generate_output(self, slices, image_width, image_height):
        new_image = Image.new('RGB', (image_width, image_height))   # Todo: concept mode may need to be a param

        piece_height: int = self.get_piece_height(image_height)
        for p in range(0, self.pieces_count):
            height_start = p * piece_height
            height_end = (p + 1) * piece_height
            new_image.paste(slices[p], (0, height_start, image_width, height_end))

        new_image.save(self.output)
        new_image.show("Test")   # Todo: remove
        new_image.close()


class VerticalSingleSourceImageBuilder(SingleSourceImageBuilder):

    def slice_image(self, image):
        image_width, image_height = image.size
        piece_width: int = self.get_piece_width(image_width)

        slices = []

        for p in range(0, self.pieces_count):
            width_start = p * piece_width
            width_end = (p + 1) * piece_width
            image_slice = image.crop((width_start, 0, width_end, image_height))
            slices.append(image_slice)

        return slices, image_width, image_height

    def get_piece_width(self, image_width):
        return floor(image_width / self.pieces_count)

    def generate_output(self, slices, image_width, image_height):
        new_image = Image.new('RGB', (image_width, image_height))   # Todo: concept mode may need to be a param
        piece_width: int = self.get_piece_width(image_width)
        for p in range(0, self.pieces_count):
            width_start = p * piece_width
            width_end = (p + 1) * piece_width
            new_image.paste(slices[p], (width_start, 0, width_end, image_height))

        new_image.save(self.output)
        new_image.show("Test")   # Todo: remove
        new_image.close()


