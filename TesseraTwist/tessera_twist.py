from image.image_builder import HorizontalSingleSourceImageBuilder


if __name__ == "__main__":
    HorizontalSingleSourceImageBuilder(
        source="sample2.jpg",
        pieces_count=20,
        output="output.jpg",
    ).build()
