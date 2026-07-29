import os
from glob import glob

import numpy as np
from PIL import Image


def average_images(input_dir: str, output_path: str = "averaged.png"):
    """
    Calculate the pixel-wise average of all PNG images in a directory.

    This function loads every PNG image in the specified directory,
    computes the average value for each pixel across all images, and
    saves the resulting averaged image to the specified output path.

    All images are assumed to have the same dimensions and colour format.

    Args:
        input_dir (str):
            Path to the directory containing PNG images.
        output_path (str, optional):
            File path where the averaged image will be saved.
            Defaults to "averaged.png".

    Raises:
        ValueError:
            If the input directory contains no PNG images.

    Returns:
        None
    """

    # Retrieve and sort all PNG image file paths in the input directory.
    files = sorted(glob(os.path.join(input_dir, "*.png")))

    # Ensure that at least one image was found.
    if not files:
        raise ValueError("No PNG images found in directory.")

    # Load the first image to determine the required array shape.
    # Convert to float64 to avoid overflow during accumulation.
    first = np.array(Image.open(files[0]), dtype=np.float64)

    # Create an array of zeros with the same dimensions as the images.
    accumulator = np.zeros_like(first)

    # Add each image's pixel values to the accumulator.
    for f in files:
        accumulator += np.array(Image.open(f), dtype=np.float64)

    # Divide by the number of images to obtain the average pixel values.
    averaged = (accumulator / len(files)).astype(np.uint8)

    # Convert the NumPy array back into an image.
    out_img = Image.fromarray(averaged)

    # Save the averaged image to disk.
    out_img.save(output_path)

    # Notify the user that processing has completed.
    print(f"Averaged image saved to {output_path}")