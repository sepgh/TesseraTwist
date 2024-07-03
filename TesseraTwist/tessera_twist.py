from image.image_builder import HorizontalSingleSourceImageBuilder, VerticalSingleSourceImageBuilder

if __name__ == "__main__":
    HorizontalSingleSourceImageBuilder(
        source="sample.jpg",
        pieces_count=20,
        output="output.jpg",
    ).build()
