import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.backends.backend_pdf import PdfPages

import base64
from IPython.display import HTML

import os
import requests

def pdf_output(*indices):

    base_url = "https://github.com/VisualXAI/PyStorAI/blob/main/image"
    num_images = 6

    downloaded_images = set()

    for i in indices:
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

    image_files = [f"image{index}.png" for index in indices]

    # Determine the number of columns based on the number of images
    num_images = len(image_files)
    if num_images <= 4:
        num_cols = num_images
    elif num_images <= 6:
        num_cols = 3
    elif num_images <= 8:
        num_cols = 4
    elif num_images == 9:
        num_cols = 3
    elif num_images <=12:
        num_cols = 4
    elif num_images <=15:
        num_cols = 5
    else:
        num_cols = 4

    num_rows = -(-num_images // num_cols)  # Ceiling division

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols*2, num_rows*2))

    # Plot each image and only show necessary axes
    for i, file_name in enumerate(image_files):
        img = imread(file_name)
        ax = axes[i // num_cols, i % num_cols] if num_rows > 1 else axes[i % num_cols]
        ax.imshow(img)
        ax.axis('off')

    # Hide any remaining empty axes
    for i in range(num_images, num_rows * num_cols):
        axes.flatten()[i].axis('off')

    # Adjust layout and show the plot
    plt.tight_layout()

    # Save as PDF
    with PdfPages('output.pdf') as pdf:
        pdf.savefig()

    plt.show()



def html_output(*indices):


    base_url = "https://github.com/VisualXAI/PyStorAI/blob/main/image"
    num_images = 6

    downloaded_images = set()

    for i in indices:
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

    image_files = [f"image{index}.png" for index in indices]

    # Create an HTML string
    html_content = '<html><body><table style="width:100%;"><tr>'

    for i, filename in enumerate(image_files):
        # Read the image file
        with open(filename, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Embed the image in the HTML
        html_content += f'<td style="text-align:center;"><img src="data:image/png;base64,{encoded_image}" </h2></td>'

        # Start a new row after every fourth image
        if (i + 1) % 4 == 0 and i < len(image_files) - 1:
            html_content += '</tr><tr>'

    html_content += '</tr></table></body></html>'

    # Save as HTML file
    html_filename = 'output.html'
    with open(html_filename, 'w') as html_file:
        html_file.write(html_content)

    # Determine the number of columns based on the number of images
    num_images = len(image_files)
    if num_images <= 4:
        num_cols = num_images
    elif num_images <= 6:
        num_cols = 3
    elif num_images <= 8:
        num_cols = 4
    elif num_images == 9:
        num_cols = 3
    elif num_images <=12:
        num_cols = 4
    elif num_images <=15:
        num_cols = 5
    else:
        num_cols = 4

    num_rows = -(-num_images // num_cols)  # Ceiling division

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols*2, num_rows*2))

    # Plot each image and only show necessary axes
    for i, file_name in enumerate(image_files):
        img = imread(file_name)
        ax = axes[i // num_cols, i % num_cols] if num_rows > 1 else axes[i % num_cols]
        ax.imshow(img)
        ax.axis('off')

    # Hide any remaining empty axes
    for i in range(num_images, num_rows * num_cols):
        axes.flatten()[i].axis('off')

    # Adjust layout and show the plot
    plt.tight_layout()