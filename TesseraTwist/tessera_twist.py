from image.image_generator import VerticalSingleSourceImageGenerator
from image.sequence_generator import SequenceGenerator


if __name__ == "__main__":
    factory = lambda: VerticalSingleSourceImageGenerator(
        source="sample2.jpg",
        pieces_count=20,
    )

    seconds = 10

    for s in range(seconds):
        sequence_generator = SequenceGenerator(
            sequence_length=24,
            image_generator_factory=factory,
            workers=10,
            output_directory="./output/",
            output_prefix=f"output.s{s}"
        )

        sequence_generator.generate()
