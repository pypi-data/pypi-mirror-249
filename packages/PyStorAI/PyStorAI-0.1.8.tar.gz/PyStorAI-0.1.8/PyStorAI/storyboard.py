import requests
import os

def download_and_rename_images(base_url, num_images):
    downloaded_images = set()

    for i in range(1, num_images + 1):
        url = f"{base_url}{i}.png?raw=true"

        if url in downloaded_images:
            print(f"Image {i} already downloaded. Skipping.")
            continue

        response = requests.get(url)

        if response.status_code == 200:
            # Extracting the filename from the URL
            file_name = f"image{i}.png"

            with open(file_name, 'wb') as f:
                f.write(response.content)
                print(f"Image {i} downloaded successfully.")

            # Renaming the file to remove the "?raw=true" part
            os.rename(file_name, f"image{i}.png")
            print(f"Image {i} renamed.")

            # Add the URL to the set of downloaded images
            downloaded_images.add(url)
        else:
            print(f"Failed to download image {i}. Status code: {response.status_code}")

# Example usage:
base_url = "https://github.com/VisualXAI/PyStorAI/blob/main/image"
num_images = 6

download_and_rename_images(base_url, num_images)

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

def pdf_output(*indices):

    # List of image filenames with full paths or relative paths
    image_filenames = ['image1.png', 'image2.png', 'image3.png', 'image4.png', 'image5.png', 'image6.png']

    # Captions for each image
    captions = ['Machine Learning', 'Classification', 'Regression', 'Supervised', 'Unsupervised', 'Reinforcement']

    # Number of images per row
    images_per_row = 3
    images_per_column = 2

    # Create subplots
    fig, axes = plt.subplots(images_per_column, images_per_row, figsize=(6, 4))

    # Flatten the axes array to simplify indexing
    axes = axes.flatten()

    for i, filename in enumerate(image_filenames):
        img = mpimg.imread(filename)
        axes[i].imshow(img)
        axes[i].axis('off')

        # Add caption
        axes[i].text(0.5, -0.1, captions[i], size=10, ha="center", transform=axes[i].transAxes)

    # Adjust layout and display
    plt.tight_layout()

    # Save as PDF
    with PdfPages('output.pdf') as pdf:
        pdf.savefig()

    # Display the Matplotlib plot in the notebook
    plt.show()