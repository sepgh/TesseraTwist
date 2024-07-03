import random
from abc import ABC, abstractmethod
from math import floor

from PIL import Image


class SingleSourceImageBuilder(ABC):

    def __init__(self, source: str, pieces_count: int, **kwargs):
        self.source = source
        self.pieces_count = pieces_count
        self.slices = None
        self.image_width = None
        self.image_height = None
        self._build_called = False
        self.args = kwargs

    def build(self) -> "SingleSourceImageBuilder":
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
        new_image.show("Test")  # Todo: remove
        new_image.close()

    def randomize(self):
        random.shuffle(self.slices)


class HorizontalSingleSourceImageBuilder(SingleSourceImageBuilder):

    def get_piece_position(self, piece_index):
        piece_height: int = self.get_piece_height()
        height_start = piece_index * piece_height
        height_end = (piece_index + 1) * piece_height
        return 0, height_start, self.image_width, height_end

    def get_piece_height(self) -> int:
        return floor(self.image_height / self.pieces_count)


class VerticalSingleSourceImageBuilder(SingleSourceImageBuilder):

    def get_piece_position(self, piece_index):
        piece_width: int = self.get_piece_width()
        width_start = piece_index * piece_width
        width_end = (piece_index + 1) * piece_width
        return width_start, 0, width_end, self.image_height

    def get_piece_width(self):
        return floor(self.image_width / self.pieces_count)
