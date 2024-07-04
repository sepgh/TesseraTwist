import argparse

from image.helper import get_image_info
from image.image_generator import VerticalSingleSourceImageGenerator, HorizontalSingleSourceImageGenerator, \
    TilingSingleSourceImageGenerator
from image.sequence_generator import SequenceGenerator
from video.timelapse_generator import TimelapseGenerator


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='Tessera Twist',
        description='Sliced image turns into a timelaps',
        epilog='Get more info at: https://github.com/sepgh/TesseraTwist'
    )
    parser.add_argument('-i', '--input', help='Input image file', required=True)
    parser.add_argument('-o', '--output', help='Output timelapse path (including filename ending in mp4)', required=True)
    parser.add_argument(
        '-g',
        '--generator',
        choices=['SV', 'SH', 'ST'],
        required=True,
        help='Image generator type. '
             '"SV" for "VerticalSingleSourceImageGenerator",'
             ' "SH" for "HorizontalSingleSourceImageGenerator",'
             ' "ST" for "TilingSingleSourceImageGenerator"',
    )
    parser.add_argument(
        '-s',
        '--storage',
        help='Storage directory to store timelapse images in. Default would be in temp.',
        required=False
    )
    parser.add_argument('-p', '--pieces', help='Pieces / Slices count', type=int, default=10, required=False)
    parser.add_argument('-w', '--workers', help='Number of worker processes', type=int, default=4, required=False)
    parser.add_argument('-d', '--duration', help='Duration of the clip in seconds', type=int, default=15, required=False)
    parser.add_argument('-fb', '--ffmpeg', help='Path to ffmpeg executable', type=str, default='ffmpeg', required=False)
    parser.add_argument('-crf', help="Value for crf flag passed to ffmpeg", type=int, default=17, required=False)
    parser.add_argument('-fps', help="Value for fps flag passed to ffmpeg", type=int, default=24, required=False)
    parser.add_argument('-smoother', help="Smoothing by doing more shifts next to shuffles. This is incomplete.", type=int, choices=[1, 0], default=0, required=False)
    args = vars(parser.parse_args())

    if args['generator'] == 'SV':
        factory = lambda: VerticalSingleSourceImageGenerator(
            source=args["input"],
            pieces_count=args["pieces"],
        )
    elif args['generator'] == 'SH':
        factory = lambda: HorizontalSingleSourceImageGenerator(
            source=args["input"],
            pieces_count=args["pieces"],
        )
    elif args['generator'] == 'ST':
        factory = lambda: TilingSingleSourceImageGenerator(
            source=args["input"],
            pieces_count=args["pieces"]
        )

    w, h, ext = get_image_info(args["input"])

    seconds = args["duration"]

    for s in range(seconds):
        sequence_generator = SequenceGenerator(
            sequence_length=args["fps"],
            image_generator_factory=factory,
            workers=args["workers"],
            output_directory=args["storage"],
            output_prefix=f"tessera_twist.s{s}",
            extension=ext,
            smoothing=bool(args["smoother"]),
        )

        sequence_generator.generate()

    TimelapseGenerator(
        args["ffmpeg"],
        args["fps"],
        ext,
        crf=args["crf"],
        input_directory=args["storage"],
        output_path=args["output"],
        width=w, height=h
    ).generate()
