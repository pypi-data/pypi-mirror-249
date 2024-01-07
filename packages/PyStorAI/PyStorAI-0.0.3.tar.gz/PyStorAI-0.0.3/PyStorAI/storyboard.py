import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

def pdf_output(*indices):

    # List of image filenames with full paths or relative paths
    image_filenames = ['image1.png', 'image2.png', 'image3.png',
                   'image4.png', 'image5.png', 'image6.png']

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