from image.helper import get_image_info
from image.image_generator import VerticalSingleSourceImageGenerator
from image.sequence_generator import SequenceGenerator
from video.timelapse_generator import TimelapseGenerator


if __name__ == "__main__":
    factory = lambda: VerticalSingleSourceImageGenerator(
        source="sample2.jpg",
        pieces_count=20,
    )

    w, h, ext = get_image_info("sample2.jpg")

    seconds = 10

    for s in range(seconds):
        sequence_generator = SequenceGenerator(
            sequence_length=24,
            image_generator_factory=factory,
            workers=10,
            output_directory="./output/",
            output_prefix=f"output.s{s}",
            extension=ext
        )

        sequence_generator.generate()

    TimelapseGenerator(
        "ffmpeg",
        24,
        ext,  # Todo: detect
        crf=17,
        input_directory="./output/",
        output_path="./timelapse.mp4",
        width=w, height=h  # Todo: detect
    ).generate()
