from image.image_generator import VerticalSingleSourceImageGenerator
from image.sequence_generator import SequenceGenerator


if __name__ == "__main__":
    factory = lambda: VerticalSingleSourceImageGenerator(
        source="sample2.jpg",
        pieces_count=20,
    )

    sequence_generator = SequenceGenerator(
        sequence_length=24,
        image_generator_factory=factory,
        workers=4,
        output_directory="./output/",
        output_prefix="output"
    )

    sequence_generator.generate()
