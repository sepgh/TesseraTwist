import random
from abc import ABC, abstractmethod
from math import floor
from typing import List

from PIL import Image


class SingleSourceImageGenerator(ABC):

    def __init__(self, source: str, pieces_count: int, **kwargs):
        self.source = source
        self.pieces_count = pieces_count
        self.slices: List = None
        self.image_width = None
        self.image_height = None
        self._build_called = False
        self.args = kwargs

    def build(self) -> "SingleSourceImageGenerator":
        image = Image.open(self.source)
        image_width, image_height = image.size
        self.image_width = image_width
        self.image_height = image_height
        self.slices = self.slice_image(image)
        self.randomize()
        self._build_called = True
        return self

    @abstractmethod
    def get_piece_position(self, piece_index):
        raise NotImplemented

    def slice_image(self, image):
        slices = []

        for p in range(0, self.pieces_count):
            image_slice = image.crop(self.get_piece_position(p))
            slices.append(image_slice)

        return slices

    def generate_output(self, output_path: str):
        if not self._build_called:
            self.build()

        new_image = Image.new('RGB', (self.image_width, self.image_height))  # Todo: concept mode may need to be a param

        for p in range(0, self.pieces_count):
            new_image.paste(self.slices[p], self.get_piece_position(p))

        new_image.save(output_path)
        new_image.close()

    def randomize(self):
        random.shuffle(self.slices)
        return self

    def shift_slices(self):
        self.slices = self.slices[-1:] + self.slices[:-1]
        return self


class HorizontalSingleSourceImageGenerator(SingleSourceImageGenerator):

    def get_piece_position(self, piece_index):
        piece_height: int = self.get_piece_height()
        height_start = piece_index * piece_height
        height_end = (piece_index + 1) * piece_height
        return 0, height_start, self.image_width, height_end

    def get_piece_height(self) -> int:
        return floor(self.image_height / self.pieces_count)


class VerticalSingleSourceImageGenerator(SingleSourceImageGenerator):

    def get_piece_position(self, piece_index):
        piece_width: int = self.get_piece_width()
        width_start = piece_index * piece_width
        width_end = (piece_index + 1) * piece_width
        return width_start, 0, width_end, self.image_height

    def get_piece_width(self):
        return floor(self.image_width / self.pieces_count)


class TilingSingleSourceImageGenerator(SingleSourceImageGenerator):

    def __init__(self, source: str, pieces_count: int, **kwargs):
        self.initial_pieces_count = pieces_count
        self.width_slicing_index = 0
        pieces_count = pieces_count * pieces_count
        super().__init__(source, pieces_count, **kwargs)

    def get_piece_position(self, p):
        piece_width: int = self.get_piece_width()
        piece_height: int = self.get_piece_height()

        h_i = floor(p / self.initial_pieces_count)
        w_i = p % self.initial_pieces_count

        height_start = h_i * piece_height
        height_end = (h_i + 1) * piece_height

        width_start = w_i * piece_width
        width_end = (w_i + 1) * piece_width

        return width_start, height_start, width_end, height_end

    def get_piece_width(self):
        return floor(self.image_width / self.initial_pieces_count)

    def get_piece_height(self) -> int:
        return floor(self.image_height / self.initial_pieces_count)
