from image.image_builder import HorizontalSingleSourceImageBuilder, VerticalSingleSourceImageBuilder

if __name__ == "__main__":
    builder = VerticalSingleSourceImageBuilder(
        source="sample2.jpg",
        pieces_count=20,
    ).build()

    builder.generate_output("output.jpg")
    builder.randomize()
    builder.generate_output("output2.jpg")

